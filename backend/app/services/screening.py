"""AI Resume Screening service — ranks candidates against job descriptions."""

from app.services.resume_parser import ParsedResume, parse_resume, calculate_match_score


async def screen_resumes(
    resumes: list[dict],
    job_description: str,
    required_skills: list[str] | None = None,
) -> list[dict]:
    """Screen and rank multiple resumes against a job description.

    Args:
        resumes: List of dicts with at least 'id' and 'text' (resume content)
        job_description: The job description to match against
        required_skills: Optional list of required skills

    Returns:
        Sorted list with match scores, explanations, and bias flags
    """
    from app.services.resume_parser import ALL_SKILLS

    # Extract required skills from JD if not provided
    if not required_skills:
        jd_lower = job_description.lower()
        required_skills = [s for s in ALL_SKILLS if s in jd_lower]

    results = []

    for resume in resumes:
        parsed = parse_resume(resume.get("text", ""))
        match = calculate_match_score(parsed, job_description, required_skills)

        # Simple bias detection heuristics
        bias_flags = _detect_bias_risks(parsed)

        results.append(
            {
                "candidate_id": resume.get("id"),
                "name": parsed.name or "Unknown",
                "email": parsed.email or "Unknown",
                "match_score": match["score"],
                "matched_skills": match["matched_skills"],
                "missing_skills": match["missing_skills"],
                "years_experience": parsed.years_experience,
                "education": parsed.education,
                "explanation": match["explanation"],
                "bias_flags": bias_flags,
            }
        )

    # Sort by match score descending
    results.sort(key=lambda r: r["match_score"], reverse=True)
    return results


def _detect_bias_risks(parsed: ParsedResume) -> list[str]:
    """Detect potential bias signals in screening process."""
    flags = []

    # Check for missing standardized info
    if not parsed.years_experience:
        flags.append("No years of experience detected — manual review recommended")

    if not parsed.education:
        flags.append("No education detected — ensure education requirements are job-relevant")

    # Name-based bias risk
    if parsed.name and len(parsed.name.split()) < 2:
        flags.append("Single name detected — avoid name-based assumptions")

    return flags


async def anonymize_resume(text: str) -> str:
    """Remove PII from resume text for bias-free screening."""
    import re

    # Remove email
    text = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL REDACTED]", text)
    # Remove phone
    text = re.sub(
        r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        "[PHONE REDACTED]",
        text,
    )
    # Remove names (heuristic: first line)
    lines = text.split("\n")
    if lines:
        lines[0] = "[NAME REDACTED]"
    text = "\n".join(lines)

    return text
