"use client";

import React from "react";
import Link from "next/link";
import { AppHeader } from "@/components/app/app-header";
import { listJobs, deleteJob, type JobRequisition } from "@/lib/api";
import { Search, Briefcase, MapPin, DollarSign, Users, Trash2, ExternalLink, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

const statusColors: Record<string, string> = {
  open: "text-emerald-400 bg-emerald-950/50 border-emerald-800/30",
  paused: "text-yellow-400 bg-yellow-950/50 border-yellow-800/30",
  closed: "text-muted-foreground bg-muted/50 border-border/40",
};

export default function JobsPage() {
  const [jobs, setJobs] = React.useState<JobRequisition[]>([]);
  const [total, setTotal] = React.useState(0);
  const [query, setQuery] = React.useState("");
  const [status, setStatus] = React.useState("");
  const [loading, setLoading] = React.useState(true);
  const [deleting, setDeleting] = React.useState<string | null>(null);

  const load = React.useCallback(async () => {
    setLoading(true);
    try {
      const res = await listJobs({ query: query || undefined, status: status || undefined });
      setJobs(res.items);
      setTotal(res.total);
    } catch {
      setJobs([]);
    } finally {
      setLoading(false);
    }
  }, [query, status]);

  React.useEffect(() => {
    const t = setTimeout(load, 300);
    return () => clearTimeout(t);
  }, [load]);

  async function handleDelete(id: string) {
    if (!confirm("Delete this job posting?")) return;
    setDeleting(id);
    try {
      await deleteJob(id);
      await load();
    } finally {
      setDeleting(null);
    }
  }

  return (
    <>
      <AppHeader title="Jobs" action={{ label: "New Job", href: "/jobs/new" }} />
      <main className="flex-1 p-6 space-y-5">
        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1 max-w-sm">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search jobs..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="pl-9 bg-card/40 border-border/50 h-9 text-sm"
            />
          </div>
          <div className="flex gap-2">
            {["", "open", "paused", "closed"].map((s) => (
              <button
                key={s}
                onClick={() => setStatus(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all border ${
                  status === s
                    ? "bg-gradient-to-r from-pink-600 to-purple-600 text-white border-transparent"
                    : "border-border/50 text-muted-foreground hover:text-foreground hover:border-border"
                }`}
              >
                {s === "" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
              </button>
            ))}
          </div>
        </div>

        {/* Count */}
        <div className="text-xs text-muted-foreground">{total} job{total !== 1 ? "s" : ""}</div>

        {/* Table */}
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : jobs.length === 0 ? (
          <div className="text-center py-20">
            <Briefcase className="h-12 w-12 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-muted-foreground text-sm mb-4">No jobs yet</p>
            <Button size="sm" className="bg-gradient-to-r from-pink-600 to-purple-600 text-white border-0" asChild>
              <Link href="/jobs/new">Post your first job</Link>
            </Button>
          </div>
        ) : (
          <div className="space-y-2">
            {jobs.map((job) => (
              <div
                key={job.id}
                className="bg-card/40 border border-border/50 rounded-xl p-4 hover:border-pink-800/40 transition-all group"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-4 min-w-0">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-pink-950/60 to-purple-950/40 border border-pink-800/30 flex items-center justify-center shrink-0">
                      <Briefcase className="h-4 w-4 text-pink-400" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <Link
                          href={`/jobs/${job.id}`}
                          className="font-semibold text-sm text-foreground hover:text-pink-300 transition-colors"
                        >
                          {job.title}
                        </Link>
                        <span className={`text-xs px-2 py-0.5 rounded border ${statusColors[job.status] || statusColors.closed}`}>
                          {job.status}
                        </span>
                      </div>
                      <div className="flex items-center flex-wrap gap-3 mt-1.5 text-xs text-muted-foreground">
                        {job.department && (
                          <span className="flex items-center gap-1">
                            <Briefcase className="h-3 w-3" />
                            {job.department}
                          </span>
                        )}
                        {job.location && (
                          <span className="flex items-center gap-1">
                            <MapPin className="h-3 w-3" />
                            {job.location}
                          </span>
                        )}
                        {job.salary_range && (
                          <span className="flex items-center gap-1">
                            <DollarSign className="h-3 w-3" />
                            {job.salary_range}
                          </span>
                        )}
                        <span className="flex items-center gap-1">
                          <Users className="h-3 w-3" />
                          {job.candidate_count} candidate{job.candidate_count !== 1 ? "s" : ""}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <Link
                      href={`/jobs/${job.id}`}
                      className="p-1.5 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all"
                    >
                      <ExternalLink className="h-3.5 w-3.5" />
                    </Link>
                    <button
                      onClick={() => handleDelete(job.id)}
                      disabled={deleting === job.id}
                      className="p-1.5 rounded-lg text-muted-foreground hover:text-red-400 hover:bg-red-950/20 transition-all"
                    >
                      {deleting === job.id ? (
                        <Loader2 className="h-3.5 w-3.5 animate-spin" />
                      ) : (
                        <Trash2 className="h-3.5 w-3.5" />
                      )}
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
