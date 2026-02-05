import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import json
import pickle

def generate_embeddings():
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    csv_path = os.path.join(data_dir, "books.csv")
    
    if not os.path.exists(csv_path):
        print("books.csv not found. Please run download_data.py first.")
        return

    print("Loading data...")
    df = pd.read_csv(csv_path)
    
    # Data Cleaning
    print(f"Initial shape: {df.shape}")
    df = df.dropna(subset=['description', 'title', 'authors'])
    df = df.reset_index(drop=True)
    print(f"Shape after cleaning: {df.shape}")
    
    # Generate Embeddings
    print("Loading SentenceTransformer model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Generating embeddings (this may take a while)...")
    descriptions = df['description'].tolist()
    embeddings = model.encode(descriptions, show_progress_bar=True)
    
    # Normalize embeddings for cosine similarity (if using Inner Product) or just use L2
    # FAISS IndexFlatL2 uses Euclidean distance. 
    # For semantic search, Cosine Similarity is often preferred. 
    # With normalized vectors, L2 distance is equivalent to Cosine Similarity.
    # L2 = 2 - 2 * DotProduct. So we can usage IndexFlatL2 with normalized vectors.
    print("Normalizing embeddings...")
    faiss.normalize_L2(embeddings)
    
    # Create FAISS Index
    print("Creating FAISS index...")
    d = embeddings.shape[1]  # Dimension (384 for all-MiniLM-L6-v2)
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    
    print(f"Index contains {index.ntotal} vectors")
    
    # Save artifacts
    index_path = os.path.join(data_dir, "faiss.index")
    metadata_path = os.path.join(data_dir, "books_metadata.csv") # Using CSV for simplicity with Pandas
    
    print(f"Saving index to {index_path}...")
    faiss.write_index(index, index_path)
    
    print(f"Saving metadata to {metadata_path}...")
    # Save only necessary columns for the API to load quickly
    clean_df = df[['isbn13', 'isbn10', 'title', 'subtitle', 'authors', 'categories', 'thumbnail', 'description', 'published_year', 'average_rating', 'num_pages', 'ratings_count']]
    clean_df.to_csv(metadata_path, index=False)
    
    print("Done!")

if __name__ == "__main__":
    generate_embeddings()
