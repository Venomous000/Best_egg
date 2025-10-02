from unittest.mock import patch, AsyncMock

import httpx
import pytest
import respx
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app

NYT_BASE_URL = "https://api.nytimes.com/svc"


@pytest.mark.asyncio
@respx.mock
async def test_get_topstories_success():
    categories = ["arts", "food", "movies", "travel", "science"]
    mock_response = {
        "status": "OK",
        "results": [
            {
                "title": "Sample Title",
                "abstract": "Summary here",
                "url": "https://example.com",
                "byline": "By Author",
                "published_date": "2023-01-01",
            }
        ],
    }

    # Mock each category endpoint
    for cat in categories:
        respx.get(f"{NYT_BASE_URL}/topstories/v2/{cat}.json").mock(
            return_value=httpx.Response(200, json=mock_response)
        )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nytimes/topstories")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["title"] == "Sample Title"


@pytest.mark.asyncio
@respx.mock
async def test_get_articlesearch_success():
    mock_response = {
        "status": "OK",
        "response": {
            "docs": [
                {
                    "headline": {"main": "Sample Article"},
                    "snippet": "This is a snippet.",
                    "web_url": "https://example.com",
                    "byline": {"original": "By Someone"},
                    "pub_date": "2023-01-01T00:00:00Z",
                }
            ]
        },
    }

    respx.get(f"{NYT_BASE_URL}/search/v2/articlesearch.json").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nytimes/articlesearch?q=sample")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["headline"] == "Sample Article"
        assert "snippet" in data[0]


@pytest.mark.asyncio
async def test_articlesearch_missing_query_param():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nytimes/articlesearch")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


client = TestClient(app)


def test_health_check():
    response = client.get("/docs")  # Assuming /api/v1/health doesn't exist
    assert response.status_code == 200


@pytest.mark.asyncio
@patch("app.services.nyt_client.httpx.AsyncClient.get", new_callable=AsyncMock)
async def test_rate_limit_retry_exhausted(mock_get):
    mock_response = httpx.Response(
        429,
        json={"detail": "Rate limit exceeded"},
        request=httpx.Request("GET", "http://test")
    )
    mock_get.return_value = mock_response

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/nytimes/topstories")
        assert response.status_code == 429
        assert response.json()["detail"] == "Rate limit exceeded"
