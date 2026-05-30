"use client";

import React from "react";
import { AppHeader } from "@/components/app/app-header";
import { listCandidates, updateCandidate, deleteCandidate, type Candidate } from "@/lib/api";
import { Users, Loader2, Trash2, Mail } from "lucide-react";

const STAGES = ["applied", "screening", "interview", "offer", "hired", "rejected"] as const;
type Stage = typeof STAGES[number];

const stageColors: Record<Stage, string> = {
  applied: "border-blue-800/30 text-blue-300 bg-blue-950/50",
  screening: "border-purple-800/30 text-purple-300 bg-purple-950/50",
  interview: "border-pink-800/30 text-pink-300 bg-pink-950/50",
  offer: "border-yellow-800/30 text-yellow-300 bg-yellow-950/50",
  hired: "border-emerald-800/30 text-emerald-300 bg-emerald-950/50",
  rejected: "border-red-800/30 text-red-300/60 bg-red-950/30",
};

const stageLabels: Record<Stage, string> = {
  applied: "Applied",
  screening: "Screening",
  interview: "Interview",
  offer: "Offer",
  hired: "Hired",
  rejected: "Rejected",
};

export default function CandidatesPage() {
  const [candidates, setCandidates] = React.useState<Candidate[]>([]);
  const [loading, setLoading] = React.useState(true);
  const [dragging, setDragging] = React.useState<string | null>(null);

  async function load() {
    setLoading(true);
    try {
      const res = await listCandidates({ limit: 100 });
      setCandidates(res.items);
    } catch {
      setCandidates([]);
    } finally {
      setLoading(false);
    }
  }

  React.useEffect(() => { load(); }, []);

  async function moveTo(candidateId: string, stage: Stage) {
    try {
      await updateCandidate(candidateId, { stage });
      setCandidates((prev) => prev.map((c) => c.id === candidateId ? { ...c, stage } : c));
    } catch {}
  }

  async function handleDelete(id: string) {
    if (!confirm("Remove this candidate?")) return;
    try {
      await deleteCandidate(id);
      setCandidates((prev) => prev.filter((c) => c.id !== id));
    } catch {}
  }

  const byStage = STAGES.slice(0, 5).reduce((acc, stage) => {
    acc[stage] = candidates.filter((c) => c.stage === stage);
    return acc;
  }, {} as Record<Stage, Candidate[]>);

  return (
    <>
      <AppHeader title="Candidate Pipeline" />
      <main className="flex-1 p-6">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
          </div>
        ) : candidates.length === 0 ? (
          <div className="text-center py-20">
            <Users className="h-12 w-12 text-muted-foreground/30 mx-auto mb-4" />
            <p className="text-muted-foreground text-sm mb-2">No candidates yet</p>
            <p className="text-xs text-muted-foreground/60">Open a job and use AI Source to find candidates.</p>
          </div>
        ) : (
          <div className="flex gap-4 overflow-x-auto pb-4">
            {(STAGES.slice(0, 5) as Stage[]).map((stage) => (
              <div
                key={stage}
                className="shrink-0 w-60"
                onDragOver={(e) => e.preventDefault()}
                onDrop={() => {
                  if (dragging) moveTo(dragging, stage);
                  setDragging(null);
                }}
              >
                {/* Column header */}
                <div className={`flex items-center justify-between px-3 py-2 rounded-lg border text-xs font-semibold mb-3 ${stageColors[stage]}`}>
                  <span>{stageLabels[stage]}</span>
                  <span className="opacity-70">{byStage[stage].length}</span>
                </div>

                {/* Cards */}
                <div className="space-y-2 min-h-[100px]">
                  {byStage[stage].map((c) => (
                    <div
                      key={c.id}
                      draggable
                      onDragStart={() => setDragging(c.id)}
                      onDragEnd={() => setDragging(null)}
                      className={`bg-card/60 border border-border/50 rounded-xl p-3 cursor-grab active:cursor-grabbing hover:border-pink-800/40 transition-all group ${dragging === c.id ? "opacity-40" : ""}`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="min-w-0">
                          <div className="text-xs font-semibold text-foreground truncate">{c.name}</div>
                          <div className="flex items-center gap-1 mt-0.5 text-xs text-muted-foreground truncate">
                            <Mail className="h-2.5 w-2.5 shrink-0" />
                            <span className="truncate">{c.email}</span>
                          </div>
                          {c.source && (
                            <div className="text-xs text-muted-foreground/60 mt-1 truncate">via {c.source}</div>
                          )}
                        </div>
                        <button
                          onClick={() => handleDelete(c.id)}
                          className="shrink-0 p-1 rounded text-transparent group-hover:text-muted-foreground hover:!text-red-400 hover:bg-red-950/20 transition-all"
                        >
                          <Trash2 className="h-3 w-3" />
                        </button>
                      </div>

                      {/* Move buttons */}
                      <div className="flex gap-1 mt-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        {STAGES.slice(0, 5).filter((s) => s !== stage).map((s) => (
                          <button
                            key={s}
                            onClick={() => moveTo(c.id, s)}
                            title={`Move to ${stageLabels[s]}`}
                            className={`flex-1 text-[9px] py-0.5 rounded border transition-all hover:opacity-100 ${stageColors[s]}`}
                          >
                            {stageLabels[s].slice(0, 3)}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </>
  );
}
