"""DClaw Recruit — AI endpoints: sourcing, screening, scheduling, scorecards."""

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.services.sourcing_ai import source_candidates
from app.services.screening import screen_resumes, anonymize_resume
from app.services.scheduling import generate_available_slots, find_best_slots, generate_reminder_message
from app.services.scorecards import get_scorecard_template, calculate_scorecard

router = APIRouter(prefix="/ai", tags=["ai"])


# ── Schemas ──────────────────────────────────────────────────────

class SourceRequest(BaseModel):
    job_title: str = Field(..., description="Job title to search for")
    job_description: str = Field("", description="Full job description")
    required_skills: list[str] | None = Field(None, description="Specific skills required")
    sources: list[str] | None = Field(None, description="Platforms: linkedin, github")
    limit: int = Field(10, ge=1, le=50)


class ScreenRequest(BaseModel):
    job_description: str = Field(..., description="Job description to match against")
    required_skills: list[str] | None = None
    resumes: list[dict] = Field(..., description="List of {id, text} resume objects")


class ScheduleRequest(BaseModel):
    candidate_availability: list[dict] = Field(
        default_factory=list, description="List of {start, end} ISO datetime strings"
    )
    interviewer_availability: list[dict] = Field(
        default_factory=list, description="List of {start, end} ISO datetime strings"
    )
    num_slots: int = Field(3, ge=1, le=10)
    timezone_offset_hours: int | None = None


class ScorecardRequest(BaseModel):
    role_type: str = Field("general", description="engineering, product, or general")
    category_scores: dict[str, float] = Field(..., description="Category name -> score (1-5)")


class ReminderRequest(BaseModel):
    candidate_name: str
    interviewer_name: str
    scheduled_time: str = Field(..., description="ISO datetime string")
    days_before: int = 1


class AnonymizeRequest(BaseModel):
    text: str = Field(..., description="Resume text to anonymize")


# ── P0.1: AI Recruiting Copilot (Sourcing) ────────────────────────

@router.post("/source", summary="Source candidates with AI matching")
async def ai_source(payload: SourceRequest):
    """Find candidates across platforms based on job requirements.
    Returns ranked candidates with match scores and outreach messages.
    """
    results = source_candidates(
        job_title=payload.job_title,
        job_description=payload.job_description,
        required_skills=payload.required_skills,
        sources=payload.sources,
        limit=payload.limit,
    )
    return {
        "job_title": payload.job_title,
        "candidates_found": len(results),
        "candidates": [
            {
                "name": c.name,
                "title": c.title,
                "company": c.company,
                "location": c.location,
                "source": c.source,
                "profile_url": c.profile_url,
                "match_score": c.match_score,
                "skills": c.skills,
                "outreach_message": c.outreach_message,
            }
            for c in results
        ],
    }


# ── P0.2: AI Resume Screening & Ranking ───────────────────────────

@router.post("/screen", summary="Screen and rank resumes against a job description")
async def ai_screen(payload: ScreenRequest):
    """Parse resumes and rank candidates by match score.
    Includes skill matching, experience weighting, and bias detection.
    """
    results = await screen_resumes(
        resumes=payload.resumes,
        job_description=payload.job_description,
        required_skills=payload.required_skills,
    )
    return {
        "job_description_preview": payload.job_description[:200],
        "resumes_screened": len(results),
        "ranked_candidates": results,
    }


@router.post("/anonymize", summary="Anonymize a resume for bias-free screening")
async def ai_anonymize(payload: AnonymizeRequest):
    """Remove PII (name, email, phone) from resume text."""
    anon_text = await anonymize_resume(payload.text)
    return {"anonymized_text": anon_text}


# ── P0.3: Interview Scheduling ────────────────────────────────────

@router.get("/slots", summary="Get available interview time slots")
async def get_slots(
    days_ahead: int = Query(14, ge=1, le=30),
    business_hours_only: bool = Query(True),
    slot_duration_minutes: int = Query(60, ge=15, le=120),
):
    """Generate available time slots for the next N days."""
    slots = generate_available_slots(
        days_ahead=days_ahead,
        business_hours_only=business_hours_only,
        slot_duration_minutes=slot_duration_minutes,
    )
    return {
        "days_ahead": days_ahead,
        "total_slots": len(slots),
        "slots": [{"start": s.start.isoformat(), "end": s.end.isoformat()} for s in slots],
    }


@router.post("/schedule", summary="Find best interview slots")
async def ai_schedule(payload: ScheduleRequest):
    """Find overlapping availability between candidate and interviewer."""
    result = find_best_slots(
        candidate_availability=payload.candidate_availability,
        interviewer_availability=payload.interviewer_availability,
        num_slots=payload.num_slots,
        timezone_offset_hours=payload.timezone_offset_hours,
    )
    return {
        "proposed_slots": [s.isoformat() for s in result.proposed_slots],
        "conflicts": result.conflicts,
        "timezone_note": result.timezone_note,
    }


@router.post("/reminder", summary="Generate interview reminder message")
async def ai_reminder(payload: ReminderRequest):
    """Generate a reminder message for scheduled interviews."""
    from datetime import datetime

    scheduled = datetime.fromisoformat(payload.scheduled_time).replace(tzinfo=None)
    message = generate_reminder_message(
        candidate_name=payload.candidate_name,
        interviewer_name=payload.interviewer_name,
        scheduled_time=scheduled,
        days_before=payload.days_before,
    )
    return {"message": message}


# ── P0.4: Interview Scorecards ────────────────────────────────────

@router.get("/scorecards/template", summary="Get scorecard template for a role")
async def get_template(
    role_type: str = Query("general", description="engineering, product, or general"),
):
    """Get a structured interview scorecard template."""
    template = get_scorecard_template(role_type)
    return {
        "role_type": role_type,
        "categories": [
            {
                "name": r.category,
                "weight": r.weight,
                "criteria": r.criteria,
            }
            for r in template
        ],
    }


@router.post("/scorecards/calculate", summary="Calculate scorecard result")
async def calculate_result(payload: ScorecardRequest):
    """Calculate weighted score from category ratings."""
    template = get_scorecard_template(payload.role_type)
    result = calculate_scorecard(
        category_scores=payload.category_scores,
        template=template,
    )
    return {
        "role_type": payload.role_type,
        "total_score": result.total_score,
        "category_scores": result.category_scores,
        "strengths": result.strengths,
        "weaknesses": result.weaknesses,
        "recommendation": result.overall_recommendation,
    }
