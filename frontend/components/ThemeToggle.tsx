"use client"

import * as React from "react"
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"

export function ThemeToggle() {
    const { theme, setTheme } = useTheme()
    const [mounted, setMounted] = React.useState(false)

    React.useEffect(() => {
        setMounted(true)
    }, [])

    if (!mounted) {
        return (
            <button className="p-2 rounded-full bg-gray-200 dark:bg-gray-800 animate-pulse">
                <span className="sr-only">Loading theme</span>
                <div className="w-5 h-5" />
            </button>
        )
    }

    return (
        <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="relative p-2 rounded-full transition-colors hover:bg-gray-100 dark:hover:bg-gray-800 focus:outline-none ring-offset-2 focus:ring-2 ring-purple-500"
            aria-label="Toggle Theme"
        >
            <Sun className="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0 text-amber-500" />
            <Moon className="absolute top-2 left-2 h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100 text-purple-400" />
            <span className="sr-only">Toggle theme</span>
        </button>
    )
}
