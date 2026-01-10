import type { Metadata } from "next";
import { Inter, Plus_Jakarta_Sans } from "next/font/google";
import "./globals.css";

// 1. Configure the Body Font (Standard text)
const inter = Inter({
  subsets: ["latin"],
  variable: "--font-body",
  display: "swap",
});

// 2. Configure the Heading Font (Large, readable titles)
const jakarta = Plus_Jakarta_Sans({
  subsets: ["latin"],
  variable: "--font-heading",
  display: "swap",
});

export const metadata: Metadata = {
  title: "ForeverHome - Aging in Place",
  description: "Visualize accessibility renovations for your future home.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        // 3. Apply the font variables - Inter for body, Plus Jakarta Sans for headings
        className={`${inter.variable} ${jakarta.variable} antialiased bg-[#FAFAF9] text-slate-900`}
        style={{
          fontFamily: "var(--font-body)",
        }}
      >
        {children}
      </body>
    </html>
  );
}