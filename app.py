import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import os

# Page config
st.set_page_config(
    page_title="AI Book Recommender",
    page_icon="📚",
    layout="wide"
)

# Title
st.title("📚 AI-Powered Book Recommendation System")
st.markdown("Find your next favorite book using semantic search!")

# Cache the model and data
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_data
def load_data():
    # Check if data exists, if not download
    if not os.path.exists('backend/data/books.csv'):
        st.info("Downloading dataset for the first time... This may take a moment.")
        import subprocess
        subprocess.run(['python', 'backend/data_pipeline/download_data.py'])
    
    df = pd.read_csv('backend/data/books.csv')
    
    # Load or generate embeddings
    if os.path.exists('backend/data/faiss_index.bin'):
        index = faiss.read_index('backend/data/faiss_index.bin')
        embeddings = np.load('backend/data/book_embeddings.npy')
    else:
        st.info("Generating embeddings for the first time... This will take ~10 minutes.")
        import subprocess
        subprocess.run(['python', 'backend/data_pipeline/generate_embeddings.py'])
        index = faiss.read_index('backend/data/faiss_index.bin')
        embeddings = np.load('backend/data/book_embeddings.npy')
    
    return df, index, embeddings

# Load everything
model = load_model()
df, index, embeddings = load_data()

# Sidebar filters
st.sidebar.header("🎯 Filters")
moods = ["All", "Joyful", "Dark", "Suspenseful", "Romantic", "Thought-provoking"]
selected_mood = st.sidebar.selectbox("Select Mood", moods)

min_rating = st.sidebar.slider("Minimum Rating", 0.0, 5.0, 3.5, 0.1)
top_k = st.sidebar.slider("Number of Results", 5, 50, 10)

# Search box
query = st.text_input(
    "🔍 Describe the book you're looking for",
    placeholder="e.g., 'space opera with aliens and political intrigue'"
)

# Search button
if st.button("Search", type="primary") or query:
    if query:
        with st.spinner("Finding perfect books for you..."):
            # Generate query embedding
            query_embedding = model.encode([query])
            
            # Search FAISS
            distances, indices = index.search(query_embedding, top_k * 2)
            
            # Get results
            results = df.iloc[indices[0]].copy()
            results['similarity'] = 1 - distances[0]  # Convert distance to similarity
            
            # Apply filters
            if selected_mood != "All" and 'mood' in results.columns:
                results = results[results['mood'] == selected_mood]
            
            if 'rating' in results.columns:
                results = results[results['rating'] >= min_rating]
            
            results = results.head(top_k)
            
            # Display results
            st.success(f"Found {len(results)} books matching your search!")
            
            for idx, row in results.iterrows():
                with st.container():
                    col1, col2 = st.columns([1, 4])
                    
                    with col1:
                        if 'image' in row and pd.notna(row['image']):
                            st.image(row['image'], width=120)
                        else:
                            st.image("https://via.placeholder.com/120x180?text=No+Cover", width=120)
                    
                    with col2:
                        title = row.get('title', 'Unknown Title')
                        author = row.get('authors', 'Unknown Author')
                        rating = row.get('rating', 0)
                        similarity = row['similarity'] * 100
                        
                        st.markdown(f"### {title}")
                        st.markdown(f"**Author:** {author}")
                        st.markdown(f"⭐ **Rating:** {rating:.1f}/5.0 | 🎯 **Match:** {similarity:.1f}%")
                        
                        if 'description' in row and pd.notna(row['description']):
                            with st.expander("📖 Description"):
                                st.write(row['description'])
                    
                    st.divider()
    else:
        st.info("👆 Enter a search query to find books!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "This app uses AI to find books based on semantic similarity. "
    "Powered by Sentence Transformers and FAISS."
)