import { Book } from "@/lib/types";
import Image from "next/image";
import { useState } from "react";
import { Sparkles, BookOpen } from "lucide-react";

interface BookCardProps {
    book: Book;
    onSelect: (book: Book) => void;
}

export default function BookCard({ book, onSelect }: BookCardProps) {
    const [imageError, setImageError] = useState(false);

    // Get top mood
    const topMood = book.moods
        ? Object.entries(book.moods).reduce((a, b) => a[1] > b[1] ? a : b)[0]
        : null;

    return (
        <div
            onClick={() => onSelect(book)}
            className="group relative flex flex-col h-full bg-white dark:bg-slate-800 rounded-xl shadow-sm hover:shadow-xl transition-all duration-300 p-4 border border-gray-100 dark:border-gray-800 hover:border-purple-200 dark:hover:border-purple-900 cursor-pointer transform hover:-translate-y-1"
        >
            {/* Image Section */}
            <div className="relative w-full aspect-[2/3] mb-4 bg-gray-50 dark:bg-slate-700/30 rounded-lg overflow-hidden">
                {book.thumbnail && !imageError ? (
                    <Image
                        src={book.thumbnail}
                        alt={book.title}
                        fill
                        className="object-cover transition-transform duration-700 group-hover:scale-110"
                        sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
                        onError={() => setImageError(true)}
                    />
                ) : (
                    <div className="flex h-full w-full items-center justify-center text-gray-400">
                        <BookOpen size={40} strokeWidth={1.5} />
                    </div>
                )}

                {/* Overlay Gradient */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

                {/* Mood Badge */}
                {topMood && (
                    <div className="absolute top-2 right-2 bg-white/90 dark:bg-slate-900/90 backdrop-blur-sm text-purple-700 dark:text-purple-300 text-[10px] px-2 py-1 rounded-full font-bold flex items-center gap-1 shadow-sm">
                        <Sparkles size={10} />
                        {topMood.toUpperCase()}
                    </div>
                )}
            </div>

            {/* Content */}
            <div className="flex flex-col flex-1">
                <h3 className="font-bold text-gray-900 dark:text-white leading-snug line-clamp-2 mb-1 group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">
                    {book.title}
                </h3>
                <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-1 mb-3">
                    {book.authors || "Unknown"}
                </p>

                {/* Footer */}
                <div className="mt-auto flex items-center justify-between">
                    {book.similarity_score !== undefined && (
                        <span className="text-xs font-bold text-green-600 dark:text-green-400 bg-green-50 dark:bg-green-900/20 px-2 py-1 rounded-md">
                            {Math.round(Math.max(0, (1 - book.similarity_score / 2) * 100))}% Match
                        </span>
                    )}
                    <span className="text-xs font-medium text-purple-600 dark:text-purple-400 opacity-0 group-hover:opacity-100 transition-opacity transform translate-x-2 group-hover:translate-x-0">
                        Read more →
                    </span>
                </div>
            </div>
        </div>
    );
}
