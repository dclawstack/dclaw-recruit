# DClaw Recruit — Feature Evolution (v1.2 → v2.0)

> **Date:** 2026-05-19
> **Rationale:** Industry shift toward AI-first, skills-based, internal-mobility-driven recruiting. Traditional ATS features are now table stakes — differentiation comes from AI-native capabilities.

---

## 🔴 REMOVED / DEPRECATED Features

| # | Feature | Reason for Removal | Replacement |
|---|---------|-------------------|-------------|
| P1.8 | **Job Board Syndication** | Manual syndication to LinkedIn/Indeed is outdated. Replaced by programmatic ad buying with AI-optimized spend across platforms. | Programmatic Job Ads (P1 New) |
| v1.0 | **Basic Resume Keyword Parsing** | Keyword matching produces high false positives and misses skills inferred from actual work. Industry moving to verified skills assessment. | Skills-Based Hiring Engine (P0 New) |
| P0.4 | **Manual Interview Scorecards** | Static scorecards with human rubrics being replaced by AI-generated interview intelligence that analyzes transcripts for signals. | AI Screening Interviews (P0 New) |
| P0.1 | **Traditional Sourcing (keyword-based)** | Simple keyword matching on LinkedIn/GitHub yields low-quality matches. Modern platforms use skill inference and project-based matching. | Skills-Based Hiring Engine (P0 New) |
| P1.6 | **Basic Offer Management** | Standalone offer letters without market intelligence are insufficient. Industry now demands total compensation benchmarking. | Labor Market Intelligence (P2 New) |

---

## 🟢 NEW Features (2025-2026 Industry Standards)

### P0 — Must Have (Ship Now)

| # | Feature | Industry Driver | What It Does |
|---|---------|----------------|--------------|
| **N1** | **AI Screening Interviews** | Mercor, Paradox — AI conducts first-round screening via voice/video, assessing communication, soft skills, and culture fit. 80% reduction in phone screen time. | AI analyzes candidate responses, detects red flags, scores communication, and recommends advance/hold/reject. |
| **N2** | **Skills-Based Hiring Engine** | LinkedIn Skills-First Movement — infer verified skills from GitHub repos, portfolios, and project descriptions instead of relying on self-reported keywords. | Analyzes code repos and project text to infer proficiency (Beginner→Expert) with confidence scores. Matches skills to role requirements. |

### P1 — Should Have (Next Quarter)

| # | Feature | Industry Driver | What It Does |
|---|---------|----------------|--------------|
| **N3** | **Internal Mobility AI** | "Hire from Within" — companies save $20K+ per internal hire. AI matches existing employees to open roles before external posting. | Scans workforce for skill overlap, predicts readiness (now/3mo/6mo/12mo), calculates ROI of internal vs external hire. |
| **N4** | **Candidate Experience Hub** | Candidate ghosting is the #1 complaint. Modern platforms provide real-time transparency, AI chatbots, and structured feedback at every stage. | AI chatbot for 24/7 candidate questions, transparency score, pipeline timeline, instant self-scheduling. |

### P2 — Future

| # | Feature | Industry Driver | What It Does |
|---|---------|----------------|--------------|
| **N5** | **Programmatic Job Advertising** | AI-optimized ad spend across LinkedIn/Indeed/Google — replaces manual syndication. Dynamic bidding and budget allocation. | Auto-distributes job posts with AI budget optimization across platforms. |
| **N6** | **Labor Market Intelligence** | Real-time salary benchmarking, talent availability heatmaps, competitor hiring analysis. | Live market data for compensation decisions and hiring strategy. |
| **N7** | **DEI Intelligence Dashboard** | Regulatory pressure + ESG requirements. Real-time diversity metrics, bias interception alerts, slate diversity tracking. | Monitors pipeline diversity, flags bias patterns, ensures compliant hiring. |

---

## 📊 Migration Map: Old → New

```
v1.2 Feature              →  v2.0 Replacement
─────────────────────────────────────────────────
Job Board Syndication     →  Programmatic Job Ads (N5)
Resume Keyword Parsing    →  Skills-Based Hiring Engine (N2)
Manual Scorecards         →  AI Screening Interviews (N1)
Traditional Sourcing      →  Skills-Based Hiring Engine (N2)
Basic Offer Management    →  Labor Market Intelligence (N6)
Basic Interview Schedule  →  AI Screening Interviews (N1) + Candidate Experience Hub (N4)
ATS Pipeline              →  Retained as foundation, enhanced with transparency
AI Recruit Copilot        →  Retained, enhanced with skills-based matching
Recruitment Analytics     →  Retained, enhanced with DEI Intelligence (N7)
```

---

## 🏗️ Implementation Status

| Feature | Backend Service | API Endpoint | Tests |
|---------|----------------|--------------|-------|
| AI Screening Interviews | `ai_screening_interview.py` | `POST /api/v1/ai/v2/screening/analyze` | ✅ |
| Skills-Based Hiring | `skills_engine.py` | `POST /api/v1/ai/v2/skills/infer` | ✅ |
| Internal Mobility | `internal_mobility.py` | `POST /api/v1/ai/v2/mobility/find` | ✅ |
| Candidate Experience | `candidate_experience.py` | `POST /api/v1/ai/v2/experience/chatbot` | ✅ |
| Programmatic Ads | TBD | TBD | ⬜ |
| Labor Market Intel | TBD | TBD | ⬜ |
| DEI Intelligence | TBD | TBD | ⬜ |

---

## 📝 Landing Page Updates

- Tagline updated: "Next-Gen AI Recruiting — Skills-Based, Internal-First, Candidate-Centric"
- Hero stats updated: 60% faster, 4.8★ candidate experience, 35% internal-first
- Features grid replaced with 6 new cards highlighting N1-N4 + retained core features
- Badges clearly mark "New P0" and "New P1" features

---

*This document serves as the authoritative record of feature evolution from PLAN-v1.2 to the current state.*
