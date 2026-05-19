"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight } from "lucide-react";

interface CTAProps {
  data: {
    heading: string;
    subheading: string;
    button: { text: string; href: string };
    secondaryText: string;
  };
}

export function CTASection({ data }: CTAProps) {
  return (
    <section className="py-20 lg:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="relative rounded-3xl bg-gradient-to-br from-pink-600 to-purple-600 p-10 sm:p-16 lg:p-20 overflow-hidden">
          {/* Decorative elements */}
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_50%,rgba(255,255,255,0.1),transparent_50%)]" />
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full -translate-y-1/2 translate-x-1/2" />
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/5 rounded-full translate-y-1/2 -translate-x-1/2" />

          <div className="relative text-center text-white">
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight mb-4">
              {data.heading}
            </h2>
            <p className="text-lg text-pink-100 max-w-2xl mx-auto mb-8">
              {data.subheading}
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Button
                size="lg"
                className="bg-white text-pink-700 hover:bg-pink-50 text-base px-8 h-12 rounded-xl shadow-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
              >
                <Link href={data.button.href} className="flex items-center">
                  {data.button.text}
                  <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
            <p className="text-pink-200 text-sm mt-4">{data.secondaryText}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
