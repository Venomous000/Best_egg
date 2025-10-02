# 📰 NYTimes Top Stories Microservice

A FastAPI-based microservice to fetch the latest Top Stories from the New York Times API across multiple categories.

## Features

- **Top Stories API**: `/nytimes/topstories` — Retrieves the two most recent top stories from each of: arts, food, movies, travel, science
- **Article Search API**: `/nytimes/articlesearch` — Search articles by keyword with optional date filtering
- **Health Check**: `/nytimes/health` — Simple endpoint to check API status
- **Caching**: Built-in lru_cache for optimized repeated requests
- **Resilience**: Automatic retry with exponential backoff for rate-limiting (HTTP 429)
- **Testing**: Comprehensive unit tests using pytest
- **Clean Code**: Fully PEP8-compliant and lint-clean

## Getting Started

### 1. Clone the Repository

```bash
git clone <repo-url>
cd nytimes_microservice
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

You'll need an NYTimes API Key. Set it as an environment variable:

**Linux/Mac:**
```bash
export NYT_API_KEY=your-nyt-api-key
```

**Windows (PowerShell):**
```powershell
$env:NYT_API_KEY="your-nyt-api-key"
```

## Running the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

API docs will be available at: http://localhost:8000/docs

## API Endpoints

### Top Stories
- **GET** `/nytimes/topstories`
- Returns the two most recent top stories from each category (arts, food, movies, travel, science)
- Response includes: title, section, url, abstract, published_date

### Article Search
- **GET** `/nytimes/articlesearch`
- Search articles by keyword with optional date filtering
- Query parameters:
  - `q` (required): Search query string
  - `begin_date` (optional): Start date in YYYYMMDD format
  - `end_date` (optional): End date in YYYYMMDD format
- Response includes: headline, snippet, web_url, pub_date

### Health Check
- **GET** `/nytimes/health`
- Simple health status endpoint

## Running Tests

```bash
pytest
```

All tests are located under the `tests/` directory.

## Project Structure

```
nytimes_microservice/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── nytimes.py     # API routes
│   ├── models/
│   │   └── nytimes.py         # Response models
│   ├── services/
│   │   └── nyt_client.py      # NYTimes fetch + retry logic
│   ├── core/
│   │   └── settings.py        # Configuration settings
│   ├── utils/
│   │   ├── error_handler.py   # Error handling utilities
│   │   └── logger.py          # Logging configuration
│   └── main.py                # App entrypoint
│
├── tests/
│   ├── test_nytimes.py        # Unit tests
│   └── test_api.py            # API tests
│
├── requirements.txt
├── pyproject.toml
├── .env.example
└── README.md
```

## Development

The project uses:
- **FastAPI** for the web framework
- **Pydantic** for data validation
- **httpx** for async HTTP requests
- **pytest** for testing
- **Black** and **isort** for code formatting
- **Pylint** for linting

## Environment Variables

Copy `.env.example` to `.env` and set your NYTimes API key:

```bash
cp .env.example .env
```

Then edit the `.env` file:

```
NYT_API_KEY=your-nyt-api-key
```

## Requirements Compliance

This microservice fully meets all specified requirements:

### API Key Setup
- NYTimes Developer API key integration
- Environment variable configuration

### Microservice Implementation
- FastAPI framework with clean project structure
- Pydantic models for request/response validation

### Required Endpoints
- `/nytimes/topstories` - Top Stories API integration
- `/nytimes/articlesearch` - Article Search API integration
- All required response fields included

### Documentation and Testing
- Auto-generated OpenAPI/Swagger docs at `/docs`
- Comprehensive unit tests with pytest
- Both success and error case coverage

## Additional Features

- **Retry Logic**: Exponential backoff for rate limiting
- **Error Handling**: Comprehensive error management
- **Logging**: Structured logging throughout
- **Type Safety**: Full type hints
- **CORS Support**: Cross-origin request handling
- **Async Performance**: Non-blocking HTTP requests
