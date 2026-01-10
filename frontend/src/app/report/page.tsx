"use client";

import { useState, useEffect } from "react";
import { MOCK_ANALYSIS } from "../../../../lib/mock-data";
import PropertySidebar from "@/components/report/PropertySidebar";
import TransformationViewer from "@/components/report/TransformationViewer";
import Gallery from "@/components/report/Gallery";
import LoadingSkeleton from "@/components/report/LoadingSkeleton";

export default function ReportPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [analysis, setAnalysis] = useState(MOCK_ANALYSIS);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);

  useEffect(() => {
    // Simulate loading state
    const timer = setTimeout(() => {
      setIsLoading(false);
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  return (
    <div className="min-h-screen bg-[#FAFAF9]">
      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="flex flex-col gap-8 lg:flex-row">
          {/* Left Sidebar - 1/3 width */}
          <aside className="w-full lg:w-1/3">
            <PropertySidebar analysis={analysis} />
          </aside>

          {/* Right Main Area - 2/3 width */}
          <main className="w-full lg:w-2/3 space-y-8">
            <TransformationViewer 
              analysis={analysis} 
              selectedImageIndex={selectedImageIndex}
            />
            <Gallery 
              analysis={analysis} 
              selectedIndex={selectedImageIndex}
              onImageSelect={setSelectedImageIndex}
            />
          </main>
        </div>
      </div>
    </div>
  );
}
