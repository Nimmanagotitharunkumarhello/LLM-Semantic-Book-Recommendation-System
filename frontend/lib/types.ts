export interface Book {
    isbn13: string;
    title: string;
    authors: string;
    description: string;
    thumbnail: string;
    categories: string;
    published_year: number;
    average_rating: number;
    moods?: Record<string, number>;
    similarity_score?: number;
}

export interface SearchResponse {
    results: Book[];
    total: number;
    query_time: number;
}

export type Mood = "joyful" | "sad" | "suspenseful" | "romantic" | "dark" | "adventurous" | "funny" | "inspirational" | "thriller" | "mystery" | "educational" | "technical";
