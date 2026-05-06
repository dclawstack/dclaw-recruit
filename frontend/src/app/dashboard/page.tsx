"use client";

import { useState } from "react";
import { api, JobPost } from "@/lib/api";

export default function Dashboard() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<JobPost | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    try {
      const job = await api<JobPost>("/jobs", {
        method: "POST",
        body: JSON.stringify({ title, description }),
      });
      setResult(job);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto px-4 py-12">
      <h2 className="text-2xl font-semibold text-gray-800 mb-6">Recruit Dashboard</h2>
      <form onSubmit={handleSubmit} className="space-y-4 mb-8">
        <div>
          <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
            Job title
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand"
          />
        </div>
        <div>
          <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
            Job description
          </label>
          <textarea
            id="description"
            rows={4}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            required
            className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-brand"
          />
        </div>
        <button
          type="submit"
          disabled={loading}
          className="inline-flex items-center justify-center px-5 py-2.5 text-white bg-brand rounded-lg hover:opacity-90 transition-opacity disabled:opacity-60"
        >
          {loading ? "Posting..." : "Post & Rank"}
        </button>
      </form>

      {result && (
        <div className="bg-white rounded-lg shadow p-6 space-y-3">
          <h3 className="text-lg font-semibold text-gray-800">Mock Results</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <span className="text-xs uppercase tracking-wide text-gray-500">Job ID</span>
              <p className="text-sm font-medium text-gray-900">{result.id}</p>
            </div>
            <div>
              <span className="text-xs uppercase tracking-wide text-gray-500">Candidate pool size</span>
              <p className="text-sm font-medium text-gray-900">{result.candidate_pool_size}</p>
            </div>
            <div>
              <span className="text-xs uppercase tracking-wide text-gray-500">Top candidate match</span>
              <p className="text-sm font-medium text-gray-900">{result.top_candidate_match}</p>
            </div>
            <div>
              <span className="text-xs uppercase tracking-wide text-gray-500">Time to fill estimate</span>
              <p className="text-sm font-medium text-gray-900">{result.time_to_fill_days} days</p>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
