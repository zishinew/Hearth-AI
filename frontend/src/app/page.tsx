import Hero from "@/components/landing/Hero";
import TrustSection from "@/components/landing/TrustSection";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col bg-[#FFF8E7]">
      <Hero />
      <TrustSection />
      <Footer />
    </main>
  );
}
