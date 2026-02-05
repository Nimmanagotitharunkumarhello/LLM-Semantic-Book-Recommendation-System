"use client"

import { useState, useEffect, useCallback } from "react";
import { searchBooks } from "@/lib/api";
import { Book } from "@/lib/types";
import SearchBar from "@/components/SearchBar";
import MoodFilter from "@/components/MoodFilter";
import BookGrid from "@/components/BookGrid";
import { ThemeToggle } from "@/components/ThemeToggle";
import BookModal from "@/components/BookModal";
import { BookOpen } from "lucide-react";

export default function Home() {
  const [books, setBooks] = useState<Book[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [mood, setMood] = useState<string | undefined>(undefined);
  const [lastQuery, setLastQuery] = useState("");
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);

  // Consolidated search function to avoid duplication and race conditions
  const performSearch = useCallback(async (query: string, filterMood: string | undefined) => {
    setIsLoading(true);

    // Fallback logic: if no query, try to use mood as query, or default to "stories"
    let effectiveQuery = query.trim();
    if (!effectiveQuery && filterMood) {
      effectiveQuery = `books about ${filterMood}`;
    } else if (!effectiveQuery && !filterMood) {
      // Just clear if literally nothing
      setBooks([]);
      setIsLoading(false);
      return;
    }

    try {
      const data = await searchBooks(effectiveQuery, filterMood);
      setBooks(data.results);
    } catch (error) {
      console.error("Search error:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  // Initial Load
  useEffect(() => {
    performSearch("stories", undefined);
  }, [performSearch]);

  const handleSearch = useCallback((query: string) => {
    setLastQuery(query);
    performSearch(query, mood);
  }, [mood, performSearch]);

  const handleMoodChange = useCallback((newMood: string | undefined) => {
    setMood(newMood);
    // If we have a query, keep it. If not, the performSearch logic handles it.
    performSearch(lastQuery, newMood);
  }, [lastQuery, performSearch]);

  return (
    <main className="flex flex-col min-h-screen relative overflow-hidden bg-gray-50 dark:bg-slate-950 transition-colors duration-300">
      {/* Background Decor */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[500px] bg-purple-500/20 rounded-full blur-[120px] -z-10 pointer-events-none opacity-50 dark:opacity-20 animate-pulse"></div>

      <header className="w-full max-w-7xl mx-auto p-6 flex justify-between items-center z-10 sticky top-0 bg-white/80 dark:bg-slate-950/80 backdrop-blur-md border-b border-gray-200 dark:border-gray-800">
        <div className="flex items-center gap-2 font-bold text-2xl text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-blue-500 cursor-pointer" onClick={() => window.location.reload()}>
          <BookOpen className="text-purple-600 dark:text-purple-400" />
          <span>BookFinder.ai</span>
        </div>
        <ThemeToggle />
      </header>

      <div className="flex-1 w-full max-w-7xl mx-auto px-6 pb-20 flex flex-col items-center gap-8 mt-8">

        {/* Hero Section */}
        <div className="text-center space-y-4 pt-4 pb-6 max-w-3xl">
          <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-900 dark:text-white leading-tight">
            Find your next favorite story <span className="text-purple-600 dark:text-purple-400">instantly</span>.
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">
            AI-powered semantic search that understands plot, vibe, and character.
          </p>
        </div>

        {/* Search & Filter */}
        <div className="w-full flex flex-col items-center gap-6 z-20">
          <SearchBar onSearch={handleSearch} isSearching={isLoading} />

          <div className="flex flex-wrap items-center justify-center gap-3 text-sm text-gray-500 w-full">
            <span className="font-medium">Filter by mood:</span>
            <MoodFilter selectedMood={mood} onSelectMood={handleMoodChange} />
          </div>
        </div>

        {/* Results Area */}
        <div className="w-full pt-8 min-h-[500px]">
          <div className="flex items-end justify-between mb-8 border-b border-gray-200 dark:border-gray-800 pb-4">
            <div>
              <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                {lastQuery ? `Results for "${lastQuery}"` : "Recommended for You"}
              </h2>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                {isLoading ? "Curating best matches..." : `Found ${books.length} books matching your criteria`}
              </p>
            </div>

            {mood && (
              <span className="bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 px-3 py-1 rounded-full text-xs font-bold border border-purple-200 dark:border-purple-800">
                {mood.toUpperCase()}
              </span>
            )}
          </div>

          <BookGrid
            books={books}
            isLoading={isLoading}
            onSelectBook={setSelectedBook}
          />
        </div>

      </div>

      {/* Detail Modal */}
      <BookModal
        book={selectedBook}
        onClose={() => setSelectedBook(null)}
      />
    </main>
  );
}
