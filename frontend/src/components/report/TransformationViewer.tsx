"use client";

import Image from "next/image";
import type { PropertyAnalysis } from "../../../../lib/mock-data";

interface TransformationViewerProps {
  analysis: PropertyAnalysis;
  selectedImageIndex?: number;
}

export default function TransformationViewer({
  analysis,
  selectedImageIndex = 0,
}: TransformationViewerProps) {
  // Use the selected image or first image from the gallery as the main transformation
  const mainImage = analysis.images[selectedImageIndex] || analysis.images[0] || {
    label: "Main Entryway",
    original: "",
    renovated: "",
  };

  return (
    <div className="bg-white rounded-lg p-6 shadow-sm space-y-6">
      {/* Address - Large, Centered */}
      <div className="text-center">
        <h1 className="font-heading text-4xl font-bold text-slate-900 sm:text-5xl">
          {analysis.address}
        </h1>
      </div>

      {/* Before & After Comparison - Split View */}
      <div className="relative w-full h-[600px] rounded-lg overflow-hidden border-4 border-slate-200">
        {/* Dashed divider line */}
        <div className="absolute left-1/2 top-0 bottom-0 w-0.5 border-l-2 border-dashed border-slate-400 z-10"></div>

        {/* BEFORE Section - Left */}
        <div className="absolute left-0 top-0 w-1/2 h-full">
          <div className="absolute top-4 left-4 z-20 bg-white/90 px-4 py-2 rounded-lg shadow-sm">
            <span className="font-heading text-xl font-bold text-slate-900">
              BEFORE
            </span>
          </div>
          <Image
            src={mainImage.original}
            alt="Before renovation"
            fill
            className="object-cover"
            sizes="50vw"
          />
        </div>

        {/* AFTER Section - Right */}
        <div className="absolute right-0 top-0 w-1/2 h-full">
          <div className="absolute top-4 right-4 z-20 bg-white/90 px-4 py-2 rounded-lg shadow-sm">
            <span className="font-heading text-xl font-bold text-slate-900">
              AFTER
            </span>
          </div>
          <Image
            src={mainImage.renovated}
            alt="After renovation"
            fill
            className="object-cover"
            sizes="50vw"
          />
        </div>
      </div>
    </div>
  );
}
