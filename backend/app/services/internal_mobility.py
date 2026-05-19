"""Internal Mobility Engine — match existing employees to open roles.

AI-driven internal talent marketplace that reduces external hiring costs
by surfacing internal candidates who are ready to move.
"""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class InternalCandidate:
    employee_id: UUID
    name: str
    current_role: str
    current_department: str
    tenure_months: int
    skills: list[str]
    performance_rating: float  # 1-5
    career_aspirations: list[str] = field(default_factory=list)
    mobility_score: float = 0.0
    match_explanation: str = ""


@dataclass
class MobilityMatch:
    candidate: InternalCandidate
    job_title: str
    job_department: str
    match_score: float
    skill_overlap: list[str]
    skill_gaps: list[str]
    readiness: str  # "ready_now", "ready_3mo", "ready_6mo", "ready_12mo"
    recommended_lateral: bool
    explanation: str


# Simulated internal employee database
_INTERNAL_EMPLOYEES = [
    InternalCandidate(
        employee_id=UUID("e0000000-0000-0000-0000-000000000001"),
        name="Diana Ross", current_role="Senior Backend Engineer",
        current_department="Engineering", tenure_months=24,
        skills=["python", "postgresql", "aws", "docker", "kubernetes"],
        performance_rating=4.5,
        career_aspirations=["tech lead", "architecture"],
    ),
    InternalCandidate(
        employee_id=UUID("e0000000-0000-0000-0000-000000000002"),
        name="James Wilson", current_role="Product Analyst",
        current_department="Product", tenure_months=18,
        skills=["sql", "tableau", "data analysis", "a/b testing", "python"],
        performance_rating=4.2,
        career_aspirations=["product manager", "data science"],
    ),
    InternalCandidate(
        employee_id=UUID("e0000000-0000-0000-0000-000000000003"),
        name="Maria Garcia", current_role="Marketing Manager",
        current_department="Marketing", tenure_months=36,
        skills=["marketing", "content strategy", "analytics", "leadership", "project management"],
        performance_rating=4.8,
        career_aspirations=["director", "growth"],
    ),
    InternalCandidate(
        employee_id=UUID("e0000000-0000-0000-0000-000000000004"),
        name="Alex Turner", current_role="Junior Frontend Dev",
        current_department="Engineering", tenure_months=12,
        skills=["react", "typescript", "tailwindcss", "next.js", "git"],
        performance_rating=3.8,
        career_aspirations=["full stack", "tech lead"],
    ),
    InternalCandidate(
        employee_id=UUID("e0000000-0000-0000-0000-000000000005"),
        name="Priya Sharma", current_role="Customer Success Lead",
        current_department="Customer Success", tenure_months=30,
        skills=["customer success", "account management", "salesforce", "data analysis", "leadership"],
        performance_rating=4.6,
        career_aspirations=["sales", "operations"],
    ),
]


def find_internal_candidates(
    job_title: str,
    job_department: str,
    required_skills: list[str],
    prefer_internal: bool = True,
    max_candidates: int = 5,
) -> list[MobilityMatch]:
    """Find internal candidates matching an open role.
    
    Prioritizes internal mobility before external sourcing.
    """
    required_lower = set(s.lower() for s in required_skills)
    matches = []
    
    for emp in _INTERNAL_EMPLOYEES:
        emp_skills_lower = set(s.lower() for s in emp.skills)
        overlap = required_lower & emp_skills_lower
        gaps = required_lower - emp_skills_lower
        
        if not overlap:
            continue
        
        # Score components
        skill_match_pct = len(overlap) / len(required_lower) if required_lower else 0.5
        perf_factor = emp.performance_rating / 5.0
        tenure_factor = min(emp.tenure_months / 24, 1.0)  # cap at 2 years
        aspiration_match = any(
            asp.lower() in job_title.lower() or job_title.lower() in asp.lower()
            for asp in emp.career_aspirations
        )
        
        score = (
            skill_match_pct * 50 +
            perf_factor * 25 +
            tenure_factor * 15 +
            (10 if aspiration_match else 0)
        )
        
        # Readiness
        if skill_match_pct >= 0.8:
            readiness = "ready_now"
        elif skill_match_pct >= 0.6:
            readiness = "ready_3mo"
        elif skill_match_pct >= 0.4:
            readiness = "ready_6mo"
        else:
            readiness = "ready_12mo"
        
        # Lateral move?
        is_lateral = emp.current_department != job_department
        
        matches.append(MobilityMatch(
            candidate=emp,
            job_title=job_title,
            job_department=job_department,
            match_score=round(score, 1),
            skill_overlap=list(overlap),
            skill_gaps=list(gaps),
            readiness=readiness,
            recommended_lateral=is_lateral,
            explanation=(
                f"{emp.name} ({emp.current_role}) matches {len(overlap)}/{len(required_lower)} skills. "
                f"Performance: {emp.performance_rating}/5. "
                f"{'Career aspiration aligned. ' if aspiration_match else ''}"
                f"{'Lateral move from ' + emp.current_department + '. ' if is_lateral else ''}"
                f"Estimated readiness: {readiness.replace('_', ' ')}."
            ),
        ))
    
    matches.sort(key=lambda m: m.match_score, reverse=True)
    return matches[:max_candidates]


def calculate_internal_hire_savings(
    external_cost_per_hire: float = 25000,
    internal_cost: float = 5000,
    time_to_productivity_external_days: int = 90,
    time_to_productivity_internal_days: int = 30,
) -> dict:
    """Calculate cost savings from internal hiring vs external."""
    savings = external_cost_per_hire - internal_cost
    time_savings_days = time_to_productivity_external_days - time_to_productivity_internal_days
    
    return {
        "cost_savings": savings,
        "time_savings_days": time_savings_days,
        "productivity_gain_days": time_savings_days,
        "retention_boost": "Internal hires have 20% higher 2-year retention",
        "total_roi": f"${savings:,} saved per internal hire, {time_savings_days} days faster to productivity",
    }
