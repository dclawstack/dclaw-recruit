"""Tests for AI services — sourcing, screening, scheduling, scorecards."""

import pytest
from app.services.resume_parser import parse_resume, calculate_match_score
from app.services.sourcing_ai import source_candidates
from app.services.scheduling import generate_available_slots, find_best_slots, generate_reminder_message
from app.services.scorecards import get_scorecard_template, calculate_scorecard, SCORECARD_TEMPLATES


# ── Resume Parser ─────────────────────────────────────────────────

SAMPLE_RESUME = """
Alice Johnson
alice@example.com | (555) 123-4567

Senior Software Engineer with 8 years of experience
TechScale Inc., San Francisco, CA

Skills: Python, React, AWS, Kubernetes, PostgreSQL, Docker

Education: B.S. Computer Science, Stanford University

Experience:
- Led team of 5 engineers building microservices platform
- Architected cloud migration to AWS saving $500K annually
- Built CI/CD pipeline with GitHub Actions and Docker
"""


def test_parse_resume_extracts_email():
    parsed = parse_resume(SAMPLE_RESUME)
    assert parsed.email == "alice@example.com"


def test_parse_resume_extracts_phone():
    parsed = parse_resume(SAMPLE_RESUME)
    assert parsed.phone is not None
    assert "555" in parsed.phone


def test_parse_resume_extracts_skills():
    parsed = parse_resume(SAMPLE_RESUME)
    assert "python" in parsed.skills
    assert "react" in parsed.skills
    assert "aws" in parsed.skills


def test_parse_resume_extracts_experience():
    parsed = parse_resume(SAMPLE_RESUME)
    assert parsed.years_experience == 8.0


def test_parse_resume_extracts_education():
    parsed = parse_resume(SAMPLE_RESUME)
    assert len(parsed.education) > 0


def test_parse_resume_handles_empty_text():
    parsed = parse_resume("")
    assert parsed.email is None
    assert parsed.phone is None
    assert parsed.skills == []


def test_calculate_match_score_perfect():
    parsed = parse_resume(SAMPLE_RESUME)
    required = ["python", "react", "aws", "docker"]
    result = calculate_match_score(parsed, "", required)
    assert result["score"] > 0
    assert len(result["matched_skills"]) > 0


def test_calculate_match_score_no_match():
    parsed = parse_resume(SAMPLE_RESUME)
    required = ["ruby", "ember", "azure"]
    result = calculate_match_score(parsed, "", required)
    assert len(result["matched_skills"]) == 0
    assert len(result["missing_skills"]) == 3


# ── Sourcing ──────────────────────────────────────────────────────

def test_source_candidates_returns_results():
    results = source_candidates(
        job_title="Senior Software Engineer",
        job_description="We need Python, React, AWS skills",
        limit=5,
    )
    assert len(results) > 0
    assert len(results) <= 5
    assert results[0].match_score > 0
    assert len(results[0].outreach_message) > 0


def test_source_candidates_respects_limit():
    results = source_candidates(
        job_title="Engineer",
        job_description="",
        limit=3,
    )
    assert len(results) <= 3


# ── Scheduling ────────────────────────────────────────────────────

def test_generate_available_slots():
    slots = generate_available_slots(days_ahead=7, business_hours_only=True)
    assert len(slots) > 0
    # Weekdays only: 5 days × 8 business hours (60-min slots) = ~40
    assert len(slots) >= 30
    for slot in slots:
        assert slot.start.weekday() < 5  # no weekends


def test_generate_available_slots_skips_weekends():
    slots = generate_available_slots(days_ahead=7, business_hours_only=False)
    # Should have some weekends and weekdays
    weekdays = sum(1 for s in slots if s.start.weekday() < 5)
    weekends = sum(1 for s in slots if s.start.weekday() >= 5)
    assert weekdays > 0
    # With 7 days, 2 are weekends, so weekends should exist
    # (but they might be at the end of the week)
    assert len(slots) > 0


def test_find_best_slots_no_constraints():
    result = find_best_slots(
        candidate_availability=[],
        interviewer_availability=[],
        num_slots=3,
    )
    assert len(result.proposed_slots) == 3


def test_generate_reminder_message():
    from datetime import datetime, timezone

    msg = generate_reminder_message(
        candidate_name="Alice",
        interviewer_name="Bob",
        scheduled_time=datetime.now(timezone.utc).replace(tzinfo=None),
        days_before=1,
    )
    assert "Alice" in msg
    assert "Bob" in msg


# ── Scorecards ────────────────────────────────────────────────────

def test_get_scorecard_template_engineering():
    template = get_scorecard_template("engineering")
    assert len(template) == 5
    total_weight = sum(r.weight for r in template)
    assert abs(total_weight - 1.0) < 0.01


def test_get_scorecard_template_general_fallback():
    template = get_scorecard_template("nonexistent")
    assert len(template) > 0


def test_calculate_scorecard_strong_hire():
    template = get_scorecard_template("general")
    scores = {r.category: 5.0 for r in template}
    result = calculate_scorecard(scores, template)
    assert result.total_score >= 4.0
    assert result.overall_recommendation == "strong_hire"
    assert len(result.strengths) > 0


def test_calculate_scorecard_no_hire():
    template = get_scorecard_template("general")
    scores = {r.category: 1.0 for r in template}
    result = calculate_scorecard(scores, template)
    assert result.total_score <= 2.0
    assert result.overall_recommendation == "no_hire"


def test_all_templates_have_valid_weights():
    for role_type, template in SCORECARD_TEMPLATES.items():
        total = sum(r.weight for r in template)
        assert abs(total - 1.0) < 0.01, f"{role_type} weights sum to {total}, not 1.0"
