"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { MOCK_ANALYSIS, PropertyAnalysis } from "../../../../lib/mock-data";
import PropertySidebar from "@/components/report/PropertySidebar";
import TransformationViewer from "@/components/report/TransformationViewer";
import Gallery from "@/components/report/Gallery";
import LoadingSkeleton from "@/components/report/LoadingSkeleton";

interface PropertyInfo {
  address: string;
  price: string;
  bedrooms: string;
  bathrooms: string;
  square_feet: string;
  mls_number: string;
  neighborhood: string;
  location: string;
  amenities: string[];
}

interface AuditData {
  barrier: string;
  renovation_suggestion: string;
  cost_estimate: string;
  compliance_notes: string;
  accessibility_score: number;
  image_gen_prompt?: string;
  mask_prompt?: string;
  clear_mask?: string;
  clear_prompt?: string;
  build_mask?: string;
  build_prompt?: string;
  [key: string]: unknown;
}

interface ImageResult {
  image_number: number;
  original_url: string;
  audit: AuditData;
  error?: string;
}

interface ListingAnalysisResult {
  property_info: PropertyInfo;
  total_images_found: number;
  images_analyzed: number;
  results: ImageResult[];
}

export default function ReportPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [analysis, setAnalysis] = useState<PropertyAnalysis>(MOCK_ANALYSIS);
  const [listingResult, setListingResult] = useState<ListingAnalysisResult | null>(null);
  const [selectedImageIndex, setSelectedImageIndex] = useState(0);
  const [generatingImage, setGeneratingImage] = useState(false);
  const [renovatedImages, setRenovatedImages] = useState<{ [key: number]: string }>({});
  const router = useRouter();

  useEffect(() => {
    // Read listing analysis result from localStorage
    const storedListingResult = localStorage.getItem("listingAnalysisResult");

    if (storedListingResult) {
      try {
        const result: ListingAnalysisResult = JSON.parse(storedListingResult);
        setListingResult(result);

        // ONLY include images with identified problems
        const imagesWithProblems = result.results.filter(r => {
          // Check if audit exists and has a barrier/problem
          if (!r.audit || r.error) return false;

          // Check if barrier is meaningful (not N/A, empty, or "none")
          const barrier = r.audit.barrier?.toLowerCase() || '';
          if (!barrier || barrier === 'n/a' || barrier === 'none' || barrier === 'no barrier') {
            return false;
          }

          return true;
        });

        // Calculate total renovation cost from images with problems
        const totalRenovationCost = imagesWithProblems.reduce((sum, imageResult) => {
          if (imageResult.audit && imageResult.audit.cost_estimate) {
            // Parse cost estimate (e.g., "$1,500 - $3,000" -> average)
            const match = imageResult.audit.cost_estimate.match(/\$?([\d,]+)/g);
            if (match) {
              const costs = match.map(c => parseFloat(c.replace(/[$,]/g, '')));
              const avgCost = costs.reduce((a, b) => a + b, 0) / costs.length;
              return sum + avgCost;
            }
          }
          return sum;
        }, 0);

        // Calculate average accessibility score from images with problems
        const avgAccessibilityScore = imagesWithProblems.length > 0
          ? imagesWithProblems.reduce((sum, imageResult) => {
              return sum + (imageResult.audit?.accessibility_score || 0);
            }, 0) / imagesWithProblems.length
          : 100;

        // Transform to PropertyAnalysis format for existing components
        const transformedAnalysis: PropertyAnalysis = {
          id: "listing-analysis",
          address: result.property_info.address || "Property Analysis",
          originalPrice: parseFloat(result.property_info.price?.replace(/[$,]/g, '') || '0'),
          renovationCost: totalRenovationCost,
          accessibilityScore: {
            current: Math.round(100 - avgAccessibilityScore), // Round to whole number
            potential: Math.round(avgAccessibilityScore), // Round to whole number
          },
          features: imagesWithProblems.map((r, idx) => ({
            name: r.audit.barrier || "Accessibility Barrier",
            riskLevel: "High" as const,
            description: r.audit.renovation_suggestion || "",
          })),
          images: imagesWithProblems.map((r, idx) => ({
            label: `Room ${idx + 1}`,
            original: r.original_url,
            renovated: r.original_url, // Will be replaced when user clicks
          })),
        };

        setAnalysis(transformedAnalysis);
        setIsLoading(false);
      } catch (error) {
        console.error("Failed to parse listing analysis result:", error);
        setIsLoading(false);
      }
    } else {
      // No stored result, redirect to home
      router.push("/");
    }
  }, [router]);

  const handleImageClick = async (imageIndex: number) => {
    // If image already generated, just select it
    if (renovatedImages[imageIndex]) {
      setSelectedImageIndex(imageIndex);
      return;
    }

    // If no listing result, can't generate
    if (!listingResult || !listingResult.results[imageIndex]) {
      return;
    }

    const imageResult = listingResult.results[imageIndex];

    // Check if audit data has prompts for generation
    if (!imageResult.audit.image_gen_prompt || !imageResult.audit.mask_prompt) {
      console.warn("No generation prompts available for this image");
      setSelectedImageIndex(imageIndex);
      return;
    }

    // Generate renovation image on-demand
    setGeneratingImage(true);
    setSelectedImageIndex(imageIndex);

    try {
      const response = await fetch("http://localhost:8000/generate-renovation", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          image_url: imageResult.original_url,
          audit_data: imageResult.audit,
        }),
      });

      if (!response.ok) {
        throw new Error(`Generation failed: ${response.statusText}`);
      }

      const result = await response.json();

      if (result.success && result.renovated_image) {
        // Cache the generated image
        setRenovatedImages(prev => ({
          ...prev,
          [imageIndex]: result.renovated_image,
        }));

        // Update the analysis images with the renovated version
        setAnalysis(prev => ({
          ...prev,
          images: prev.images.map((img, idx) =>
            idx === imageIndex
              ? { ...img, renovated: result.renovated_image }
              : img
          ),
        }));
      } else {
        console.error("Image generation failed:", result.error);
      }
    } catch (error) {
      console.error("Error generating renovation image:", error);
    } finally {
      setGeneratingImage(false);
    }
  };

  if (isLoading) {
    return <LoadingSkeleton />;
  }

  return (
    <div className="min-h-screen bg-[#F0F7FF]">
      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="flex flex-col gap-8 lg:flex-row">
          {/* Left Sidebar - 1/3 width */}
          <aside className="w-full lg:w-1/3">
            <PropertySidebar analysis={analysis} propertyInfo={listingResult?.property_info} />
          </aside>

          {/* Right Main Area - 2/3 width */}
          <main className="w-full lg:w-2/3 space-y-8">
            <TransformationViewer
              analysis={analysis}
              selectedImageIndex={selectedImageIndex}
              originalImageUrl={analysis.images[selectedImageIndex]?.original || ""}
              renovatedImageData={renovatedImages[selectedImageIndex] || null}
              isGenerating={generatingImage}
            />
            <Gallery
              analysis={analysis}
              selectedIndex={selectedImageIndex}
              onImageSelect={handleImageClick}
              renovatedImages={renovatedImages}
            />
          </main>
        </div>
      </div>
    </div>
  );
}
