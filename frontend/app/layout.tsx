import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "next-themes";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Semantic Book Recommender",
  description: "Find your next read with AI-powered semantic search.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <ThemeProvider attribute="class" defaultTheme="light" enableSystem>
          <div className="min-h-screen bg-gray-50 dark:bg-slate-950 transition-colors duration-300">
            {children}
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
