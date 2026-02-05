import { Book } from "@/lib/types";
import BookCard from "./BookCard";

import clsx from "clsx";

interface BookGridProps {
    books: Book[];
    isLoading: boolean;
    onSelectBook: (book: Book) => void;
}

export default function BookGrid({ books, isLoading, onSelectBook }: BookGridProps) {
    if (isLoading && books.length === 0) {
        return (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 w-full">
                {[...Array(10)].map((_, i) => (
                    <div key={i} className="aspect-[2/3] w-full rounded-xl bg-gray-200 dark:bg-slate-800 animate-pulse" />
                ))}
            </div>
        );
    }

    if (books.length === 0) {
        return (
            <div className="text-center py-20 flex flex-col items-center justify-center">
                <div className="bg-gray-100 dark:bg-slate-800 p-6 rounded-full mb-4">
                    <span className="text-4xl">📚</span>
                </div>
                <h3 className="text-2xl font-bold text-gray-700 dark:text-gray-200">No books found</h3>
                <p className="text-gray-500 mt-2 max-w-md mx-auto">
                    We couldn't find any matches locally. Try a different mood or keyword.
                </p>
            </div>
        )
    }

    // Deduplicate books by ISBN just in case
    const uniqueBooks = Array.from(new Map(books.map(book => [book.isbn13 + book.title, book])).values());

    return (
        <div className={clsx("grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6 w-full pb-20", isLoading ? "opacity-60 pointer-events-none" : "")}>
            {uniqueBooks.map((book) => (
                <BookCard
                    key={`${book.isbn13}-${book.title}`}
                    book={book}
                    onSelect={onSelectBook}
                />
            ))}
        </div>
    );
}
