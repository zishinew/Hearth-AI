import Hero from "@/components/landing/Hero";
import TrustSection from "@/components/landing/TrustSection";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col bg-[#FAFAF9]">
      <Hero />
      <TrustSection />
      <Footer />
    </main>
  );
}
