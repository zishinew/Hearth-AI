"use client";

import Link from "next/link";
import { Home } from "lucide-react";

export default function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-[#D4A574]/20 bg-[#FFF8E7]/95 backdrop-blur-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center">
          <Link 
            href="/" 
            className="flex items-center gap-2 text-[#5C4033] hover:text-[#D2691E] transition-colors"
          >
            {/* Temporary logo - simple home icon */}
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#D2691E] text-white">
              <Home className="h-6 w-6" />
            </div>
            <span className="text-xl font-bold text-[#5C4033]">hearth.</span>
          </Link>
        </div>
      </div>
    </header>
  );
}

