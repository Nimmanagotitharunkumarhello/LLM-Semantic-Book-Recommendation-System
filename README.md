# Semantic Book Recommendation System

A full-stack AI-powered book recommendation engine that matches books to your mood and natural language queries using semantic search (FAISS + Sentence Transformers).

## Features
- **Semantic Search**: Find books by describing plots, vibes, or characters (e.g., "space opera with aliens").
- **Mood Filtering**: Filter results by moods like "Joyful", "Dark", "Suspenseful".
- **Modern UI**: Response Next.js 14 application with Tailwind CSS, dark mode, and glassmorphism design.
- **Fast Performance**: Vector search using FAISS retrieves results in milliseconds.

## Tech Stack
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.11+, FastAPI, Sentencetransformers, FAISS, Pandas
- **Data**: Kaggle 7k Books Dataset (Automatically downloaded)

## Setup Instructions

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

### 2. Data Pipeline
Download the dataset and generate embeddings (this takes ~10-15 minutes on first run):

```bash
python data_pipeline/download_data.py
python data_pipeline/generate_embeddings.py
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

### 4. Running the Application

**Start Backend API**
```bash
# In backend/ directory
uvicorn api.main:app --reload --port 8000
```

**Start Frontend**
```bash
# In frontend/ directory
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000) to start discovering books!

## Project Structure
- `backend/data_pipeline/`: Scripts for data processing.
- `backend/api/`: FastAPI application source.
- `frontend/app/`: Next.js App Router pages.
- `frontend/components/`: Reusable UI components.

## License
MIT
