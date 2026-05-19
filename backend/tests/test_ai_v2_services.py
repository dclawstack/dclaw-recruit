"""Tests for v2 AI services — screening interviews, skills engine, mobility, experience."""

import pytest
from uuid import uuid4

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
    classify_intent,
    generate_chatbot_response,
    generate_journey,
    PipelineStage,
)


# ── AI Screening Interviews ───────────────────────────────────────

def test_get_questions_engineering():
    questions = get_screening_questions("engineering")
    assert len(questions) == 4
    assert questions[0].category == "technical"


def test_get_questions_general_fallback():
    questions = get_screening_questions("nonexistent")
    assert len(questions) == 4


def test_analyze_good_response():
    q = get_screening_questions("general")[0]
    result = analyze_screening_response(
        q,
        "I led a challenging migration from monolith to microservices. "
        "My specific contribution was architecting the new service boundaries "
        "and implementing the API gateway. We achieved 99.9% uptime and reduced "
        "deployment time by 80%. It was a great learning experience.",
        60.0,
    )
    assert result["communication_score"] > 50
    assert len(result["strengths"]) > 0
    assert len(result["red_flags"]) == 0


def test_analyze_poor_response():
    q = get_screening_questions("general")[0]
    result = analyze_screening_response(q, "I don't know. Whatever.", 10.0)
    assert result["communication_score"] <= 60
    assert len(result["red_flags"]) > 0


def test_generate_screening_result_advance():
    questions = get_screening_questions("general")
    responses = [
        {
            "question_id": q.id,
            "text": "I built and led a major project that delivered great results. I collaborated with the team and we achieved our goals. The impact was significant.",
            "duration_seconds": 45,
        }
        for q in questions
    ]
    result = generate_screening_result(uuid4(), "general", responses)
    assert result.overall_score > 0
    assert result.recommendation in ("advance", "hold", "reject")
    assert len(result.transcript_summary) > 0


# ── Skills-Based Hiring Engine ────────────────────────────────────

SAMPLE_PROJECT_TEXT = """
Built a real-time data pipeline using Python, FastAPI, and PostgreSQL.
Deployed on AWS using Lambda, S3, and DynamoDB. Containerized with Docker
and orchestrated with Kubernetes. Implemented CI/CD with GitHub Actions.
Used async/await patterns and type hints throughout. Built custom React
dashboard with hooks and Redux for the frontend.
"""


def test_infer_skills_from_text():
    skills = infer_skills_from_text(SAMPLE_PROJECT_TEXT)
    assert len(skills) > 0
    skill_names = [s.skill_name for s in skills]
    assert "python" in skill_names
    assert "aws" in skill_names


def test_infer_skills_proficiency_levels():
    skills = infer_skills_from_text(SAMPLE_PROJECT_TEXT)
    proficiencies = {s.skill_name: s.proficiency for s in skills}
    # Python with async/type hints should be advanced+
    assert proficiencies.get("python") in ("advanced", "expert")


def test_infer_skills_empty_text():
    skills = infer_skills_from_text("")
    assert len(skills) == 0


def test_infer_skills_from_github():
    repos = [
        {
            "name": "ml-pipeline",
            "description": "Production ML pipeline with FastAPI and Docker",
            "language": "Python",
            "topics": ["machine-learning", "fastapi", "docker"],
            "stars": 42,
        }
    ]
    skills = infer_skills_from_github(repos)
    assert any(s.skill_name == "python" for s in skills)
    assert any(s.skill_name == "machine_learning" for s in skills)


def test_match_skills_to_role_ready():
    profile = SkillsProfile()
    profile.inferred_skills = infer_skills_from_text(SAMPLE_PROJECT_TEXT)
    matched = match_skills_to_role(profile, ["python", "aws", "kubernetes"])
    assert matched.overall_readiness > 30  # 3 skills, 1 expert + 2 beginner
    assert "python" not in matched.skill_gaps


def test_match_skills_to_role_gaps():
    profile = SkillsProfile()
    profile.inferred_skills = infer_skills_from_text(SAMPLE_PROJECT_TEXT)
    matched = match_skills_to_role(profile, ["ruby", "azure", "swift"])
    assert len(matched.skill_gaps) > 0
    assert matched.overall_readiness < 50


# ── Internal Mobility ─────────────────────────────────────────────

def test_find_internal_candidates():
    matches = find_internal_candidates(
        job_title="Senior Backend Engineer",
        job_department="Engineering",
        required_skills=["python", "postgresql", "aws", "kubernetes"],
        max_candidates=5,
    )
    assert len(matches) > 0
    assert matches[0].match_score > 0
    assert len(matches[0].explanation) > 0


def test_find_internal_candidates_no_match():
    matches = find_internal_candidates(
        job_title="Rust Engineer",
        job_department="Engineering",
        required_skills=["rust", "wasm", "zig"],
        max_candidates=5,
    )
    assert len(matches) == 0


def test_internal_hire_savings():
    savings = calculate_internal_hire_savings()
    assert savings["cost_savings"] > 0
    assert savings["time_savings_days"] > 0


# ── Candidate Experience ─────────────────────────────────────────

def test_classify_intent_status():
    assert classify_intent("what's my status?") == "status"
    assert classify_intent("any updates?") == "status"


def test_classify_intent_schedule():
    assert classify_intent("when is my interview?") == "schedule"
    assert classify_intent("can I reschedule?") == "schedule"


def test_classify_intent_feedback():
    assert classify_intent("how did I do?") == "feedback"


def test_classify_intent_unknown():
    assert classify_intent("random message") == "general"


def test_generate_chatbot_response():
    resp = generate_chatbot_response(
        message="what's my status?",
        candidate_name="Alice",
        current_stage=PipelineStage.AI_SCREENING,
        days_in_pipeline=5,
    )
    assert "Alice" in resp.message
    assert "ai screening" in resp.message.lower()
    assert len(resp.action_links) > 0


def test_generate_journey():
    from datetime import datetime, timezone

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    journey = generate_journey(
        candidate_id=uuid4(),
        candidate_name="Bob",
        current_stage=PipelineStage.TECHNICAL,
        stage_dates={
            PipelineStage.APPLIED: now,
            PipelineStage.TECHNICAL: now,
        },
    )
    assert journey.candidate_name == "Bob"
    assert journey.current_stage == PipelineStage.TECHNICAL
    assert journey.transparency_score >= 0
    assert len(journey.updates) > 0
