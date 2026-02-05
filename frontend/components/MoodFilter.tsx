import { Mood } from "@/lib/types";
import { Filter } from "lucide-react";

interface MoodFilterProps {
    selectedMood: string | undefined;
    onSelectMood: (mood: string | undefined) => void;
}

const MOODS: Mood[] = [
    "joyful", "sad", "suspenseful", "romantic",
    "dark", "adventurous", "funny", "inspirational",
    "thriller", "mystery", "educational", "technical"
];

export default function MoodFilter({ selectedMood, onSelectMood }: MoodFilterProps) {
    return (
        <div className="relative inline-block text-left z-10">
            <div className="flex items-center gap-2">
                <Filter className="h-5 w-5 text-gray-500 dark:text-gray-400" />
                <select
                    value={selectedMood || ""}
                    onChange={(e) => onSelectMood(e.target.value || undefined)}
                    className="block w-full rounded-md border-0 py-2 pl-3 pr-10 text-gray-900 dark:text-gray-100 ring-1 ring-inset ring-gray-300 dark:ring-gray-700 focus:ring-2 focus:ring-purple-600 sm:text-sm sm:leading-6 bg-white dark:bg-slate-800"
                >
                    <option value="">All Moods</option>
                    {MOODS.map((mood) => (
                        <option key={mood} value={mood} className="capitalize">{mood}</option>
                    ))}
                </select>
            </div>
        </div>
    );
}
