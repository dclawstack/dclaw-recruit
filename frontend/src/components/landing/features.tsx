"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Bot,
  KanbanSquare,
  CalendarCheck,
  FileCheck,
  Search,
  BarChart3,
  Mic,
  BadgeCheck,
  ArrowRightLeft,
  MessageCircle,
  type LucideIcon,
} from "lucide-react";

interface Feature {
  id: string;
  icon: string;
  title: string;
  description: string;
  badge: string;
  benefits: string[];
}

interface FeaturesProps {
  data: {
    heading: string;
    subheading: string;
    items: Feature[];
  };
}

const iconMap: Record<string, LucideIcon> = {
  Bot,
  KanbanSquare,
  CalendarCheck,
  FileCheck,
  Search,
  BarChart3,
  Mic,
  BadgeCheck,
  ArrowRightLeft,
  MessageCircle,
};

const badgeColors: Record<string, string> = {
  "New P0": "bg-pink-950/60 text-pink-300 border-pink-800/60",
  "New P1": "bg-purple-950/60 text-purple-300 border-purple-800/60",
  "Core AI": "bg-blue-950/60 text-blue-300 border-blue-800/60",
  "Insights": "bg-emerald-950/60 text-emerald-300 border-emerald-800/60",
};

export function Features({ data }: FeaturesProps) {
  return (
    <section id="features" className="py-20 lg:py-28 relative">
      <div className="absolute inset-0 bg-gradient-to-b from-background via-muted/20 to-background" />
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section header */}
        <div className="max-w-3xl mx-auto text-center mb-16">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-4">
            {data.heading}
          </h2>
          <p className="text-lg text-muted-foreground">{data.subheading}</p>
        </div>

        {/* Feature cards */}
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {data.items.map((feature) => {
            const Icon = iconMap[feature.icon] || Bot;
            const badgeClass = badgeColors[feature.badge] || "bg-pink-950/60 text-pink-300 border-pink-800/60";
            return (
              <Card
                key={feature.id}
                className="group relative overflow-hidden bg-card/50 border border-border/50 hover:border-pink-700/50 transition-all duration-300 hover:shadow-lg hover:shadow-pink-950/20 hover:-translate-y-1 backdrop-blur-sm"
              >
                <div className="absolute inset-0 bg-gradient-to-br from-pink-950/0 to-purple-950/0 group-hover:from-pink-950/10 group-hover:to-purple-950/10 transition-all duration-300" />
                <CardHeader className="relative">
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-pink-900/50 to-purple-900/50 border border-pink-800/30 flex items-center justify-center group-hover:from-pink-800/60 group-hover:to-purple-800/60 transition-all">
                      <Icon className="h-5 w-5 text-pink-400" />
                    </div>
                    <Badge
                      variant="outline"
                      className={`text-xs ${badgeClass}`}
                    >
                      {feature.badge}
                    </Badge>
                  </div>
                  <CardTitle className="text-base">{feature.title}</CardTitle>
                  <CardDescription className="text-sm leading-relaxed text-muted-foreground/80">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent className="relative">
                  <ul className="space-y-2">
                    {feature.benefits.map((benefit, i) => (
                      <li key={i} className="flex items-start gap-2 text-sm text-muted-foreground">
                        <svg
                          className="h-4 w-4 mt-0.5 shrink-0 text-pink-500"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2}
                        >
                          <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                        </svg>
                        {benefit}
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>
    </section>
  );
}
