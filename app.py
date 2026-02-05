import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# --- Configuration ---
st.set_page_config(page_title="AI Book Recommender", page_icon="📚", layout="wide")

# --- Constants & Utilities (Embedded from backend/api/utils.py) ---
MOOD_KEYWORDS = {
    "joyful": ["joy", "happy", "happiness", "smile", "laugh", "fun", "delight", "cheerful", "light", "bright"],
    "sad": ["sad", "grief", "sorrow", "tear", "cry", "loss", "death", "mourn", "tragedy", "broken"],
    "suspenseful": ["suspense", "secret", "hide", "hiding", "mystery", "threat", "tension", "wait", "fear"],
    "romantic": ["love", "romance", "heart", "kiss", "marriage", "passion", "relationship", "lover", "couple"],
    "dark": ["dark", "evil", "kill", "murder", "blood", "horror", "death", "grim", "shadow", "violence"],
    "adventurous": ["adventure", "journey", "quest", "travel", "explore", "wild", "expedition", "hidden", "discovery"],
    "funny": ["funny", "humor", "comedy", "laugh", "joke", "hilarious", "wit", "sarcasm", "amusing"],
    "inspirational": ["inspire", "hope", "faith", "dream", "life", "wisdom", "courage", "strength", "soul", "god"],
    "thriller": ["thriller", "killer", "suspense", "danger", "psychological", "crime", "hunt", "chase"],
    "mystery": ["mystery", "detective", "clue", "solve", "crime", "strange", "unexplained", "hidden", "secret"],
    "educational": ["learn", "guide", "textbook", "study", "history", "science", "academic", "theory", "introduction"],
    "technical": ["software", "code", "programming", "data", "computer", "algorithm", "system", "guide", "engineering"]
}

def classify_moods_jit(descriptions: list):
    """Classify a list of descriptions using fast keyword matching."""
    results = []
    for text in descriptions:
        text_lower = str(text).lower()
        scores = {}
        for mood, keywords in MOOD_KEYWORDS.items():
            score = 0
            for word in keywords:
                if word in text_lower:
                    score += 0.3
            if score > 0.9: score = 0.95
            scores[mood] = score
        results.append(scores)
    return results

# --- App Logic ---
st.title("📚 AI-Powered Book Recommendation System")
st.markdown("Find your next favorite book using semantic search! Powered by **Sentence Transformers** and **FAISS**.")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_data():
    # Paths are relative to root because script is at root
    data_dir = os.path.join("backend", "data")
    csv_path = os.path.join(data_dir, "books_metadata.csv") # Using metadata csv which is smaller and cleaner
    index_path = os.path.join(data_dir, "faiss.index")
    
    # 1. Check Data
    if not os.path.exists(csv_path):
        st.error(f"Data file not found at {csv_path}. Please run backend/data_pipeline/download_data.py")
        return None, None
        
    df = pd.read_csv(csv_path).fillna("")
    
    # 2. Check Index
    if not os.path.exists(index_path):
        st.warning("FAISS index not found. Generating now... (This helps search speed)")
        # In a real deployed app, you'd want to pre-generate this. 
        # For this demo script, we might fail if index is missing to save time/memory on small cloud instances.
        st.error("Index missing. Please run the generation script locally and push the 'backend/data/faiss.index' file.")
        return None, None

    index = faiss.read_index(index_path)
    
    return df, index

model = load_model()
df, index = load_data()

if df is not None and index is not None:
    # --- Sidebar ---
    st.sidebar.header("🎯 Filters")
    mood_options = ["All"] + sorted(list(MOOD_KEYWORDS.keys()))
    selected_mood = st.sidebar.selectbox("Select Mood", mood_options).lower()
    
    min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, 0.1)
    top_k = st.sidebar.slider("Number of Results", 5, 50, 10)

    # --- Main Search ---
    query = st.text_input("🔍 Describe the book you're looking for", placeholder="e.g., 'space opera with aliens' or 'overcoming grief'")

    if st.button("Search", type="primary") or query:
        if query:
            with st.spinner("Finding perfect books for you..."):
                # 1. Vector Search
                query_embedding = model.encode([query])
                faiss.normalize_L2(query_embedding) # Normalize for cosine similarity equivalent
                distances, indices = index.search(query_embedding, top_k * 2) # Fetch extra for filtering
                
                # 2. Get Candidates
                found_indices = indices[0]
                found_distances = distances[0]
                
                results = []
                descriptions_to_classify = []
                
                for i, idx in enumerate(found_indices):
                    if idx == -1: continue
                    row = df.iloc[idx].to_dict()
                    row['similarity'] = float(found_distances[i])
                    results.append(row)
                    descriptions_to_classify.append(row.get('description', ''))
                
                # 3. Mood Analysis & Filtering
                mood_scores = classify_moods_jit(descriptions_to_classify)
                final_results = []
                
                for i, row in enumerate(results):
                    book_moods = mood_scores[i]
                    
                    # Apply Mood Filter
                    if selected_mood != "all":
                        # Logic: Mood must be present with decent score
                        if book_moods.get(selected_mood, 0) < 0.3:
                            continue
                            
                    # Apply Rating Filter
                    if float(row.get('average_rating', 0)) < min_rating:
                        continue
                        
                    final_results.append(row)
                
                # Limit to top_k
                final_results = final_results[:top_k]
                
                st.success(f"Found {len(final_results)} books!")
                
                # 4. Display
                for row in final_results:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if row.get('thumbnail'):
                            st.image(row['thumbnail'], width=100)
                        else:
                            st.image("https://via.placeholder.com/100x150?text=No+Cover", width=100)
                    with col2:
                        st.markdown(f"### {row.get('title', 'Unknown')}")
                        authors = row.get('authors', 'Unknown')
                        st.markdown(f"**Author:** {authors}")
                        
                        rating = float(row.get('average_rating', 0))
                        sim = row['similarity']
                        st.markdown(f"⭐ {rating:.1f}/5.0 | 🎯 Match Score: {sim:.2f}")
                        
                        desc = row.get('description', 'No description available.')
                        with st.expander("📖 Read Description"):
                            st.write(desc)
                    st.divider()

        else:
            st.info("👆 Enter a search query to find books!")

    st.sidebar.markdown("---")
    st.sidebar.info("This app uses AI to find books based on semantic similarity. Powered by Sentence Transformers and FAISS.")
