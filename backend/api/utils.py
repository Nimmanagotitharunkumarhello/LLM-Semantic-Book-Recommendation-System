import re

CANDIDATE_LABELS = [
    "joyful", "sad", "suspenseful", "romantic", 
    "dark", "adventurous", "funny", "inspirational",
    "thriller", "mystery", "educational", "technical"
]

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
    """
    Classify a list of descriptions using fast keyword matching.
    """
    results = []
    
    for text in descriptions:
        text_lower = text.lower()
        scores = {}
        for mood, keywords in MOOD_KEYWORDS.items():
            score = 0
            for word in keywords:
                if word in text_lower:
                    score += 0.3 # Simple keyword presence score
            
            # Normalize reasonably
            if score > 0.9: score = 0.95
            scores[mood] = score
            
        results.append(scores)
        
    return results

def get_moods():
    return CANDIDATE_LABELS
