"""Resume parsing service — extracts structured data from resume text/files.

Uses regex + keyword extraction for basic parsing.
Ready for LLM-based enhancement when API keys are configured.
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ParsedResume:
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str] = field(default_factory=list)
    years_experience: Optional[float] = None
    education: list[str] = field(default_factory=list)
    companies: list[str] = field(default_factory=list)
    job_titles: list[str] = field(default_factory=list)
    raw_text: str = ""


# Common skill keywords for tech roles
TECH_SKILLS = {
    "python", "javascript", "typescript", "java", "go", "rust", "c++", "c#",
    "react", "angular", "vue", "next.js", "node.js", "django", "flask", "fastapi",
    "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "git", "agile", "scrum", "jira", "confluence",
}

# Common skill keywords for non-tech roles
BUSINESS_SKILLS = {
    "project management", "product management", "marketing", "sales",
    "business development", "customer success", "account management",
    "recruiting", "talent acquisition", "hr", "human resources",
    "finance", "accounting", "operations", "strategy", "consulting",
    "leadership", "communication", "presentation", "negotiation",
    "data analysis", "excel", "tableau", "power bi", "looker",
}

ALL_SKILLS = TECH_SKILLS | BUSINESS_SKILLS


def parse_resume(text: str) -> ParsedResume:
    """Parse a resume text and extract structured information.

    Args:
        text: Raw text content of the resume

    Returns:
        ParsedResume with extracted fields
    """
    result = ParsedResume(raw_text=text)

    # Extract email
    email_match = re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    if email_match:
        result.email = email_match.group(0)

    # Extract phone
    phone_match = re.search(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        text,
    )
    if phone_match:
        result.phone = phone_match.group(0)

    # Extract name — heuristic: first line or near email
    lines = text.strip().split("\n")
    for line in lines[:5]:
        line = line.strip()
        if line and not re.search(r"[@:]", line) and len(line.split()) <= 4:
            # Skip lines that are likely titles/headers
            if not any(
                kw in line.lower()
                for kw in ["resume", "cv", "curriculum", "summary", "objective", "experience", "education", "skill"]
            ):
                result.name = line
                break

    # Extract skills
    text_lower = text.lower()
    for skill in ALL_SKILLS:
        if skill in text_lower:
            result.skills.append(skill)

    # Estimate years of experience
    exp_years = re.findall(r"(\d+)[\+]?\s*(?:years|yrs)(?:\s+of)?\s+experience", text_lower)
    if exp_years:
        result.years_experience = float(exp_years[0])

    # Extract education keywords
    education_keywords = [
        "bachelor", "master", "phd", "ph.d", "mba", "b.tech", "m.tech",
        "b.s.", "m.s.", "b.a.", "m.a.", "associate", "diploma",
    ]
    for edu in education_keywords:
        if edu in text_lower:
            result.education.append(edu)

    # Extract company names (heuristic: lines after "experience" with known suffixes)
    company_suffixes = r"(?:Inc\.|LLC|Ltd|Limited|Corp|Corporation|GmbH|S\.A\.|B\.V\.)"
    company_matches = re.findall(
        rf"([A-Z][A-Za-z0-9\s&]+(?:{company_suffixes}))", text
    )
    result.companies = list(set(c.strip() for c in company_matches))[:10]

    # Extract job titles (heuristic: capitalized short phrases)
    title_patterns = [
        r"(?:Senior|Lead|Principal|Staff|Jr\.?|Junior)?\s*(?:Software\s+)?(?:Engineer|Developer|Manager|Director|VP|Analyst|Designer|Architect|Consultant|Scientist|Recruiter|Coordinator|Specialist)",
    ]
    for pattern in title_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        result.job_titles.extend(m.strip() for m in matches)

    return result


def calculate_match_score(
    resume: ParsedResume, job_description: str, required_skills: list[str] | None = None
) -> dict:
    """Calculate match score between a parsed resume and job description.

    Args:
        resume: Parsed resume data
        job_description: Job description text
        required_skills: Optional list of required skills

    Returns:
        dict with score (0-100), matched_skills, missing_skills, and explanation
    """
    required = set(s.lower() for s in (required_skills or []))

    # Extract skills from job description if not provided
    if not required:
        jd_lower = job_description.lower()
        required = {s for s in ALL_SKILLS if s in jd_lower}

    matched = [s for s in required if s in (sk.lower() for sk in resume.skills)]
    missing = list(required - set(matched))

    if not required:
        return {
            "score": 50,
            "matched_skills": [],
            "missing_skills": [],
            "explanation": "No specific skills extracted from job description.",
        }

    # Score components
    skill_score = (len(matched) / len(required)) * 60 if required else 30
    experience_bonus = min(resume.years_experience or 0, 10) * 2
    education_bonus = 10 if resume.education else 0

    total_score = min(round(skill_score + experience_bonus + education_bonus), 100)

    return {
        "score": total_score,
        "matched_skills": matched,
        "missing_skills": missing,
        "explanation": (
            f"Candidate matches {len(matched)}/{len(required)} required skills. "
            + (f"Has {resume.years_experience} years of experience. " if resume.years_experience else "")
            + (f"{len(missing)} skills missing: {', '.join(missing[:5])}." if missing else "All required skills matched!")
        ),
    }
