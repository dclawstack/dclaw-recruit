"""AI Sourcing Agent — finds candidates and generates outreach messages.

Uses keyword matching + heuristic scoring for baseline.
Ready for LLM/embedding integration when API keys are configured.
"""

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class SourcedCandidate:
    name: str
    title: str
    company: str
    location: str | None = None
    source: str = "linkedin"
    profile_url: str = ""
    match_score: float = 0.0
    skills: list[str] = field(default_factory=list)
    outreach_message: str = ""


# Simulated candidate database for demo purposes
# In production, this would query LinkedIn API, GitHub API, etc.
_SIMULATED_CANDIDATES = [
    {
        "name": "Alice Johnson",
        "title": "Senior Software Engineer",
        "company": "TechScale Inc.",
        "location": "San Francisco, CA",
        "skills": ["python", "react", "aws", "kubernetes", "postgresql"],
    },
    {
        "name": "Bob Martinez",
        "title": "Full Stack Developer",
        "company": "DataFlow Systems",
        "location": "Austin, TX",
        "skills": ["typescript", "next.js", "node.js", "docker", "mongodb"],
    },
    {
        "name": "Carol Chen",
        "title": "ML Engineer",
        "company": "AI Dynamics",
        "location": "Seattle, WA",
        "skills": ["python", "tensorflow", "pytorch", "aws", "docker"],
    },
    {
        "name": "David Kim",
        "title": "DevOps Engineer",
        "company": "CloudBase Solutions",
        "location": "New York, NY",
        "skills": ["kubernetes", "terraform", "aws", "ci/cd", "python"],
    },
    {
        "name": "Elena Rodriguez",
        "title": "Product Manager",
        "company": "BuildWith Inc.",
        "location": "Remote",
        "skills": ["product management", "agile", "data analysis", "sql", "leadership"],
    },
    {
        "name": "Frank Williams",
        "title": "Backend Engineer",
        "company": "FinScale",
        "location": "Chicago, IL",
        "skills": ["java", "spring", "postgresql", "redis", "docker"],
    },
    {
        "name": "Grace Liu",
        "title": "Frontend Developer",
        "company": "UX Labs",
        "location": "Los Angeles, CA",
        "skills": ["react", "typescript", "tailwindcss", "next.js", "figma"],
    },
    {
        "name": "Henry Patel",
        "title": "Data Scientist",
        "company": "InsightIQ",
        "location": "Boston, MA",
        "skills": ["python", "pandas", "scikit-learn", "sql", "tableau"],
    },
]


def source_candidates(
    job_title: str,
    job_description: str,
    required_skills: list[str] | None = None,
    sources: list[str] | None = None,
    limit: int = 10,
) -> list[SourcedCandidate]:
    """Source candidates based on job requirements.

    Args:
        job_title: The job title to search for
        job_description: Full job description text
        required_skills: Specific skills to match against
        sources: Which platforms to search (linkedin, github, etc.)
        limit: Max candidates to return

    Returns:
        List of SourcedCandidate with match scores and outreach messages
    """
    if not required_skills:
        # Extract skills from job description
        jd_lower = job_description.lower()
        from app.services.resume_parser import ALL_SKILLS
        required_skills = [s for s in ALL_SKILLS if s in jd_lower]

    required_lower = set(s.lower() for s in (required_skills or []))
    results = []

    for candidate in _SIMULATED_CANDIDATES:
        candidate_skills_lower = set(s.lower() for s in candidate["skills"])
        matched = required_lower & candidate_skills_lower

        if required_lower and not matched:
            continue

        score = (len(matched) / len(required_lower) * 100) if required_lower else 50

        outreach = _generate_outreach(
            candidate["name"],
            candidate["title"],
            candidate["company"],
            job_title,
            list(matched),
        )

        results.append(
            SourcedCandidate(
                name=candidate["name"],
                title=candidate["title"],
                company=candidate["company"],
                location=candidate.get("location"),
                source="linkedin",
                profile_url=f"https://linkedin.com/in/{candidate['name'].lower().replace(' ', '-')}",
                match_score=round(score, 1),
                skills=candidate["skills"],
                outreach_message=outreach,
            )
        )

    results.sort(key=lambda c: c.match_score, reverse=True)
    return results[:limit]


def _generate_outreach(
    candidate_name: str,
    candidate_title: str,
    candidate_company: str,
    job_title: str,
    matched_skills: list[str],
) -> str:
    """Generate a personalized outreach message."""
    skill_mention = (
        f"I noticed your experience with {', '.join(matched_skills[:3])}. "
        if matched_skills
        else ""
    )

    return (
        f"Hi {candidate_name.split()[0]},\n\n"
        f"{skill_mention}"
        f"We're hiring a {job_title} at DClaw and I think your background "
        f"as {candidate_title} at {candidate_company} would be a great fit. "
        f"Would you be open to a quick chat about the opportunity?\n\n"
        f"Best,\nDClaw Recruit Team"
    )
