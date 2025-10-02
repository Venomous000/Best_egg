#📰 NYTimes Top Stories Microservice
A FastAPI-based microservice to fetch the latest Top Stories from the New York Times API across multiple categories.

##Features
Top Stories API: /api/v1/topstories — Retrieves the two most recent top stories from each of: arts, food, movies, travel, science
Health Check: /api/v1/health — Simple endpoint to check API status
Caching: Built-in lru_cache for optimized repeated requests
Resilience: Automatic retry with exponential backoff for rate-limiting (HTTP 429)
Testing: Comprehensive unit tests using pytest
Clean Code: Fully PEP8-compliant and lint-clean

##Getting Started
1. Clone the Repository
git clone <repo-url>
cd nytimes_microservice


2. Create and Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Set Environment Variables
You'll need an NYTimes API Key. Set it as an environment variable:
export NYT_API_KEY=your-nyt-api-key


For Windows (PowerShell):
$env:NYT_API_KEY="your-nyt-api-key"

##Running the Application

Start the FastAPI server:
uvicorn app.main:app --reload

API docs will be available at: http://localhost:8000/docs

## Running Tests
pytest
All tests are located under the tests/ directory.

##Project Structure
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
│   └── main.py                # App entrypoint
│
├── tests/
│   └── test_nytimes.py        # Unit tests
│
├── requirements.txt
└── README.md