"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function Hero() {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;

    setIsLoading(true);
    
    // Simulate loading for 1 second
    await new Promise((resolve) => setTimeout(resolve, 1000));
    
    router.push("/report");
  };

  return (
    <section className="flex min-h-[80vh] flex-col items-center justify-center px-4 py-16 text-center bg-[#FAFAF9]">
      <div className="mx-auto w-full max-w-3xl space-y-8">
        {/* Headline - VERY large typography for elderly users */}
        <h1 className="font-heading text-5xl font-bold leading-tight tracking-tight text-slate-900 sm:text-6xl">
          Find a home that grows with you
        </h1>

        {/* Subheadline - Large body text */}
        <p className="mx-auto max-w-2xl text-xl leading-8 text-slate-600">
          Visualize accessibility renovations for your future home and make informed decisions about aging in place.
        </p>

        {/* Search Form */}
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 sm:flex-row sm:items-center">
          <div className="relative flex-1">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4">
              <Search className="h-5 w-5 text-slate-400" aria-hidden="true" />
            </div>
            <Input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="Paste Realtor.ca link here..."
              className="pl-12"
              aria-label="Realtor.ca listing URL"
              required
            />
          </div>
          <Button
            type="submit"
            disabled={isLoading}
            size="lg"
            className="bg-blue-600 sm:whitespace-nowrap"
          >
            {isLoading ? "Analyzing..." : "Analyze Home"}
          </Button>
        </form>

        {/* Helper Text */}
        <p className="text-sm text-slate-500">
          Simply paste any Realtor.ca listing URL to get started
        </p>
      </div>
    </section>
  );
}