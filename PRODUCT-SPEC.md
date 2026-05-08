# PRODUCT-SPEC: Recruit

## Overview

**App Name:** Recruit
**Domain:** ATS / Hiring Pipeline
**Target User:** HR teams, hiring managers

## Core Entities

### JobRequisition
```
JobRequisition
├── id: UUID (PK)
├── title: str (required)
├── department: str (optional)
├── location: str (optional)
├── salary_range: str (optional)
├── description: str (optional)
├── status: enum ["open", "paused", "closed"] (default: "open")
├── created_at: datetime
└── updated_at: datetime
```

### Candidate
```
Candidate
├── id: UUID (PK)
├── name: str (required)
├── email: str (unique, required)
├── phone: str (optional)
├── resume_url: str (optional)
├── source: str (optional) — e.g. "linkedin", "referral", "direct"
├── stage: enum ["applied", "screening", "interview", "offer", "hired", "rejected"] (default: "applied")
├── job_id: UUID (FK → JobRequisition, ondelete=SET NULL, optional)
├── created_at: datetime
└── updated_at: datetime
```

### Interview
```
Interview
├── id: UUID (PK)
├── candidate_id: UUID (FK → Candidate, ondelete=CASCADE)
├── job_id: UUID (FK → JobRequisition, ondelete=SET NULL, optional)
├── scheduled_at: datetime (optional)
├── interviewer: str (optional)
├── feedback: str (optional)
├── rating: int (1-5, optional)
├── created_at: datetime
└── updated_at: datetime
```

## User Stories / Screens

### Screen 1: Dashboard
- Summary cards: open jobs, total candidates, interviews this week, time-to-hire avg
- Recent candidates feed
- Jobs by status chart
- Quick actions (post job, add candidate, schedule interview)

### Screen 2: Jobs
- Table view with pagination, search by title/department
- Status filter (open/paused/closed)
- "Add Job" modal/form

### Screen 3: Job Detail
- Job info card with edit/delete
- Related candidates list with stage filters
- Add candidate button

### Screen 4: Candidates
- Table view with pagination, search by name/email
- Stage filter (applied/screening/interview/offer/hired/rejected)
- Source breakdown
- "Add Candidate" form with job dropdown

### Screen 5: Candidate Detail
- Candidate info with edit/delete
- Stage progression buttons
- Related interviews list
- Schedule interview button
- Resume link

### Screen 6: Interviews
- Calendar/list view
- "Add Interview" form with candidate/job dropdowns
- Feedback form

## API Endpoints

- `GET /api/v1/jobs` — list jobs
- `POST /api/v1/jobs` — create job
- `GET /api/v1/jobs/{id}` — get job
- `PATCH /api/v1/jobs/{id}` — update job
- `DELETE /api/v1/jobs/{id}` — delete job

- `GET /api/v1/candidates` — list candidates
- `POST /api/v1/candidates` — create candidate
- `GET /api/v1/candidates/{id}` — get candidate
- `PATCH /api/v1/candidates/{id}` — update candidate
- `DELETE /api/v1/candidates/{id}` — delete candidate

- `GET /api/v1/interviews` — list interviews
- `POST /api/v1/interviews` — create interview
- `GET /api/v1/interviews/{id}` — get interview
- `PATCH /api/v1/interviews/{id}` — update interview
- `DELETE /api/v1/interviews/{id}` — delete interview
