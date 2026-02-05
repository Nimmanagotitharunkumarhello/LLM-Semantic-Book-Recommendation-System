import { Search } from "lucide-react";
import { useState, useEffect, useRef } from "react";

interface SearchBarProps {
    onSearch: (query: string) => void;
    isSearching: boolean;
}

export default function SearchBar({ onSearch, isSearching }: SearchBarProps) {
    const [query, setQuery] = useState("");
    const firstRender = useRef(true);

    useEffect(() => {
        if (firstRender.current) {
            firstRender.current = false;
            return;
        }

        const timeoutId = setTimeout(() => {
            onSearch(query);
        }, 500); // 500ms debounce

        return () => clearTimeout(timeoutId);
    }, [query, onSearch]);

    return (
        <div className="relative w-full max-w-2xl mx-auto">
            <div className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-lg blur opacity-25 group-hover:opacity-100 transition duration-1000 group-hover:duration-200"></div>
                <div className="relative flex items-center bg-white dark:bg-slate-900 rounded-lg shadow-xl ring-1 ring-slate-900/5">
                    <Search className="ml-4 h-5 w-5 text-slate-400" />
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Find your next great read by plot, mood, or character..."
                        className="w-full h-14 bg-transparent pl-4 pr-4 ml-2 text-slate-900 dark:text-slate-100 placeholder:text-slate-400 focus:outline-none text-lg"
                    />
                    {isSearching && (
                        <div className="absolute right-4 animate-spin h-5 w-5 border-2 border-purple-500 rounded-full border-t-transparent"></div>
                    )}
                </div>
            </div>
        </div>
    );
}
