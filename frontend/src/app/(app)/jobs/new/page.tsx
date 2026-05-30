"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { AppHeader } from "@/components/app/app-header";
import { createJob } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Loader2 } from "lucide-react";

export default function NewJobPage() {
  const router = useRouter();
  const [saving, setSaving] = React.useState(false);
  const [error, setError] = React.useState("");
  const [form, setForm] = React.useState({
    title: "",
    department: "",
    location: "",
    salary_range: "",
    status: "open",
    description: "",
  });

  function set(key: string, val: string) {
    setForm((f) => ({ ...f, [key]: val }));
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!form.title.trim()) {
      setError("Job title is required.");
      return;
    }
    setSaving(true);
    setError("");
    try {
      const job = await createJob({
        title: form.title,
        department: form.department || undefined,
        location: form.location || undefined,
        salary_range: form.salary_range || undefined,
        description: form.description || undefined,
        status: form.status,
      });
      router.push(`/jobs/${job.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create job. Check API connection.");
      setSaving(false);
    }
  }

  return (
    <>
      <AppHeader title="New Job Posting" />
      <main className="flex-1 p-6">
        <div className="max-w-2xl mx-auto">
          <div className="bg-card/40 border border-border/50 rounded-xl p-6">
            <h2 className="font-semibold text-base text-foreground mb-1">Job Details</h2>
            <p className="text-xs text-muted-foreground mb-6">Fill in the requisition details. AI will help you source and screen candidates.</p>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="space-y-1.5">
                <Label htmlFor="title" className="text-xs text-muted-foreground">Job Title *</Label>
                <Input
                  id="title"
                  placeholder="e.g. Senior Backend Engineer"
                  value={form.title}
                  onChange={(e) => set("title", e.target.value)}
                  className="bg-muted/30 border-border/50 h-9 text-sm"
                />
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label htmlFor="dept" className="text-xs text-muted-foreground">Department</Label>
                  <Input
                    id="dept"
                    placeholder="e.g. Engineering"
                    value={form.department}
                    onChange={(e) => set("department", e.target.value)}
                    className="bg-muted/30 border-border/50 h-9 text-sm"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="location" className="text-xs text-muted-foreground">Location</Label>
                  <Input
                    id="location"
                    placeholder="e.g. Remote / SF"
                    value={form.location}
                    onChange={(e) => set("location", e.target.value)}
                    className="bg-muted/30 border-border/50 h-9 text-sm"
                  />
                </div>
              </div>

              <div className="grid sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label htmlFor="salary" className="text-xs text-muted-foreground">Salary Range</Label>
                  <Input
                    id="salary"
                    placeholder="e.g. $120k–$160k"
                    value={form.salary_range}
                    onChange={(e) => set("salary_range", e.target.value)}
                    className="bg-muted/30 border-border/50 h-9 text-sm"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="status" className="text-xs text-muted-foreground">Status</Label>
                  <select
                    id="status"
                    value={form.status}
                    onChange={(e) => set("status", e.target.value)}
                    className="w-full h-9 rounded-md border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-pink-600"
                  >
                    <option value="open">Open</option>
                    <option value="paused">Paused</option>
                    <option value="closed">Closed</option>
                  </select>
                </div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="desc" className="text-xs text-muted-foreground">Job Description</Label>
                <textarea
                  id="desc"
                  rows={6}
                  placeholder="Describe the role, requirements, and what makes it exciting..."
                  value={form.description}
                  onChange={(e) => set("description", e.target.value)}
                  className="w-full rounded-md border border-border/50 bg-muted/30 px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-pink-600 resize-none"
                />
              </div>

              {error && (
                <div className="text-xs text-red-400 bg-red-950/30 border border-red-800/30 rounded-lg px-3 py-2">
                  {error}
                </div>
              )}

              <div className="flex items-center gap-3 pt-2">
                <Button
                  type="submit"
                  disabled={saving}
                  className="bg-gradient-to-r from-pink-600 to-purple-600 hover:from-pink-500 hover:to-purple-500 text-white border-0 rounded-lg h-9 px-6 text-sm"
                >
                  {saving ? (
                    <>
                      <Loader2 className="h-3.5 w-3.5 animate-spin mr-2" />
                      Creating...
                    </>
                  ) : (
                    "Create Job Posting"
                  )}
                </Button>
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => router.back()}
                  className="text-muted-foreground"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </div>
      </main>
    </>
  );
}
