from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import SearchRequest, SearchResponse, FilterRequest
from .search import search_books, load_resources
from .utils import get_moods
import time

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load resources on startup
    print("Loading resources on startup...")
    load_resources()
    print("Resources ready.")
    yield

app = FastAPI(title="Semantic Book Recommender", lifespan=lifespan)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Semantic Book Recommender API"}

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    start_time = time.time()
    try:
        results = await search_books(request.query, request.top_k, request.mood)
        duration = time.time() - start_time
        return {
            "results": results,
            "total": len(results),
            "query_time": duration
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/filter")
# Placeholder for filter endpoint - strictly speaking, this might need more logic
# if filtering *without* a query.
async def filter_books(request: FilterRequest):
    # For now, just return empty or implement basic filtering if time permits.
    # The user requirements asked for "Filter results by mood".
    # If this is independent of search, we need a way to list books by mood.
    # This might require pre-computed mood tags.
    return {"message": "Filter endpoint under construction"}

@app.get("/api/moods")
def list_moods():
    return {"moods": get_moods()}

@app.get("/api/stats")
def get_stats():
    # Load stats from metadata or index
    return {"message": "Stats endpoint"}
