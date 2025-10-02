"""NYTimes API endpoints for Top Stories and Article Search."""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from app.models.nytimes import (
    ArticleSearchQueryParams,
    ArticleSearchResponse,
    TopStoryResponse,
)
from app.services.nyt_client import fetch_article_search, fetch_top_stories

router = APIRouter()


@router.get("/topstories", response_model=List[TopStoryResponse], tags=["NYTimes"])
async def get_top_stories() -> List[TopStoryResponse]:
    """Get the two most recent top stories from each category."""
    try:
        return await fetch_top_stories()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@router.get(
    "/articlesearch", response_model=List[ArticleSearchResponse], tags=["NYTimes"]
)
async def get_article_search(
    q: str = Query(..., description="Search query string"),
    begin_date: Optional[str] = Query(
        None, description="Start date in YYYYMMDD format"
    ),
    end_date: Optional[str] = Query(None, description="End date in YYYYMMDD format"),
) -> List[ArticleSearchResponse]:
    """Search NYTimes articles by keyword and optional date range."""
    params = ArticleSearchQueryParams(q=q, begin_date=begin_date, end_date=end_date)
    try:
        return await fetch_article_search(params)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
