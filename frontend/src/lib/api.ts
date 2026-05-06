export interface JobPost {
  id: string;
  title: string;
  description: string;
  candidate_pool_size: number;
  top_candidate_match: string;
  time_to_fill_days: number;
  created_at: string;
}

export interface Candidate {
  id: string;
  name: string;
  match_score: number;
  rank: number;
}

export async function api<T>(
  path: string,
  options?: RequestInit
): Promise<T> {
  const res = await fetch(`/api/v1${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });
  if (!res.ok) {
    throw new Error(`API error: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}
