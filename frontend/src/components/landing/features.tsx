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

export function Features({ data }: FeaturesProps) {
  return (
    <section id="features" className="py-20 lg:py-28 bg-muted/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
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
            return (
              <Card
                key={feature.id}
                className="group relative overflow-hidden border-2 border-transparent hover:border-pink-200 dark:hover:border-pink-800 transition-all duration-300 hover:shadow-lg hover:-translate-y-1"
              >
                <CardHeader>
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-10 h-10 rounded-lg bg-pink-50 dark:bg-pink-950/50 flex items-center justify-center group-hover:bg-pink-100 dark:group-hover:bg-pink-900/50 transition-colors">
                      <Icon className="h-5 w-5 text-pink-600 dark:text-pink-400" />
                    </div>
                    <Badge
                      variant="secondary"
                      className="text-xs bg-pink-50 text-pink-700 dark:bg-pink-950/30 dark:text-pink-300 border-pink-200 dark:border-pink-800"
                    >
                      {feature.badge}
                    </Badge>
                  </div>
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                  <CardDescription className="text-sm leading-relaxed">
                    {feature.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="space-y-2">
                    {feature.benefits.map((benefit, i) => (
                      <li
                        key={i}
                        className="flex items-start gap-2 text-sm text-muted-foreground"
                      >
                        <svg
                          className="h-4 w-4 mt-0.5 shrink-0 text-pink-500"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M5 13l4 4L19 7"
                          />
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
