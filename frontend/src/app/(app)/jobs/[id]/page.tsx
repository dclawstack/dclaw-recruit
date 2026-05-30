"use client";

import React from "react";
import { useParams, useRouter } from "next/navigation";
import { AppHeader } from "@/components/app/app-header";
import { getJob, updateJob, listCandidates, type JobRequisition, type Candidate } from "@/lib/api";
import { Briefcase, MapPin, DollarSign, Users, Bot, CalendarDays, FileCheck, Loader2, ChevronLeft } from "lucide-react";
import { Button } from "@/components/ui/button";
import Link from "next/link";

type Tab = "overview" | "source" | "screen" | "schedule" | "scorecards";

const tabs: { id: Tab; label: string; icon: React.ElementType }[] = [
  { id: "overview", label: "Overview", icon: Briefcase },
  { id: "source", label: "AI Source", icon: Bot },
  { id: "screen", label: "AI Screen", icon: FileCheck },
  { id: "schedule", label: "Schedule", icon: CalendarDays },
  { id: "scorecards", label: "Scorecards", icon: Users },
];

export default function JobDetailPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [job, setJob] = React.useState<JobRequisition | null>(null);
  const [candidates, setCandidates] = React.useState<Candidate[]>([]);
  const [activeTab, setActiveTab] = React.useState<Tab>("overview");
  const [loading, setLoading] = React.useState(true);
  const [sourcing, setSourcing] = React.useState(false);
  const [sourceResults, setSourceResults] = React.useState<{ name: string; title: string; match_score: number; skills: string[]; outreach_message: string }[]>([]);

  React.useEffect(() => {
    async function load() {
      try {
        const [j, c] = await Promise.all([getJob(id), listCandidates({ job_id: id })]);
        setJob(j);
        setCandidates(c.items);
      } catch {
        // show empty state
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [id]);

  async function handleSource() {
    if (!job) return;
    setSourcing(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL || ""}/api/v1/ai/source`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ job_title: job.title, job_description: job.description || "", limit: 5 }),
      });
      if (res.ok) {
        const data = await res.json();
        setSourceResults(data.candidates || []);
      }
    } catch {
      setSourceResults([]);
    } finally {
      setSourcing(false);
    }
  }

  if (loading) {
    return (
      <>
        <AppHeader title="Job Details" />
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      </>
    );
  }

  if (!job) {
    return (
      <>
        <AppHeader title="Job Not Found" />
        <div className="flex flex-col items-center justify-center py-20 gap-4">
          <p className="text-muted-foreground text-sm">This job no longer exists.</p>
          <Button size="sm" onClick={() => router.push("/jobs")}>Back to Jobs</Button>
        </div>
      </>
    );
  }

  return (
    <>
      <AppHeader title={job.title} />
      <main className="flex-1 p-6 space-y-5">
        {/* Back */}
        <Link href="/jobs" className="inline-flex items-center gap-1 text-xs text-muted-foreground hover:text-foreground transition-colors">
          <ChevronLeft className="h-3 w-3" />
          Back to Jobs
        </Link>

        {/* Job meta */}
        <div className="bg-card/40 border border-border/50 rounded-xl p-5">
          <div className="flex items-start justify-between gap-4 flex-wrap">
            <div>
              <div className="flex items-center gap-2 mb-2 flex-wrap">
                <h2 className="text-lg font-bold text-foreground">{job.title}</h2>
                <span className={`text-xs px-2 py-0.5 rounded border ${
                  job.status === "open" ? "text-emerald-400 bg-emerald-950/50 border-emerald-800/30"
                  : job.status === "paused" ? "text-yellow-400 bg-yellow-950/50 border-yellow-800/30"
                  : "text-muted-foreground bg-muted/50 border-border/40"
                }`}>
                  {job.status}
                </span>
              </div>
              <div className="flex items-center flex-wrap gap-4 text-xs text-muted-foreground">
                {job.department && <span className="flex items-center gap-1"><Briefcase className="h-3 w-3" />{job.department}</span>}
                {job.location && <span className="flex items-center gap-1"><MapPin className="h-3 w-3" />{job.location}</span>}
                {job.salary_range && <span className="flex items-center gap-1"><DollarSign className="h-3 w-3" />{job.salary_range}</span>}
                <span className="flex items-center gap-1"><Users className="h-3 w-3" />{job.candidate_count} candidates</span>
              </div>
            </div>
            <Button
              size="sm"
              variant="outline"
              className="text-xs border-border/50 hover:border-pink-700/50"
              onClick={async () => {
                const newStatus = job.status === "open" ? "paused" : "open";
                const updated = await updateJob(id, { status: newStatus });
                setJob(updated);
              }}
            >
              {job.status === "open" ? "Pause Job" : "Reopen Job"}
            </Button>
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-1 bg-muted/30 p-1 rounded-xl border border-border/40 w-fit flex-wrap">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
                activeTab === tab.id
                  ? "bg-gradient-to-r from-pink-600 to-purple-600 text-white shadow-sm"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              <tab.icon className="h-3.5 w-3.5" />
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {activeTab === "overview" && (
          <div className="space-y-4">
            {job.description && (
              <div className="bg-card/40 border border-border/50 rounded-xl p-5">
                <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3">Description</h3>
                <p className="text-sm text-muted-foreground leading-relaxed whitespace-pre-wrap">{job.description}</p>
              </div>
            )}
            <div className="bg-card/40 border border-border/50 rounded-xl p-5">
              <h3 className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-3">
                Candidates ({candidates.length})
              </h3>
              {candidates.length === 0 ? (
                <p className="text-xs text-muted-foreground">No candidates yet. Use AI Source to find candidates.</p>
              ) : (
                <div className="space-y-2">
                  {candidates.map((c) => (
                    <div key={c.id} className="flex items-center justify-between px-3 py-2 rounded-lg bg-muted/30 border border-border/40">
                      <div>
                        <div className="text-sm font-medium text-foreground">{c.name}</div>
                        <div className="text-xs text-muted-foreground">{c.email}</div>
                      </div>
                      <span className="text-xs text-muted-foreground px-2 py-0.5 rounded bg-muted/60 border border-border/40">
                        {c.stage}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === "source" && (
          <div className="bg-card/40 border border-border/50 rounded-xl p-5 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-sm text-foreground">AI Sourcing Copilot</h3>
                <p className="text-xs text-muted-foreground mt-1">Find passive candidates across LinkedIn, GitHub, and job boards.</p>
              </div>
              <Button
                size="sm"
                disabled={sourcing}
                onClick={handleSource}
                className="bg-gradient-to-r from-pink-600 to-purple-600 text-white border-0 rounded-lg text-xs"
              >
                {sourcing ? <><Loader2 className="h-3 w-3 animate-spin mr-1" />Sourcing...</> : "Find Candidates"}
              </Button>
            </div>
            {sourceResults.length > 0 && (
              <div className="space-y-3 mt-4">
                {sourceResults.map((c, i) => (
                  <div key={i} className="border border-border/50 rounded-xl p-4 hover:border-pink-800/40 transition-all">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <div className="font-semibold text-sm text-foreground">{c.name}</div>
                        <div className="text-xs text-muted-foreground">{c.title}</div>
                        <div className="flex flex-wrap gap-1 mt-2">
                          {c.skills.slice(0, 4).map((s) => (
                            <span key={s} className="text-xs px-1.5 py-0.5 rounded bg-muted/60 border border-border/40 text-muted-foreground">{s}</span>
                          ))}
                        </div>
                      </div>
                      <div className="text-right shrink-0">
                        <div className="text-lg font-bold text-pink-400">{Math.round(c.match_score * 100)}%</div>
                        <div className="text-xs text-muted-foreground">match</div>
                      </div>
                    </div>
                    {c.outreach_message && (
                      <div className="mt-3 p-3 bg-muted/30 rounded-lg border border-border/40 text-xs text-muted-foreground italic">
                        &ldquo;{c.outreach_message}&rdquo;
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
            {!sourcing && sourceResults.length === 0 && (
              <div className="text-center py-8">
                <Bot className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
                <p className="text-xs text-muted-foreground">Click &ldquo;Find Candidates&rdquo; to start AI sourcing.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === "screen" && (
          <div className="bg-card/40 border border-border/50 rounded-xl p-5">
            <h3 className="font-semibold text-sm text-foreground mb-1">AI Resume Screening</h3>
            <p className="text-xs text-muted-foreground mb-4">Upload resumes to automatically rank candidates by fit, skills, and experience.</p>
            <div className="border-2 border-dashed border-border/40 rounded-xl p-8 text-center hover:border-pink-800/40 transition-all cursor-pointer">
              <FileCheck className="h-10 w-10 text-muted-foreground/30 mx-auto mb-3" />
              <p className="text-xs text-muted-foreground">Drop resume files here or click to upload</p>
              <p className="text-xs text-muted-foreground/50 mt-1">Supports PDF, DOCX · Bulk screening up to 100 resumes</p>
            </div>
          </div>
        )}

        {activeTab === "schedule" && (
          <div className="bg-card/40 border border-border/50 rounded-xl p-5">
            <h3 className="font-semibold text-sm text-foreground mb-1">Interview Scheduling</h3>
            <p className="text-xs text-muted-foreground mb-4">Schedule interviews with one-click coordination and calendar sync.</p>
            <div className="grid sm:grid-cols-2 gap-3">
              {["Mon Jun 2", "Tue Jun 3", "Wed Jun 4", "Thu Jun 5"].map((day) => (
                <div key={day} className="border border-border/50 rounded-xl p-3">
                  <div className="text-xs font-semibold text-foreground mb-2">{day}</div>
                  {["10:00 AM", "2:00 PM", "4:00 PM"].map((time) => (
                    <button
                      key={time}
                      className="w-full text-left text-xs text-muted-foreground px-2 py-1.5 rounded hover:bg-pink-950/40 hover:text-pink-300 hover:border-pink-800/30 border border-transparent transition-all mb-1"
                    >
                      {time}
                    </button>
                  ))}
                </div>
              ))}
            </div>
            <Button size="sm" className="mt-4 bg-gradient-to-r from-pink-600 to-purple-600 text-white border-0 rounded-lg text-xs">
              Send Scheduling Link to Candidate
            </Button>
          </div>
        )}

        {activeTab === "scorecards" && (
          <div className="bg-card/40 border border-border/50 rounded-xl p-5">
            <h3 className="font-semibold text-sm text-foreground mb-1">Interview Scorecards</h3>
            <p className="text-xs text-muted-foreground mb-4">Structured evaluation templates with rubrics and weighted scoring.</p>
            <div className="space-y-3">
              {[
                { category: "Technical Skills", weight: 0.4, score: 4.2 },
                { category: "Communication", weight: 0.25, score: 3.8 },
                { category: "Problem Solving", weight: 0.2, score: 4.5 },
                { category: "Culture Fit", weight: 0.15, score: 4.0 },
              ].map((row) => (
                <div key={row.category} className="flex items-center gap-3">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-xs text-foreground">{row.category}</span>
                      <span className="text-xs text-muted-foreground">{Math.round(row.weight * 100)}% weight</span>
                    </div>
                    <div className="h-1.5 bg-border/30 rounded-full">
                      <div
                        className="h-1.5 rounded-full bg-gradient-to-r from-pink-500 to-purple-500"
                        style={{ width: `${(row.score / 5) * 100}%` }}
                      />
                    </div>
                  </div>
                  <div className="text-sm font-bold text-foreground shrink-0">{row.score}</div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-gradient-to-br from-pink-950/30 to-purple-950/20 border border-pink-800/30 rounded-xl text-xs">
              <span className="text-muted-foreground">Composite Score: </span>
              <span className="text-pink-300 font-bold text-base">4.2/5</span>
              <span className="text-muted-foreground ml-2">— Strong Hire</span>
            </div>
          </div>
        )}
      </main>
    </>
  );
}
