const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function fetchJson<T>(path: string, options?: RequestInit): Promise<T> {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
    ...options,
  });
  if (!response.ok) {
    const error = await response.text();
    throw new ApiError(`API error ${response.status}: ${error}`, response.status);
  }
  return response.json();
}

export async function getHealth() {
  return fetchJson<{ status: string }>("/health/");
}

// ── Types ────────────────────────────────────────────────────────

export interface JobRequisition {
  id: string;
  title: string;
  department: string | null;
  location: string | null;
  salary_range: string | null;
  description: string | null;
  status: "open" | "paused" | "closed";
  created_at: string;
  updated_at: string;
  candidate_count: number;
}

export interface Candidate {
  id: string;
  name: string;
  email: string;
  phone: string | null;
  resume_url: string | null;
  source: string | null;
  stage: "applied" | "screening" | "interview" | "offer" | "hired" | "rejected";
  job_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface Interview {
  id: string;
  candidate_id: string;
  job_id: string | null;
  scheduled_at: string | null;
  interviewer: string | null;
  feedback: string | null;
  rating: number | null;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

// ── Jobs API ─────────────────────────────────────────────────────

export async function listJobs(params?: {
  query?: string;
  status?: string;
  limit?: number;
  offset?: number;
}) {
  const sp = new URLSearchParams();
  if (params?.query) sp.set("query", params.query);
  if (params?.status) sp.set("status", params.status);
  if (params?.limit) sp.set("limit", String(params.limit));
  if (params?.offset) sp.set("offset", String(params.offset));
  const qs = sp.toString();
  return fetchJson<PaginatedResponse<JobRequisition>>(`/api/v1/jobs${qs ? `?${qs}` : ""}`);
}

export async function createJob(data: {
  title: string;
  department?: string;
  location?: string;
  salary_range?: string;
  description?: string;
  status?: string;
}) {
  return fetchJson<JobRequisition>("/api/v1/jobs", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getJob(id: string) {
  return fetchJson<JobRequisition>(`/api/v1/jobs/${id}`);
}

export async function updateJob(id: string, data: Record<string, unknown>) {
  return fetchJson<JobRequisition>(`/api/v1/jobs/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function deleteJob(id: string) {
  await fetch(`${API_BASE}/api/v1/jobs/${id}`, { method: "DELETE" });
}

// ── Candidates API ───────────────────────────────────────────────

export async function listCandidates(params?: {
  query?: string;
  stage?: string;
  job_id?: string;
  limit?: number;
  offset?: number;
}) {
  const sp = new URLSearchParams();
  if (params?.query) sp.set("query", params.query);
  if (params?.stage) sp.set("stage", params.stage);
  if (params?.job_id) sp.set("job_id", params.job_id);
  if (params?.limit) sp.set("limit", String(params.limit));
  if (params?.offset) sp.set("offset", String(params.offset));
  const qs = sp.toString();
  return fetchJson<PaginatedResponse<Candidate>>(`/api/v1/candidates${qs ? `?${qs}` : ""}`);
}

export async function createCandidate(data: {
  name: string;
  email: string;
  phone?: string;
  resume_url?: string;
  source?: string;
  stage?: string;
  job_id?: string;
}) {
  return fetchJson<Candidate>("/api/v1/candidates", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getCandidate(id: string) {
  return fetchJson<Candidate>(`/api/v1/candidates/${id}`);
}

export async function updateCandidate(id: string, data: Record<string, unknown>) {
  return fetchJson<Candidate>(`/api/v1/candidates/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function deleteCandidate(id: string) {
  await fetch(`${API_BASE}/api/v1/candidates/${id}`, { method: "DELETE" });
}

// ── Interviews API ───────────────────────────────────────────────

export async function listInterviews(params?: {
  candidate_id?: string;
  job_id?: string;
  limit?: number;
  offset?: number;
}) {
  const sp = new URLSearchParams();
  if (params?.candidate_id) sp.set("candidate_id", params.candidate_id);
  if (params?.job_id) sp.set("job_id", params.job_id);
  if (params?.limit) sp.set("limit", String(params.limit));
  if (params?.offset) sp.set("offset", String(params.offset));
  const qs = sp.toString();
  return fetchJson<PaginatedResponse<Interview>>(`/api/v1/interviews${qs ? `?${qs}` : ""}`);
}

export async function createInterview(data: {
  candidate_id: string;
  job_id?: string;
  scheduled_at?: string;
  interviewer?: string;
  feedback?: string;
  rating?: number;
}) {
  return fetchJson<Interview>("/api/v1/interviews", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getInterview(id: string) {
  return fetchJson<Interview>(`/api/v1/interviews/${id}`);
}

export async function updateInterview(id: string, data: Record<string, unknown>) {
  return fetchJson<Interview>(`/api/v1/interviews/${id}`, {
    method: "PATCH",
    body: JSON.stringify(data),
  });
}

export async function deleteInterview(id: string) {
  await fetch(`${API_BASE}/api/v1/interviews/${id}`, { method: "DELETE" });
}

export { ApiError };
