import { Book } from "@/lib/types";
import { X, BookOpen, Sparkles, User, Calendar, Star } from "lucide-react";
import Image from "next/image";
import { useState, useEffect } from "react";
import clsx from "clsx";

interface BookModalProps {
    book: Book | null;
    onClose: () => void;
}

export default function BookModal({ book, onClose }: BookModalProps) {
    const [isOpen, setIsOpen] = useState(false);

    useEffect(() => {
        if (book) {
            setIsOpen(true);
            document.body.style.overflow = "hidden"; // Prevent background scroll
        } else {
            setIsOpen(false);
            document.body.style.overflow = "unset";
        }
        return () => { document.body.style.overflow = "unset"; };
    }, [book]);

    if (!book) return null;

    // Get top mood
    const topMood = book.moods
        ? Object.entries(book.moods).reduce((a, b) => a[1] > b[1] ? a : b)[0]
        : null;

    return (
        <div
            className={clsx(
                "fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 transition-opacity duration-300",
                isOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
            )}
        >
            {/* Backdrop */}
            <div
                className="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity"
                onClick={onClose}
            />

            {/* Modal Content */}
            <div
                className={clsx(
                    "relative w-full max-w-2xl bg-white dark:bg-slate-900 rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] transition-transform duration-300 transform",
                    isOpen ? "scale-100 translate-y-0" : "scale-95 translate-y-4"
                )}
            >
                {/* Close Button */}
                <button
                    onClick={onClose}
                    className="absolute top-4 right-4 z-10 p-2 rounded-full bg-white/10 hover:bg-white/20 text-gray-500 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white transition-colors"
                >
                    <X size={20} />
                </button>

                <div className="flex flex-col md:flex-row h-full overflow-y-auto md:overflow-hidden">
                    {/* Image Side */}
                    <div className="w-full md:w-2/5 h-64 md:h-auto bg-gray-50 dark:bg-slate-800 flex items-center justify-center p-6 relative">
                        {book.thumbnail ? (
                            <div className="relative w-40 h-60 md:w-full md:h-full max-h-[300px] shadow-lg rounded-md overflow-hidden transform transition-transform hover:scale-105 duration-500">
                                <Image
                                    src={book.thumbnail}
                                    alt={book.title}
                                    fill
                                    className="object-cover"
                                />
                            </div>
                        ) : (
                            <BookOpen size={64} className="text-gray-300" />
                        )}

                        {/* Match Score */}
                        {book.similarity_score !== undefined && (
                            <div className="absolute top-4 left-4 bg-green-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg">
                                {Math.round(Math.max(0, (1 - book.similarity_score / 2) * 100))}% Match
                            </div>
                        )}
                    </div>

                    {/* Content Side */}
                    <div className="w-full md:w-3/5 p-6 md:p-8 flex flex-col">
                        <div className="flex items-start justify-between gap-4 mb-2">
                            {topMood && (
                                <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 uppercase tracking-wider">
                                    <Sparkles size={12} />
                                    {topMood}
                                </span>
                            )}
                        </div>

                        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-2 leading-tight">
                            {book.title}
                        </h2>

                        <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-6 flex items-center gap-2">
                            <User size={16} />
                            {book.authors || "Unknown Author"}
                        </p>

                        <div className="flex items-center gap-6 mb-8 text-sm text-gray-500 dark:text-gray-400 border-y border-gray-100 dark:border-gray-800 py-4">
                            <div className="flex items-center gap-2">
                                <Calendar size={16} className="text-purple-500" />
                                <span>{book.published_year || "N/A"}</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <Star size={16} className="text-amber-500" />
                                <span>{book.average_rating || "N/A"} / 5</span>
                            </div>
                        </div>

                        <div className="prose prose-sm dark:prose-invert max-w-none overflow-y-auto pr-2 custom-scrollbar">
                            <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                                {book.description || "No description available for this book."}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
