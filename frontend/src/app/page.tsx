"use client";

import landingData from "@/data/landing-content.json";
import { Navbar } from "@/components/landing/navbar";
import { Hero } from "@/components/landing/hero";
import { Features } from "@/components/landing/features";
import { HowItWorks } from "@/components/landing/how-it-works";
import { Testimonials } from "@/components/landing/testimonials";
import { Pricing } from "@/components/landing/pricing";
import { CTASection } from "@/components/landing/cta-section";
import { Footer } from "@/components/landing/footer";

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      <main>
        <Hero data={landingData.hero} />
        <Features data={landingData.features} />
        <HowItWorks data={landingData.howItWorks} />
        <Testimonials data={landingData.testimonials} />
        <Pricing data={landingData.pricing} />
        <CTASection data={landingData.cta} />
      </main>
      <Footer data={landingData.footer} />
    </div>
  );
}
