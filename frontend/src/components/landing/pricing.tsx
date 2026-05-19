"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Check } from "lucide-react";

interface PricingProps {
  data: {
    heading: string;
    subheading: string;
    plans: {
      name: string;
      price: string;
      period: string;
      description: string;
      features: string[];
      cta: string;
      href: string;
      highlighted: boolean;
    }[];
  };
}

export function Pricing({ data }: PricingProps) {
  return (
    <section id="pricing" className="py-20 lg:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-4">
            {data.heading}
          </h2>
          <p className="text-lg text-muted-foreground">{data.subheading}</p>
        </div>

        {/* Plans */}
        <div className="grid gap-8 lg:grid-cols-3 max-w-5xl mx-auto">
          {data.plans.map((plan) => (
            <div
              key={plan.name}
              className={`relative rounded-2xl border-2 p-8 flex flex-col transition-all duration-300 hover:-translate-y-1 ${
                plan.highlighted
                  ? "border-pink-500 shadow-xl shadow-pink-100 dark:shadow-pink-900/20 bg-card scale-[1.02]"
                  : "border-border hover:border-pink-200 dark:hover:border-pink-800 hover:shadow-lg bg-card"
              }`}
            >
              {plan.highlighted && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 px-4 py-1 bg-pink-600 text-white text-xs font-semibold rounded-full">
                  Most Popular
                </div>
              )}

              <div className="mb-6">
                <h3 className="text-xl font-bold mb-1">{plan.name}</h3>
                <p className="text-sm text-muted-foreground">
                  {plan.description}
                </p>
              </div>

              <div className="mb-6">
                <span className="text-4xl font-extrabold">{plan.price}</span>
                {plan.period && (
                  <span className="text-muted-foreground ml-1">
                    {plan.period}
                  </span>
                )}
              </div>

              <ul className="space-y-3 mb-8 flex-1">
                {plan.features.map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm">
                    <Check className="h-4 w-4 text-pink-500 shrink-0" />
                    <span className="text-muted-foreground">{feature}</span>
                  </li>
                ))}
              </ul>

              <Button
                className={`w-full h-11 rounded-xl ${
                  plan.highlighted
                    ? "bg-pink-600 hover:bg-pink-700 text-white"
                    : "bg-muted hover:bg-muted/80"
                }`}
                variant={plan.highlighted ? "default" : "secondary"}
              >
                <Link href={plan.href}>{plan.cta}</Link>
              </Button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
