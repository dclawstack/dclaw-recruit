"""Structured Interview Scorecard service."""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class ScorecardRubric:
    category: str
    weight: float  # 0.0 to 1.0
    criteria: list[str] = field(default_factory=list)


@dataclass
class ScorecardResult:
    candidate_id: UUID
    total_score: float
    category_scores: dict[str, float]
    strengths: list[str]
    weaknesses: list[str]
    overall_recommendation: str  # "strong_hire", "hire", "maybe", "no_hire"


# Default scorecard templates by role type
SCORECARD_TEMPLATES = {
    "engineering": [
        ScorecardRubric("Technical Skills", 0.35, [
            "Code quality and best practices",
            "System design and architecture",
            "Problem-solving and debugging",
            "Knowledge of relevant tech stack",
        ]),
        ScorecardRubric("Communication", 0.20, [
            "Explains technical concepts clearly",
            "Collaborates well in team settings",
            "Provides constructive feedback",
        ]),
        ScorecardRubric("Problem Solving", 0.20, [
            "Analytical thinking approach",
            "Breaks down complex problems",
            "Considers edge cases and trade-offs",
        ]),
        ScorecardRubric("Culture Fit", 0.15, [
            "Alignment with company values",
            "Growth mindset and curiosity",
            "Initiative and ownership",
        ]),
        ScorecardRubric("Leadership", 0.10, [
            "Mentoring and knowledge sharing",
            "Project planning and estimation",
            "Cross-functional collaboration",
        ]),
    ],
    "product": [
        ScorecardRubric("Product Sense", 0.30, [
            "User empathy and research skills",
            "Feature prioritization",
            "Metrics-driven decision making",
        ]),
        ScorecardRubric("Execution", 0.25, [
            "Project management",
            "Stakeholder management",
            "Delivering outcomes on time",
        ]),
        ScorecardRubric("Communication", 0.20, [
            "Written and verbal clarity",
            "Presentation skills",
            "Cross-team alignment",
        ]),
        ScorecardRubric("Analytical", 0.15, [
            "Data analysis capability",
            "A/B testing knowledge",
            "SQL and dashboard skills",
        ]),
        ScorecardRubric("Leadership", 0.10, [
            "Vision and strategy",
            "Team motivation",
            "Conflict resolution",
        ]),
    ],
    "general": [
        ScorecardRubric("Role-Specific Skills", 0.35, [
            "Relevant experience and expertise",
            "Technical/domain knowledge",
            "Tool and process familiarity",
        ]),
        ScorecardRubric("Communication", 0.25, [
            "Clarity of expression",
            "Active listening",
            "Professionalism",
        ]),
        ScorecardRubric("Problem Solving", 0.20, [
            "Critical thinking",
            "Creativity and innovation",
            "Decision-making quality",
        ]),
        ScorecardRubric("Culture & Values", 0.20, [
            "Team fit and collaboration",
            "Adaptability and resilience",
            "Ethics and integrity",
        ]),
    ],
}


def get_scorecard_template(role_type: str = "general") -> list[ScorecardRubric]:
    """Get a scorecard template for a given role type."""
    return SCORECARD_TEMPLATES.get(role_type, SCORECARD_TEMPLATES["general"])


def calculate_scorecard(
    category_scores: dict[str, float],
    template: list[ScorecardRubric],
) -> ScorecardResult:
    """Calculate overall score from category scores weighted by template.

    Args:
        category_scores: Dict of category_name -> score (1-5)
        template: List of ScorecardRubric defining weights

    Returns:
        ScorecardResult with total, strengths, weaknesses, recommendation
    """
    if not category_scores or not template:
        return ScorecardResult(
            candidate_id=UUID("00000000-0000-0000-0000-000000000000"),
            total_score=0.0,
            category_scores={},
            strengths=[],
            weaknesses=[],
            overall_recommendation="no_hire",
        )

    total = 0.0
    total_weight = 0.0
    strengths = []
    weaknesses = []

    for rubric in template:
        score = category_scores.get(rubric.category, 2.5)
        weighted = score * rubric.weight
        total += weighted
        total_weight += rubric.weight

        if score >= 4.0:
            strengths.append(f"{rubric.category}: {score:.1f}/5")
        elif score <= 2.0:
            weaknesses.append(f"{rubric.category}: {score:.1f}/5")

    # Normalize
    if total_weight > 0:
        total = (total / total_weight)

    # Determine recommendation
    if total >= 4.0:
        recommendation = "strong_hire"
    elif total >= 3.0:
        recommendation = "hire"
    elif total >= 2.0:
        recommendation = "maybe"
    else:
        recommendation = "no_hire"

    return ScorecardResult(
        candidate_id=UUID("00000000-0000-0000-0000-000000000000"),
        total_score=round(total, 1),
        category_scores=category_scores,
        strengths=strengths if strengths else ["No standout strengths identified"],
        weaknesses=weaknesses if weaknesses else ["No major weaknesses identified"],
        overall_recommendation=recommendation,
    )
