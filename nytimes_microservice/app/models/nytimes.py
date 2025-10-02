"""Pydantic models for NYTimes API responses and queries."""

from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class TopStoryResponse(BaseModel):
    """Model for a single Top Story result."""

    title: str
    section: str
    url: HttpUrl
    abstract: str
    published_date: str


class ArticleSearchResponse(BaseModel):
    """Model for a single Article Search result."""

    headline: str
    snippet: str
    web_url: HttpUrl
    pub_date: str


class ArticleSearchQueryParams(BaseModel):
    """Model for article search query parameters."""

    q: str
    begin_date: Optional[str] = None
    end_date: Optional[str] = None
