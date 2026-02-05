from pydantic import BaseModel
from typing import List, Optional, Dict

class Book(BaseModel):
    isbn13: Optional[str] = None
    title: str
    authors: Optional[str] = None
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    categories: Optional[str] = None
    published_year: Optional[float] = None
    average_rating: Optional[float] = None
    moods: Optional[Dict[str, float]] = None # Mood scores
    similarity_score: Optional[float] = None # For search results

class SearchRequest(BaseModel):
    query: str
    top_k: int = 41
    mood: Optional[str] = None # Optional filter

class SearchResponse(BaseModel):
    results: List[Book]
    total: int
    query_time: float

class FilterRequest(BaseModel):
    mood: Optional[str] = None
    page: int = 1
    limit: int = 20
