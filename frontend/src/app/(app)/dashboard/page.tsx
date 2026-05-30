"use client";

import React from "react";
import Link from "next/link";
import { AppHeader } from "@/components/app/app-header";
import { listJobs, listCandidates, listInterviews } from "@/lib/api";
import { Briefcase, Users, CalendarDays, TrendingUp, ArrowRight, Clock, CheckCircle2 } from "lucide-react";

interface Stats {
  jobs: number;
  candidates: number;
  interviews: number;
}

export default function DashboardPage() {
  const [stats, setStats] = React.useState<Stats>({ jobs: 0, candidates: 0, interviews: 0 });
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    async function load() {
      try {
        const [j, c, i] = await Promise.all([
          listJobs({ limit: 1 }),
          listCandidates({ limit: 1 }),
          listInterviews({ limit: 1 }),
        ]);
        setStats({ jobs: j.total, candidates: c.total, interviews: i.total });
      } catch {
        // API not available in demo mode
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const statCards = [
    { label: "Active Jobs", value: loading ? "—" : String(stats.jobs), icon: Briefcase, href: "/jobs", color: "pink" },
    { label: "Total Candidates", value: loading ? "—" : String(stats.candidates), icon: Users, href: "/candidates", color: "purple" },
    { label: "Interviews Scheduled", value: loading ? "—" : String(stats.interviews), icon: CalendarDays, href: "/interviews", color: "blue" },
    { label: "Avg Time-to-Hire", value: "18d", icon: TrendingUp, href: "/jobs", color: "emerald" },
  ];

  const recentActivity = [
    { icon: Users, text: "New application from Alex Chen for Senior Backend Engineer", time: "2m ago", type: "apply" },
    { icon: CheckCircle2, text: "Interview completed with Priya Patel — Score: 4.2/5", time: "1h ago", type: "interview" },
    { icon: Briefcase, text: "AI Copilot sourced 12 candidates for Product Designer role", time: "3h ago", type: "source" },
    { icon: CalendarDays, text: "Interview scheduled: Tom Burke × Engineering Panel — Fri 2pm", time: "5h ago", type: "schedule" },
    { icon: TrendingUp, text: "Offer accepted: Sarah Wong joins as Senior Frontend Engineer", time: "1d ago", type: "hire" },
  ];

  const colorMap: Record<string, string> = {
    pink: "from-pink-950/60 to-pink-900/20 border-pink-800/30 text-pink-400",
    purple: "from-purple-950/60 to-purple-900/20 border-purple-800/30 text-purple-400",
    blue: "from-blue-950/60 to-blue-900/20 border-blue-800/30 text-blue-400",
    emerald: "from-emerald-950/60 to-emerald-900/20 border-emerald-800/30 text-emerald-400",
  };

  return (
    <>
      <AppHeader title="Dashboard" action={{ label: "New Job", href: "/jobs/new" }} />
      <main className="flex-1 p-6 space-y-6">
        {/* Stats grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {statCards.map((card) => (
            <Link
              key={card.label}
              href={card.href}
              className={`rounded-xl border bg-gradient-to-br p-5 hover:opacity-90 transition-all hover:-translate-y-0.5 ${colorMap[card.color]}`}
            >
              <div className="flex items-start justify-between mb-3">
                <card.icon className="h-5 w-5" />
                <ArrowRight className="h-3.5 w-3.5 opacity-50" />
              </div>
              <div className="text-3xl font-bold text-foreground mb-1">{card.value}</div>
              <div className="text-xs text-muted-foreground">{card.label}</div>
            </Link>
          ))}
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Recent activity */}
          <div className="lg:col-span-2 bg-card/40 border border-border/50 rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <h2 className="font-semibold text-sm text-foreground">Recent Activity</h2>
              <span className="text-xs text-muted-foreground">Live</span>
            </div>
            <div className="space-y-3">
              {recentActivity.map((item, i) => (
                <div key={i} className="flex gap-3 items-start">
                  <div className="w-7 h-7 rounded-lg bg-muted/60 border border-border/40 flex items-center justify-center shrink-0 mt-0.5">
                    <item.icon className="h-3.5 w-3.5 text-muted-foreground" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs text-muted-foreground leading-relaxed">{item.text}</p>
                    <div className="flex items-center gap-1 mt-1 text-xs text-muted-foreground/60">
                      <Clock className="h-3 w-3" />
                      {item.time}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Quick actions */}
          <div className="space-y-4">
            <div className="bg-card/40 border border-border/50 rounded-xl p-5">
              <h2 className="font-semibold text-sm text-foreground mb-4">Quick Actions</h2>
              <div className="space-y-2">
                {[
                  { label: "Post a New Job", href: "/jobs/new", desc: "Create a job requisition" },
                  { label: "Add Candidate", href: "/candidates", desc: "Upload resume or add manually" },
                  { label: "Schedule Interview", href: "/interviews", desc: "Book time with a candidate" },
                  { label: "View Pipeline", href: "/candidates", desc: "Check candidate stages" },
                ].map((action) => (
                  <Link
                    key={action.href + action.label}
                    href={action.href}
                    className="flex items-center justify-between px-3 py-2.5 rounded-lg hover:bg-muted/50 border border-transparent hover:border-border/40 transition-all group"
                  >
                    <div>
                      <div className="text-xs font-medium text-foreground">{action.label}</div>
                      <div className="text-xs text-muted-foreground">{action.desc}</div>
                    </div>
                    <ArrowRight className="h-3.5 w-3.5 text-muted-foreground group-hover:text-pink-400 transition-colors" />
                  </Link>
                ))}
              </div>
            </div>

            <div className="bg-gradient-to-br from-pink-950/40 to-purple-950/30 border border-pink-800/30 rounded-xl p-5">
              <div className="text-xs font-semibold text-pink-300 mb-1">AI Copilot Ready</div>
              <p className="text-xs text-muted-foreground mb-3">
                Let AI source candidates, screen resumes, and schedule interviews automatically.
              </p>
              <Link
                href="/jobs"
                className="inline-flex items-center gap-1 text-xs text-pink-400 hover:text-pink-300 font-medium transition-colors"
              >
                Open a job to start <ArrowRight className="h-3 w-3" />
              </Link>
            </div>
          </div>
        </div>
      </main>
    </>
  );
}
