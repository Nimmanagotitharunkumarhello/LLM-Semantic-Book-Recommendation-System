import { SearchResponse, Book } from './types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function searchBooks(query: string, mood?: string): Promise<SearchResponse> {
    const res = await fetch(`${API_URL}/api/search`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // body: JSON.stringify({ query, mood }),
        body: JSON.stringify({ query, mood, top_k: 50 }),
    });

    if (!res.ok) {
        throw new Error('Failed to fetch books');
    }

    return res.json();
}
