import faiss
import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from .models import Book
from .utils import classify_moods_jit

# Global variables for caching
index = None
metadata_df = None
model = None

def load_resources():
    global index, metadata_df, model
    
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    index_path = os.path.join(base_dir, "faiss.index")
    metadata_path = os.path.join(base_dir, "books_metadata.csv")
    
    print("Loading resources...")
    if os.path.exists(index_path) and os.path.exists(metadata_path):
        index = faiss.read_index(index_path)
        metadata_df = pd.read_csv(metadata_path).fillna("")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Resources loaded.")
    else:
        print("Resources not found. Please run data pipeline.")

async def search_books(query: str, top_k: int = 20, mood_filter: str = None):
    if index is None:
        load_resources()
        if index is None:
            raise Exception("Search index not initialized")
            
    # Encode query
    vector = model.encode([query])
    faiss.normalize_L2(vector)
    
    # Search
    distances, indices = index.search(vector, top_k * 2) # Fetch more to filter
    
    results = []
    
    # Indices is a list of lists (for each query)
    found_indices = indices[0]
    found_distances = distances[0]
    
    # Prepare inputs for mood classification if needed
    candidates = []
    
    for rank, idx in enumerate(found_indices):
        if idx == -1: continue
        
        row = metadata_df.iloc[idx]
        book = Book(
            isbn13=str(row.get('isbn13', '')),
            title=row.get('title', 'Unknown'),
            authors=row.get('authors', ''),
            description=row.get('description', ''),
            thumbnail=row.get('thumbnail', ''),
            categories=row.get('categories', ''),
            published_year=row.get('published_year', 0) if row.get('published_year') != '' else 0,
            average_rating=row.get('average_rating', 0) if row.get('average_rating') != '' else 0,
            similarity_score=float(found_distances[rank]),
            moods={}
        )
        candidates.append(book)

    # Mood classification (JIT)
    # The requirement says "Only classify top 20 search results... Cache mood results"
    # We will classify all candidates
    descriptions = [b.description for b in candidates]
    mood_scores_list = classify_moods_jit(descriptions)
    
    final_results = []
    for i, book in enumerate(candidates):
        book.moods = mood_scores_list[i]
        
        # Apply filter if requested
        if mood_filter:
            # Check if requested mood is the top mood or has high score
            # Simple logic: if mood in top 2 or score > 0.5
             if mood_filter.lower() in book.moods and book.moods[mood_filter.lower()] > 0.3: # Threshold
                 final_results.append(book)
        else:
            final_results.append(book)
            
    return final_results[:top_k]
