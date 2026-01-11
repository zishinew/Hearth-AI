import Hero from "@/components/landing/Hero";
import Footer from "@/components/landing/Footer";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col bg-[#FFF8E7] diagonal-dots-bg">
      <Hero />
      <Footer />
    </main>
  );
}
