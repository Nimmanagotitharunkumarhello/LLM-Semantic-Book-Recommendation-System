from transformers import pipeline
import pandas as pd
import os
import json

# Define the candidate labels for mood classification
CANDIDATE_LABELS = [
    "joyful", "sad", "suspenseful", "romantic", 
    "dark", "adventurous", "funny", "inspirational"
]

def classify_moods_batch(texts, batch_size=8):
    """
    Classify a batch of texts into moods using zero-shot classification.
    Returns a list of dictionaries with scores for each mood.
    """
    classifier = pipeline("zero-shot-classification", 
                         model="facebook/bart-large-mnli", 
                         device=-1) # -1 for CPU, 0 for GPU if available via PyTorch check
    
    results = classifier(texts, candidate_labels=CANDIDATE_LABELS, multi_label=True)
    
    # Format results
    processed_results = []
    for res in results:
        scores = {label: score for label, score in zip(res['labels'], res['scores'])}
        # Filter by threshold if needed here, or return raw scores
        processed_results.append(scores)
        
    return processed_results

if __name__ == "__main__":
    # Test run on a few books
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    csv_path = os.path.join(data_dir, "books.csv")
    
    if os.path.exists(csv_path):
        print("Loading first 5 books for test classification...")
        df = pd.read_csv(csv_path).head(5)
        descriptions = df['description'].fillna("").tolist()
        
        print("Classifying...")
        moods = classify_moods_batch(descriptions)
        
        for i, mood in enumerate(moods):
            print(f"\nBook: {df.iloc[i]['title']}")
            top_mood = max(mood, key=mood.get)
            print(f"Top Mood: {top_mood} ({mood[top_mood]:.2f})")
    else:
        print("Data not found.")
