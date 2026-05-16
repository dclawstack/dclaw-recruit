# DClaw Recruit — v1.2 Feature Roadmap

> 📘 **REVISED PRD v2.3 available:** See `REVISED-PRD.md` for complete gap analysis, current state, and full feature roadmap.


> Based on: Y Combinator vertical SaaS principles, trending GitHub repos (erpnext-hiring, greenhouse), AI product research (Greenhouse, Lever, Ashby, Mercor)

## Pre-Flight Checklist

- [ ] `frontend/package-lock.json` committed after any `npm install` / dependency change
- [ ] `frontend/next-env.d.ts` exists and is committed
- [ ] `docker-compose.yml` healthchecks correct
- [ ] `frontend/Dockerfile` declares `ARG NEXT_PUBLIC_API_URL` before `RUN npm run build`

## v1.0 Feature Inventory (Current)

- [ ] Job posting CRUD
- [ ] Candidate pipeline (stages)
- [ ] Resume parsing & profiles
- [ ] Interview scheduling
- [ ] Real backend CRUD (no mocks)
- [ ] Docker + Helm deployment
- [ ] Alembic migrations
- [ ] Backend tests

---

## v1.2 Roadmap

### P0 — Must Have (Ship in v1.0, demo-ready)

#### 1. AI Recruiting Copilot (Sourcing Agent)
**Description:** AI agent that finds candidates across LinkedIn, GitHub, and job boards based on job requirements. Generates personalized outreach messages.
- **AI Angle:** Profile matching via embeddings. LLM-generated outreach.
- **Backend:** `/api/v1/ai/source` endpoint. Profile scraping + scoring.
- **Frontend:** Sourcing panel with candidate cards and one-click outreach.
- **Files:** `backend/app/services/sourcing_ai.py`, `frontend/src/app/jobs/[id]/source.tsx`

#### 2. AI Resume Screening & Ranking
**Description:** Auto-parse resumes and rank candidates against job description. Explain match score.
- **AI Angle:** Resume parsing (LLM/regex). Semantic JD-candidate matching (embeddings).
- **Backend:** `/api/v1/ai/screen` endpoint. Bias detection filters.
- **Frontend:** Ranked candidate list with match scores and explanation.
- **Files:** `backend/app/services/screening.py`

#### 3. Interview Scheduling & Coordination
**Description:** Self-scheduling links, calendar sync, reminder sequences, room booking.
- **Backend:** Calendar API integration. Availability calculation.
- **Frontend:** Scheduling widget. Interview calendar.
- **Files:** `backend/app/services/scheduling.py`

#### 4. Structured Interview Scorecards
**Description:** Standardized scorecards with rubrics. Compare candidates side-by-side.
- **Backend:** Scorecard template engine. Aggregate scoring.
- **Frontend:** Scorecard form during/after interview. Comparison matrix.
- **Files:** `backend/app/services/scorecards.py`

### P1 — Should Have (v1.1–1.2)

#### 5. AI Interview Coach (Async Video Interviews)
**Description:** Candidates record video answers. AI analyzes communication, sentiment, and content.
- **AI Angle:** Video analysis (VLM) + transcript analysis (LLM).
- **Backend:** Async video processing pipeline.
- **Frontend:** Video recorder + AI insights panel.

#### 6. Offer Management & E-Sign
**Description:** Generate offer letters, approval workflows, e-signature, background check trigger.
- **Backend:** Document generation. E-sign webhook handling.
- **Frontend:** Offer builder. Approval chain view.

#### 7. Talent Pool & CRM
**Description:** Nurture passive candidates with drip campaigns and talent communities.
- **Backend:** Candidate tagging. Engagement tracking.
- **Frontend:** Talent pool board. Engagement timeline.

#### 8. Job Board Syndication
**Description:** Post to LinkedIn, Indeed, Glassdoor, niche boards from one interface.
- **Backend:** Job board API integrations.
- **Frontend:** Syndication checklist with status.

### P2 — Could Have (v1.3+)

#### 9. AI-Generated Job Descriptions
**Description:** AI writes optimized JDs based on role requirements and market data.

#### 10. Diversity Analytics
**Description:** Track diversity metrics across pipeline stages. Identify bias points.

#### 11. Employee Referral Portal
**Description:** Internal referral submission with tracking, rewards, and leaderboards.

#### 12. Predictive Time-to-Hire
**Description:** AI predicts how long each role will take to fill based on historical data.

---

## Implementation Priority

1. **Week 1–2:** AI Sourcing (P0.1) + Resume Screening (P0.2)
2. **Week 3–4:** Interview Scheduling (P0.3) + Scorecards (P0.4)
3. **Week 5–6:** Async Video Interviews (P1.5) + Offer Management (P1.6)
4. **Week 7–8:** Talent Pool (P1.7) + Job Board Syndication (P1.8)
