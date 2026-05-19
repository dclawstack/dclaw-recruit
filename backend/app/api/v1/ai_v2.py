"""DClaw Recruit — AI v2 endpoints: next-gen features (2025-2026).

Adds:
- AI Screening Interviews (replaces manual phone screens)
- Skills-Based Hiring Engine (verified skills inference)
- Internal Mobility AI (hire from within)
- Candidate Experience Hub (chatbot, journey tracking)
"""

from uuid import UUID

from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.services.ai_screening_interview import (
    get_screening_questions,
    analyze_screening_response,
    generate_screening_result,
)
from app.services.skills_engine import (
    infer_skills_from_text,
    infer_skills_from_github,
    match_skills_to_role,
    SkillsProfile,
)
from app.services.internal_mobility import (
    find_internal_candidates,
    calculate_internal_hire_savings,
)
from app.services.candidate_experience import (
    generate_chatbot_response,
    generate_journey,
    classify_intent,
    PipelineStage,
)

router = APIRouter(prefix="/ai/v2", tags=["ai-v2"])


# ── Schemas ──────────────────────────────────────────────────────

class ScreeningInterviewRequest(BaseModel):
    candidate_id: str = Field(..., description="Candidate UUID")
    role_type: str = Field("general", description="engineering, product, general")
    responses: list[dict] = Field(..., description="[{question_id, text, duration_seconds}]")


class SkillsInferenceRequest(BaseModel):
    text: str = Field(..., description="Project description, bio, or combined text")


class GitHubInferenceRequest(BaseModel):
    repos: list[dict] = Field(..., description="[{name, description, language, topics[], stars}]")


class SkillsMatchRequest(BaseModel):
    text: str = Field(..., description="Candidate's project/bio text")
    required_skills: list[str]
    nice_to_have: list[str] = Field(default_factory=list)


class InternalMobilityRequest(BaseModel):
    job_title: str
    job_department: str
    required_skills: list[str]
    max_candidates: int = Field(5, ge=1, le=20)


class ChatbotRequest(BaseModel):
    candidate_name: str
    message: str
    current_stage: str = "applied"
    days_in_pipeline: int = 0


class JourneyRequest(BaseModel):
    candidate_id: str
    candidate_name: str
    current_stage: str
    stage_dates: dict[str, str] = Field(default_factory=dict, description="{stage: ISO datetime}")


# ── NEW P0: AI Screening Interview ────────────────────────────────

@router.get("/screening/questions", summary="Get AI screening questions for a role")
async def get_screening_questions_endpoint(
    role_type: str = Query("general", description="engineering, product, general"),
):
    """Get the question set for an AI-conducted screening interview."""
    questions = get_screening_questions(role_type)
    return {
        "role_type": role_type,
        "total_questions": len(questions),
        "questions": [
            {
                "id": q.id,
                "category": q.category,
                "question": q.question,
                "max_duration_seconds": q.max_duration_seconds,
            }
            for q in questions
        ],
    }


@router.post("/screening/analyze", summary="Analyze a single screening response")
async def analyze_screening_response_endpoint(payload: ScreeningInterviewRequest):
    """Analyze all responses from an AI screening interview."""
    result = generate_screening_result(
        candidate_id=UUID(payload.candidate_id),
        role_type=payload.role_type,
        responses=payload.responses,
    )
    return {
        "candidate_id": str(result.candidate_id),
        "overall_score": result.overall_score,
        "category_scores": result.category_scores,
        "communication_score": result.communication_score,
        "technical_accuracy": result.technical_accuracy,
        "culture_fit_score": result.culture_fit_score,
        "sentiment": result.sentiment,
        "red_flags": result.red_flags,
        "strengths": result.strengths,
        "transcript_summary": result.transcript_summary,
        "recommendation": result.recommendation,
    }


# ── NEW P0: Skills-Based Hiring Engine ────────────────────────────

@router.post("/skills/infer", summary="Infer skills from text")
async def infer_skills_endpoint(payload: SkillsInferenceRequest):
    """Infer skills and proficiency levels from project/bio text."""
    assessments = infer_skills_from_text(payload.text)
    return {
        "skills_found": len(assessments),
        "skills": [
            {
                "skill": a.skill_name,
                "proficiency": a.proficiency,
                "confidence": a.confidence,
                "evidence": a.evidence,
            }
            for a in assessments
        ],
    }


@router.post("/skills/infer-github", summary="Infer skills from GitHub repos")
async def infer_skills_github_endpoint(payload: GitHubInferenceRequest):
    """Infer skills from GitHub repository data."""
    assessments = infer_skills_from_github(payload.repos)
    return {
        "repos_analyzed": len(payload.repos),
        "skills_found": len(assessments),
        "skills": [
            {
                "skill": a.skill_name,
                "proficiency": a.proficiency,
                "confidence": a.confidence,
            }
            for a in assessments
        ],
    }


@router.post("/skills/match", summary="Match skills profile to role requirements")
async def match_skills_endpoint(payload: SkillsMatchRequest):
    """Match inferred skills against job requirements."""
    profile = SkillsProfile()
    profile.inferred_skills = infer_skills_from_text(payload.text)
    matched = match_skills_to_role(profile, payload.required_skills, payload.nice_to_have)
    return {
        "overall_readiness": matched.overall_readiness,
        "matched_skills": [
            {"skill": s.skill_name, "proficiency": s.proficiency}
            for s in profile.inferred_skills
            if s.skill_name.lower() in {ms.lower() for ms in payload.required_skills}
        ],
        "skill_gaps": matched.skill_gaps,
        "recommended_roles": matched.recommended_roles,
    }


# ── NEW P1: Internal Mobility ────────────────────────────────────

@router.post("/mobility/find", summary="Find internal candidates for a role")
async def find_internal_endpoint(payload: InternalMobilityRequest):
    """Find internal employees who could fill this role before external sourcing."""
    matches = find_internal_candidates(
        job_title=payload.job_title,
        job_department=payload.job_department,
        required_skills=payload.required_skills,
        max_candidates=payload.max_candidates,
    )
    savings = calculate_internal_hire_savings()
    return {
        "job_title": payload.job_title,
        "internal_candidates_found": len(matches),
        "candidates": [
            {
                "name": m.candidate.name,
                "current_role": m.candidate.current_role,
                "current_department": m.candidate.current_department,
                "match_score": m.match_score,
                "skill_overlap": m.skill_overlap,
                "skill_gaps": m.skill_gaps,
                "readiness": m.readiness,
                "is_lateral_move": m.recommended_lateral,
                "explanation": m.explanation,
            }
            for m in matches
        ],
        "savings_analysis": savings,
    }


@router.get("/mobility/savings", summary="Calculate internal hire savings")
async def get_savings_endpoint():
    """Calculate cost/time savings from internal vs external hiring."""
    return calculate_internal_hire_savings()


# ── NEW P1: Candidate Experience Hub ──────────────────────────────

@router.post("/experience/chatbot", summary="Candidate chatbot response")
async def chatbot_endpoint(payload: ChatbotRequest):
    """Generate a chatbot response for candidate inquiries."""
    stage = PipelineStage(payload.current_stage) if payload.current_stage in [s.value for s in PipelineStage] else PipelineStage.APPLIED
    response = generate_chatbot_response(
        message=payload.message,
        candidate_name=payload.candidate_name,
        current_stage=stage,
        days_in_pipeline=payload.days_in_pipeline,
    )
    intent = classify_intent(payload.message)
    return {
        "intent": intent,
        "message": response.message,
        "action_links": response.action_links,
        "sentiment": response.sentiment,
    }


@router.post("/experience/journey", summary="Generate candidate journey")
async def journey_endpoint(payload: JourneyRequest):
    """Generate a candidate journey with transparency score."""
    from datetime import datetime
    
    stage_dates = {}
    for stage_str, date_str in payload.stage_dates.items():
        try:
            stage = PipelineStage(stage_str)
            stage_dates[stage] = datetime.fromisoformat(date_str).replace(tzinfo=None)
        except (ValueError, KeyError):
            continue
    
    journey = generate_journey(
        candidate_id=UUID(payload.candidate_id),
        candidate_name=payload.candidate_name,
        current_stage=PipelineStage(payload.current_stage),
        stage_dates=stage_dates,
    )
    return {
        "candidate_name": journey.candidate_name,
        "current_stage": journey.current_stage.value,
        "days_in_pipeline": journey.total_days_in_pipeline,
        "transparency_score": journey.transparency_score,
        "timeline": [
            {
                "stage": u.stage.value,
                "timestamp": u.timestamp.isoformat(),
                "message": u.message,
                "next_steps": u.next_steps,
            }
            for u in journey.updates
        ],
    }
