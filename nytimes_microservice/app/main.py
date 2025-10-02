"""Main FastAPI entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.nytimes import router as nytimes_router

app = FastAPI(
    title="NYTimes Article Microservice",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Optional CORS middleware (safe default config)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check route
@app.get("/", tags=["Health"])
async def root():
    return {"message": "NYTimes Microservice is running."}


# Include NYTimes API routes
app.include_router(nytimes_router, prefix="/nytimes")
