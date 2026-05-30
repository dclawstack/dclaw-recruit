"use client";

import React from "react";
import { AppHeader } from "@/components/app/app-header";
import { listInterviews, createInterview, listCandidates, deleteInterview, type Interview, type Candidate } from "@/lib/api";
import { CalendarDays, Loader2, Plus, Trash2, User, Clock } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export default function InterviewsPage() {
  const [interviews, setInterviews] = React.useState<Interview[]>([]);
  const [candidates, setCandidates] = React.useState<Candidate[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [showForm, setShowForm] = React.useState(false);
  const [saving, setSaving] = React.useState(false);
  const [form, setForm] = React.useState({
    candidate_id: "",
    scheduled_at: "",
    interviewer: "",
    feedback: "",
    rating: "",
  });

  async function load() {
    setLoading(true);
    try {
      const [iv, ca] = await Promise.all([listInterviews({ limit: 50 }), listCandidates({ limit: 100 })]);
      setInterviews(iv.items);
      setCandidates(ca.items);
    } catch {
      setInterviews([]);
    } finally {
      setLoading(false);
    }
  }

  React.useEffect(() => { load(); }, []);

  function setField(k: string, v: string) {
    setForm((f) => ({ ...f, [k]: v }));
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!form.candidate_id) return;
    setSaving(true);
    try {
      await createInterview({
        candidate_id: form.candidate_id,
        scheduled_at: form.scheduled_at || undefined,
        interviewer: form.interviewer || undefined,
        feedback: form.feedback || undefined,
        rating: form.rating ? Number(form.rating) : undefined,
      });
      setShowForm(false);
      setForm({ candidate_id: "", scheduled_at: "", interviewer: "", feedback: "", rating: "" });
      await load();
    } finally {
      setSaving(false);
    }
  }

  async function handleDelete(id: string) {
    if (!confirm("Remove this interview?")) return;
    await deleteInterview(id);
    setInterviews((prev) => prev.filter((i) => i.id !== id));
  }

  function getCandidateName(id: string) {
    return candidates.find((c) => c.id === id)?.name || id.slice(0, 8) + "…";
  }

  return (
    <>
      <AppHeader title="Interviews" />
      <main className="flex-1 p-6 space-y-5">
        {/* Schedule form */}
        <div className="bg-card/40 border border-border/50 rounded-xl overflow-hidden">
          <button
            onClick={() => setShowForm(!showForm)}
            className="w-full flex items-center justify-between px-5 py-4 hover:bg-muted/20 transition-colors"
          >
            <div className="flex items-center gap-2">
              <Plus className="h-4 w-4 text-pink-400" />
              <span className="text-sm font-medium text-foreground">Schedule New Interview</span>
            </div>
            <span className="text-xs text-muted-foreground">{showForm ? "Close" : "Open"}</span>
          </button>

          {showForm && (
            <form onSubmit={handleCreate} className="px-5 pb-5 pt-1 border-t border-border/50 space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <Label className="text-xs text-muted-foreground">Candidate *</Label>
                  <select
                    value={form.candidate_id}
                    onChange={(e) => setField("candidate_id", e.target.value)}
                    required
                    className="w-full h-9 rounded-md border border-border/50 bg-muted/30 px-3 text-sm text-foreground focus:outline-none focus:ring-1 focus:ring-pink-600"
                  >
                    <option value="">Select candidate...</option>
                    {candidates.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>
                <div className="space-y-1.5">
                  <Label className="text-xs text-muted-foreground">Scheduled At</Label>
                  <Input
                    type="datetime-local"
                    value={form.scheduled_at}
                    onChange={(e) => setField("scheduled_at", e.target.value)}
                    className="bg-muted/30 border-border/50 h-9 text-sm"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-xs text-muted-foreground">Interviewer</Label>
                  <Input
                    placeholder="e.g. Jane Smith"
                    value={form.interviewer}
                    onChange={(e) => setField("interviewer", e.target.value)}
                    className="bg-muted/30 border-border/50 h-9 text-sm"
                  />
                </div>
                <div className="space-y-1.5">
                  <Label className="text-xs text-muted-foreground">Rating (1–5)</Label>
                  <Input
                    type="number"
                    min="1"
                    max="5"
                    step="0.1"
                    placeholder="4.2"
                    value={form.rating}
                    onChange={(e) => setField("rating", e.target.value)}
                    className="bg-muted/30 border-border/50 h-9 text-sm"
                  />
                </div>
              </div>
              <div className="space-y-1.5">
                <Label className="text-xs text-muted-foreground">Feedback Notes</Label>
                <textarea
                  rows={3}
                  placeholder="Interview notes, observations..."
                  value={form.feedback}
                  onChange={(e) => setField("feedback", e.target.value)}
                  className="w-full rounded-md border border-border/50 bg-muted/30 px-3 py-2 text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-pink-600 resize-none"
                />
              </div>
              <div className="flex gap-3">
                <Button
                  type="submit"
                  disabled={saving || !form.candidate_id}
                  size="sm"
                  className="bg-gradient-to-r from-pink-600 to-purple-600 text-white border-0 rounded-lg text-xs"
                >
                  {saving ? <><Loader2 className="h-3 w-3 animate-spin mr-1" />Saving...</> : "Schedule Interview"}
                </Button>
                <Button type="button" variant="ghost" size="sm" onClick={() => setShowForm(false)} className="text-xs text-muted-foreground">
                  Cancel
                </Button>
              </div>
            </form>
          )}
        </div>

        {/* List */}
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : interviews.length === 0 ? (
          <div className="text-center py-16">
            <CalendarDays className="h-12 w-12 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-muted-foreground text-sm">No interviews scheduled yet</p>
          </div>
        ) : (
          <div className="space-y-2">
            {interviews.map((iv) => (
              <div key={iv.id} className="bg-card/40 border border-border/50 rounded-xl p-4 flex items-start justify-between gap-4 hover:border-pink-800/40 transition-all group">
                <div className="flex items-start gap-3">
                  <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-950/60 to-blue-900/20 border border-blue-800/30 flex items-center justify-center shrink-0">
                    <CalendarDays className="h-4 w-4 text-blue-400" />
                  </div>
                  <div>
                    <div className="font-semibold text-sm text-foreground flex items-center gap-2">
                      <User className="h-3.5 w-3.5 text-muted-foreground" />
                      {getCandidateName(iv.candidate_id)}
                    </div>
                    <div className="flex items-center flex-wrap gap-3 mt-1 text-xs text-muted-foreground">
                      {iv.scheduled_at && (
                        <span className="flex items-center gap-1">
                          <Clock className="h-3 w-3" />
                          {new Date(iv.scheduled_at).toLocaleString()}
                        </span>
                      )}
                      {iv.interviewer && <span>with {iv.interviewer}</span>}
                      {iv.rating && (
                        <span className="text-pink-400 font-semibold">{iv.rating}/5 ★</span>
                      )}
                    </div>
                    {iv.feedback && (
                      <p className="text-xs text-muted-foreground/70 mt-1.5 italic line-clamp-2">{iv.feedback}</p>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => handleDelete(iv.id)}
                  className="p-1.5 rounded-lg text-transparent group-hover:text-muted-foreground hover:!text-red-400 hover:bg-red-950/20 transition-all"
                >
                  <Trash2 className="h-3.5 w-3.5" />
                </button>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
