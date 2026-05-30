"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { ArrowRight, Briefcase, Users, CalendarDays, BarChart3, Bot, CheckCircle2 } from "lucide-react";

const tabs = [
  { id: "jobs", label: "Job Pipeline", icon: Briefcase },
  { id: "candidates", label: "Candidates", icon: Users },
  { id: "ai", label: "AI Copilot", icon: Bot },
  { id: "analytics", label: "Analytics", icon: BarChart3 },
];

const mockData: Record<string, React.ReactNode> = {
  jobs: (
    <div className="space-y-2">
      {[
        { title: "Senior Backend Engineer", dept: "Engineering", count: 12, status: "open", match: "94%" },
        { title: "Product Designer", dept: "Design", count: 8, status: "open", match: "88%" },
        { title: "Growth Manager", dept: "Marketing", count: 5, status: "paused", match: "76%" },
        { title: "AI/ML Engineer", dept: "Engineering", count: 19, status: "open", match: "91%" },
      ].map((job) => (
        <div key={job.title} className="flex items-center justify-between px-4 py-3 rounded-lg bg-muted/40 border border-border/40 hover:border-pink-800/40 transition-all group">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-md bg-pink-950/50 border border-pink-800/30 flex items-center justify-center">
              <Briefcase className="h-3.5 w-3.5 text-pink-400" />
            </div>
            <div>
              <div className="text-sm font-medium text-foreground">{job.title}</div>
              <div className="text-xs text-muted-foreground">{job.dept} · {job.count} applicants</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-emerald-400 bg-emerald-950/50 px-2 py-0.5 rounded border border-emerald-800/30">
              {job.match} AI match
            </span>
            <span className={`text-xs px-2 py-0.5 rounded border ${job.status === "open" ? "text-blue-400 bg-blue-950/50 border-blue-800/30" : "text-yellow-400 bg-yellow-950/50 border-yellow-800/30"}`}>
              {job.status}
            </span>
          </div>
        </div>
      ))}
    </div>
  ),
  candidates: (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
      {[
        { stage: "Applied", color: "blue", count: 47, items: ["Alex Chen", "Maria Santos", "James Liu"] },
        { stage: "Screening", color: "purple", count: 12, items: ["Priya Patel", "Sam Kim", "Elena Ross"] },
        { stage: "Interview", color: "pink", count: 6, items: ["Tom Burke", "Aisha Musa"] },
        { stage: "Offer", color: "emerald", count: 2, items: ["Sarah Wong"] },
      ].map((col) => (
        <div key={col.stage} className="space-y-2">
          <div className={`text-xs font-semibold px-2 py-1 rounded text-${col.color}-400 bg-${col.color}-950/50 border border-${col.color}-800/30 flex justify-between`}>
            <span>{col.stage}</span>
            <span>{col.count}</span>
          </div>
          {col.items.map((name) => (
            <div key={name} className="px-2 py-2 rounded bg-muted/40 border border-border/40 text-xs text-muted-foreground hover:border-pink-800/40 transition-all cursor-pointer">
              {name}
            </div>
          ))}
        </div>
      ))}
    </div>
  ),
  ai: (
    <div className="space-y-3">
      <div className="flex gap-3">
        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-pink-600 to-purple-600 flex items-center justify-center shrink-0 mt-0.5">
          <Bot className="h-3.5 w-3.5 text-white" />
        </div>
        <div className="bg-muted/40 border border-border/40 rounded-xl rounded-tl-sm px-4 py-3 text-sm text-muted-foreground flex-1">
          Found <span className="text-pink-400 font-semibold">23 candidates</span> matching &ldquo;Senior Backend Engineer&rdquo; with 4+ years Go experience. Top match: <span className="text-foreground">Alex Chen (94%)</span> — currently at Stripe, 6yr Go, open source contributor.
        </div>
      </div>
      <div className="flex gap-3 justify-end">
        <div className="bg-pink-950/40 border border-pink-800/30 rounded-xl rounded-tr-sm px-4 py-3 text-sm text-pink-200 max-w-xs">
          Generate personalized outreach for top 5 candidates
        </div>
        <div className="w-7 h-7 rounded-full bg-muted border border-border flex items-center justify-center shrink-0 mt-0.5 text-xs font-bold text-muted-foreground">
          You
        </div>
      </div>
      <div className="flex gap-3">
        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-pink-600 to-purple-600 flex items-center justify-center shrink-0 mt-0.5">
          <Bot className="h-3.5 w-3.5 text-white" />
        </div>
        <div className="bg-muted/40 border border-border/40 rounded-xl rounded-tl-sm px-4 py-3 text-sm text-muted-foreground flex-1">
          <CheckCircle2 className="inline h-3.5 w-3.5 text-emerald-400 mr-1" />
          Generated 5 personalized messages. Avg open rate prediction: <span className="text-emerald-400 font-semibold">68%</span>. Ready to send.
        </div>
      </div>
    </div>
  ),
  analytics: (
    <div className="space-y-4">
      <div className="grid grid-cols-3 gap-3">
        {[
          { label: "Time-to-Hire", value: "18d", change: "-34%", up: false },
          { label: "Offer Accept Rate", value: "82%", change: "+12%", up: true },
          { label: "Source Quality", value: "4.6★", change: "+0.4", up: true },
        ].map((m) => (
          <div key={m.label} className="bg-muted/40 border border-border/40 rounded-lg p-3">
            <div className="text-xs text-muted-foreground mb-1">{m.label}</div>
            <div className="text-xl font-bold text-foreground">{m.value}</div>
            <div className={`text-xs mt-0.5 ${m.up ? "text-emerald-400" : "text-pink-400"}`}>{m.change} vs last qtr</div>
          </div>
        ))}
      </div>
      <div className="bg-muted/40 border border-border/40 rounded-lg p-3">
        <div className="text-xs text-muted-foreground mb-2">Pipeline by Stage</div>
        {[
          { stage: "Applied", pct: 100, count: 234 },
          { stage: "Screening", pct: 62, count: 144 },
          { stage: "Interview", pct: 28, count: 65 },
          { stage: "Offer", pct: 8, count: 18 },
        ].map((row) => (
          <div key={row.stage} className="flex items-center gap-3 mb-1.5">
            <div className="text-xs text-muted-foreground w-16 shrink-0">{row.stage}</div>
            <div className="flex-1 bg-border/30 rounded-full h-1.5">
              <div
                className="h-1.5 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
                style={{ width: `${row.pct}%` }}
              />
            </div>
            <div className="text-xs text-muted-foreground w-8 text-right">{row.count}</div>
          </div>
        ))}
      </div>
    </div>
  ),
};

export function DemoSection() {
  const [activeTab, setActiveTab] = React.useState("jobs");

  return (
    <section id="demo" className="py-20 lg:py-28">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-950/50 border border-purple-800/50 text-xs text-purple-300 mb-4">
            Product Preview
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight mb-4">
            See It In Action
          </h2>
          <p className="text-lg text-muted-foreground">
            A full-stack recruiting platform built for the 2026 talent market — from AI sourcing to offer management.
          </p>
        </div>

        {/* Browser mockup */}
        <div className="max-w-4xl mx-auto rounded-2xl border border-border/50 overflow-hidden shadow-2xl shadow-black/40">
          {/* Browser chrome */}
          <div className="bg-muted/60 border-b border-border/50 px-4 py-3 flex items-center gap-3">
            <div className="flex gap-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500/60" />
              <div className="w-3 h-3 rounded-full bg-yellow-500/60" />
              <div className="w-3 h-3 rounded-full bg-green-500/60" />
            </div>
            <div className="flex-1 bg-background/50 border border-border/40 rounded-md px-3 py-1 text-xs text-muted-foreground text-center">
              app.dclaw-recruit.vercel.app/dashboard
            </div>
          </div>

          {/* App chrome */}
          <div className="flex bg-background min-h-[360px]">
            {/* Mini sidebar */}
            <div className="w-40 bg-muted/30 border-r border-border/40 p-3 hidden sm:block">
              <div className="flex items-center gap-2 mb-4 px-2">
                <div className="w-5 h-5 rounded bg-gradient-to-br from-pink-500 to-purple-600 flex items-center justify-center">
                  <span className="text-white text-[8px] font-bold">R</span>
                </div>
                <span className="text-xs font-semibold text-foreground/80">DClaw</span>
              </div>
              {[
                { icon: BarChart3, label: "Dashboard" },
                { icon: Briefcase, label: "Jobs" },
                { icon: Users, label: "Candidates" },
                { icon: CalendarDays, label: "Interviews" },
              ].map((item) => (
                <div key={item.label} className={`flex items-center gap-2 px-2 py-1.5 rounded-md mb-0.5 cursor-pointer transition-colors ${item.label === "Jobs" ? "bg-pink-950/50 text-pink-300" : "text-muted-foreground hover:text-foreground hover:bg-muted/50"}`}>
                  <item.icon className="h-3 w-3" />
                  <span className="text-xs">{item.label}</span>
                </div>
              ))}
            </div>

            {/* Content area */}
            <div className="flex-1 p-4">
              {/* Tabs */}
              <div className="flex gap-1 mb-4 bg-muted/40 p-1 rounded-lg border border-border/40 w-fit">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all ${
                      activeTab === tab.id
                        ? "bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-sm"
                        : "text-muted-foreground hover:text-foreground"
                    }`}
                  >
                    <tab.icon className="h-3 w-3" />
                    {tab.label}
                  </button>
                ))}
              </div>

              {/* Tab content */}
              <div className="transition-all">
                {mockData[activeTab]}
              </div>
            </div>
          </div>
        </div>

        <div className="text-center mt-8">
          <Button
            size="lg"
            className="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white border-0 rounded-xl px-8"
            asChild
          >
            <Link href="/signup" className="flex items-center gap-2">
              Start Free Trial
              <ArrowRight className="h-4 w-4" />
            </Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
