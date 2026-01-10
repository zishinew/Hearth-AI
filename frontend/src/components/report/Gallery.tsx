"use client";

import Image from "next/image";
import type { PropertyAnalysis } from "../../../../lib/mock-data";

interface GalleryProps {
  analysis: PropertyAnalysis;
  selectedIndex: number;
  onImageSelect: (index: number) => void;
}

export default function Gallery({ 
  analysis, 
  selectedIndex, 
  onImageSelect 
}: GalleryProps) {
  return (
    <div className="bg-white rounded-lg p-6 shadow-sm">
      <h2 className="font-heading text-2xl font-bold text-slate-900 mb-4">
        Image Gallery
      </h2>
      <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-hide">
        {analysis.images.map((image, index) => (
          <button
            key={index}
            onClick={() => onImageSelect(index)}
            className={`flex-shrink-0 rounded-lg overflow-hidden border-4 transition-all ${
              selectedIndex === index
                ? "border-blue-600 scale-105 shadow-lg"
                : "border-transparent hover:border-slate-300"
            }`}
          >
            <div className="relative w-32 h-24">
              <Image
                src={image.original}
                alt={`${image.label} thumbnail`}
                fill
                className="object-cover"
                sizes="128px"
              />
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
