"""import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os
import subprocess

st.set_page_config(page_title="AI Book Recommender", page_icon="📚", layout="wide")

st.title("📚 AI-Powered Book Recommendation System")
st.markdown("Find your next favorite book using semantic search!")

@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_data():
    # Download data if needed
    if not os.path.exists('backend/data/books.csv'):
        st.info("📥 Downloading dataset... (first time only)")
        try:
            subprocess.run(['python', 'backend/data_pipeline/download_data.py'], check=True)
        except Exception as e:
            st.error(f"Error downloading data: {e}")
            return None, None
    
    # Load books data
    df = pd.read_csv('backend/data/books.csv')
    
    # Generate embeddings if needed
    if not os.path.exists('backend/data/faiss.index'):
        st.info("🔄 Generating embeddings... This will take ~10 minutes (first time only)")
        try:
            subprocess.run(['python', 'backend/data_pipeline/generate_embeddings.py'], check=True)
        except Exception as e:
            st.error(f"Error generating embeddings: {e}")
            return df, None
    
    # Load embeddings and index
    try:
        index = faiss.read_index('backend/data/faiss.index')
        # embeddings = np.load('backend/data/book_embeddings.npy') # Not used/needed
    except Exception as e:
        st.error(f"Error loading index: {e}")
        return df, None
    
    return df, index

# Load everything
model = load_model()
df, index = load_data()

# Check if data loaded successfully
if df is None or index is None:
    st.error("❌ Failed to load data. Please check the logs.")
    st.stop()

st.sidebar.header("🎯 Filters")
moods = ["All", "Joyful", "Dark", "Suspenseful", "Romantic", "Thought-provoking"]
selected_mood = st.sidebar.selectbox("Select Mood", moods)
min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, 0.1)
top_k = st.sidebar.slider("Number of Results", 5, 50, 10)

query = st.text_input("🔍 Describe the book you're looking for", placeholder="e.g., 'space opera with aliens'")

if st.button("Search", type="primary") or query:
    if query:
        with st.spinner("Finding perfect books for you..."):
            query_embedding = model.encode([query])
            distances, indices = index.search(query_embedding, top_k * 2)
            results = df.iloc[indices[0]].copy()
            results['similarity'] = 1 - distances[0]
            
            if selected_mood != "All" and 'mood' in results.columns:
                results = results[results['mood'] == selected_mood]
            if 'rating' in results.columns:
                results = results[results['rating'] >= min_rating]
            
            results = results.head(top_k)
            st.success(f"Found {len(results)} books!")
            
            for idx, row in results.iterrows():
                col1, col2 = st.columns([1, 4])
                with col1:
                    if 'image' in row and pd.notna(row['image']):
                        st.image(row['image'], width=120)
                    else:
                        st.image("https://via.placeholder.com/120x180?text=No+Cover", width=120)
                with col2:
                    st.markdown(f"### {row.get('title', 'Unknown')}")
                    st.markdown(f"**Author:** {row.get('authors', 'Unknown')}")
                    st.markdown(f"⭐ {row.get('rating', 0):.1f}/5.0 | 🎯 {row['similarity']*100:.1f}%")
                    if 'description' in row and pd.notna(row['description']):
                        with st.expander("📖 Description"):
                            st.write(row['description'])
                st.divider()
    else:
        st.info("👆 Enter a search query to find books!")

st.sidebar.markdown("---")
st.sidebar.info("This app uses AI to find books based on semantic similarity. Powered by Sentence Transformers and FAISS.")"""