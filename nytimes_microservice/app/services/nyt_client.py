"""NYTimes Top Stories and Article Search service integration with retries."""

import asyncio
import logging
from typing import Dict, List, Optional

import httpx
from fastapi import HTTPException

from app.core.settings import settings
from app.models.nytimes import (
    ArticleSearchQueryParams,
    ArticleSearchResponse,
    TopStoryResponse,
)

logger = logging.getLogger("nytimes-microservice")

MAX_RETRIES = 3
BACKOFF_FACTOR = 2  # Exponential backoff factor in seconds


async def _get_with_retries(
    client: httpx.AsyncClient, url: str, params: Optional[Dict[str, str]] = None
) -> Dict:
    """Make GET request with retries on 429 and transient errors."""
    retries = 0
    resp = None
    while retries < MAX_RETRIES:
        try:
            response = await client.get(url, params=params)
            resp = response
            if response.status_code == 429:
                wait_time = BACKOFF_FACTOR**retries
                logger.warning(
                    "Rate limited (429). Retry %d after %ds", retries + 1, wait_time
                )
                await asyncio.sleep(wait_time)
                retries += 1
                continue
            response.raise_for_status()
            return response.json()
        except (httpx.RequestError, httpx.HTTPStatusError) as exc:
            resp = getattr(exc, "response", None)
            if resp and resp.status_code >= 500:
                wait_time = BACKOFF_FACTOR**retries
                logger.warning(
                    "Server error %d. Retry %d after %ds",
                    resp.status_code,
                    retries + 1,
                    wait_time,
                )
                await asyncio.sleep(wait_time)
                retries += 1
                continue
            logger.error("Request failed: %s", exc)
            raise

    # If retries exhausted
    if resp and resp.status_code == 429:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    raise HTTPException(status_code=503, detail="Service unavailable after retries")


async def fetch_top_stories() -> List[TopStoryResponse]:
    """Fetch two most recent top stories from each category with retry."""
    categories = ["arts", "food", "movies", "travel", "science"]
    results: List[TopStoryResponse] = []

    async with httpx.AsyncClient(timeout=10) as client:
        for category in categories:
            url = f"https://api.nytimes.com/svc/topstories/v2/{category}.json"
            params = {"api-key": settings.nyt_api_key}
            try:
                data = await _get_with_retries(client, url, params=params)
                stories = data.get("results", [])[:2]
                for story in stories:
                    try:
                        results.append(
                            TopStoryResponse(
                                title=story.get("title", ""),
                                section=story.get("section", ""),
                                url=story.get("url", ""),
                                abstract=story.get("abstract", ""),
                                published_date=story.get("published_date", ""),
                            )
                        )
                    except Exception as exc:
                        logger.warning("Skipping malformed story: %s", exc)
            except Exception as exc:
                logger.error(
                    "Failed to fetch top stories for category '%s': %s", category, exc
                )
    return results


async def fetch_article_search(
    params: ArticleSearchQueryParams,
) -> List[ArticleSearchResponse]:
    """Fetch articles matching search query parameters with retry."""
    base_url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    query_params: Dict[str, str] = {
        "q": params.q,
        "api-key": settings.nyt_api_key,
    }

    if params.begin_date:
        query_params["begin_date"] = params.begin_date
    if params.end_date:
        query_params["end_date"] = params.end_date

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            data = await _get_with_retries(client, base_url, params=query_params)
        except Exception as exc:
            logger.error("Article search failed: %s", exc)
            raise

    docs = data.get("response", {}).get("docs", [])
    results: List[ArticleSearchResponse] = []
    for doc in docs:
        try:
            results.append(
                ArticleSearchResponse(
                    headline=doc.get("headline", {}).get("main", ""),
                    snippet=doc.get("snippet", ""),
                    web_url=doc.get("web_url", ""),
                    pub_date=doc.get("pub_date", ""),
                )
            )
        except Exception as exc:
            logger.warning("Skipping malformed article: %s", exc)
    return results
