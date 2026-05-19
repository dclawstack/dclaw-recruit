"""AI Screening Interview service — AI conducts first-round screening.

Handles async screening with voice/video analysis, soft-skills assessment,
and culture-fit evaluation. Replaces traditional phone screens.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID


@dataclass
class ScreeningQuestion:
    id: str
    category: str  # "technical", "behavioral", "situational", "culture"
    question: str
    expected_themes: list[str] = field(default_factory=list)
    max_duration_seconds: int = 120  # 2 min per question


@dataclass
class ScreeningResult:
    candidate_id: UUID
    overall_score: float  # 0-100
    category_scores: dict[str, float]
    communication_score: float  # clarity, pace, confidence
    technical_accuracy: float
    culture_fit_score: float
    sentiment: str  # "positive", "neutral", "negative"
    red_flags: list[str]
    strengths: list[str]
    transcript_summary: str
    recommendation: str  # "advance", "hold", "reject"


# Screening question bank by role
SCREENING_QUESTIONS = {
    "engineering": [
        ScreeningQuestion("q1", "technical", 
            "Walk me through the most complex system you've architected. What trade-offs did you make?",
            ["architecture", "trade-offs", "scalability", "design patterns"]),
        ScreeningQuestion("q2", "behavioral",
            "Tell me about a time you disagreed with a technical decision. How did you handle it?",
            ["disagreement", "collaboration", "resolution", "data-driven"]),
        ScreeningQuestion("q3", "situational",
            "If you discovered a critical bug in production 1 hour before a major release, what would you do?",
            ["incident response", "prioritization", "communication", "rollback"]),
        ScreeningQuestion("q4", "culture",
            "What engineering practices do you believe are non-negotiable for a healthy team?",
            ["testing", "code review", "documentation", "automation"]),
    ],
    "product": [
        ScreeningQuestion("q1", "technical",
            "How do you prioritize features when stakeholders disagree? Walk me through your framework.",
            ["prioritization", "stakeholders", "data-driven", "trade-offs"]),
        ScreeningQuestion("q2", "behavioral",
            "Tell me about a product that failed. What did you learn?",
            ["failure", "learning", "metrics", "iteration"]),
        ScreeningQuestion("q3", "situational",
            "You have 2 weeks to ship an MVP. Engineering says it takes 4. What do you do?",
            ["scope", "negotiation", "mvp", "trade-offs"]),
        ScreeningQuestion("q4", "culture",
            "How do you balance user requests with product vision?",
            ["user-focus", "vision", "data", "communication"]),
    ],
    "general": [
        ScreeningQuestion("q1", "technical",
            "Describe the most challenging project you've worked on and your specific contribution.",
            ["challenge", "contribution", "impact", "skills"]),
        ScreeningQuestion("q2", "behavioral",
            "Tell me about a time you had to learn something completely new to complete a project.",
            ["learning", "adaptability", "initiative", "result"]),
        ScreeningQuestion("q3", "situational",
            "If you had conflicting priorities from two managers, how would you handle it?",
            ["prioritization", "communication", "negotiation", "transparency"]),
        ScreeningQuestion("q4", "culture",
            "What type of work environment helps you do your best work?",
            ["environment", "collaboration", "autonomy", "feedback"]),
    ],
}


def get_screening_questions(role_type: str = "general") -> list[ScreeningQuestion]:
    """Get screening question set for a role type."""
    return SCREENING_QUESTIONS.get(role_type, SCREENING_QUESTIONS["general"])


def analyze_screening_response(
    question: ScreeningQuestion,
    response_text: str,
    response_duration_seconds: float,
) -> dict:
    """Analyze a candidate's response to a screening question.
    
    In production, this would use Whisper for transcription + LLM for analysis.
    Currently uses heuristic keyword/scoring analysis.
    """
    response_lower = response_text.lower()
    
    # Theme coverage
    themes_found = [t for t in question.expected_themes if t.lower() in response_lower]
    theme_score = (len(themes_found) / len(question.expected_themes)) * 100 if question.expected_themes else 50
    
    # Communication assessment (heuristic)
    word_count = len(response_text.split())
    is_too_short = word_count < 20
    is_too_long = word_count > 500
    speaking_rate = word_count / max(response_duration_seconds, 1) * 60  # words per minute
    
    communication_score = 100.0
    if is_too_short:
        communication_score -= 30
    if is_too_long:
        communication_score -= 10
    if speaking_rate < 80:
        communication_score -= 10  # too slow
    if speaking_rate > 200:
        communication_score -= 10  # too fast
    communication_score = max(0, min(100, communication_score))
    
    # Red flags detection
    red_flags = []
    red_flag_phrases = [
        "i don't know", "no idea", "whatever", "not my problem",
        "i hate", "terrible", "worst", "boring",
    ]
    for phrase in red_flag_phrases:
        if phrase in response_lower:
            red_flags.append(f"Negative language detected: '{phrase}'")
    
    # Strengths detection
    strengths = []
    strength_phrases = [
        "i built", "i led", "i designed", "i improved", "i optimized",
        "we achieved", "i learned", "i collaborated", "i solved",
        "growth", "impact", "results", "data-driven",
    ]
    for phrase in strength_phrases:
        if phrase in response_lower:
            strengths.append(f"Positive indicator: '{phrase}'")
    
    return {
        "question_id": question.id,
        "category": question.category,
        "theme_coverage": round(theme_score, 1),
        "themes_covered": themes_found,
        "themes_missed": [t for t in question.expected_themes if t not in themes_found],
        "communication_score": round(communication_score, 1),
        "word_count": word_count,
        "speaking_rate_wpm": round(speaking_rate, 1),
        "red_flags": red_flags,
        "strengths": strengths[:5],
    }


def generate_screening_result(
    candidate_id: UUID,
    role_type: str,
    responses: list[dict],  # list of {question_id, text, duration_seconds}
) -> ScreeningResult:
    """Generate an overall screening result from all question responses."""
    questions = get_screening_questions(role_type)
    question_map = {q.id: q for q in questions}
    
    all_analyses = []
    for resp in responses:
        q = question_map.get(resp["question_id"])
        if q:
            analysis = analyze_screening_response(q, resp["text"], resp.get("duration_seconds", 60))
            all_analyses.append(analysis)
    
    if not all_analyses:
        return ScreeningResult(
            candidate_id=candidate_id,
            overall_score=0,
            category_scores={},
            communication_score=0,
            technical_accuracy=0,
            culture_fit_score=0,
            sentiment="neutral",
            red_flags=[],
            strengths=[],
            transcript_summary="No responses analyzed",
            recommendation="reject",
        )
    
    # Aggregate scores
    avg_comm = sum(a["communication_score"] for a in all_analyses) / len(all_analyses)
    avg_theme = sum(a["theme_coverage"] for a in all_analyses) / len(all_analyses)
    
    # Category scores
    category_scores: dict[str, list[float]] = {}
    for a in all_analyses:
        cat = a["category"]
        if cat not in category_scores:
            category_scores[cat] = []
        category_scores[cat].append(a["theme_coverage"])
    
    avg_category = {k: round(sum(v)/len(v), 1) for k, v in category_scores.items()}
    
    # Technical = avg of technical category; Culture = culture category
    technical = avg_category.get("technical", 50)
    culture = avg_category.get("culture", avg_category.get("behavioral", 50))
    
    overall = (avg_comm * 0.25 + avg_theme * 0.35 + technical * 0.25 + culture * 0.15)
    
    # Recommendation
    if overall >= 75:
        recommendation = "advance"
    elif overall >= 50:
        recommendation = "hold"
    else:
        recommendation = "reject"
    
    all_red_flags = []
    all_strengths = []
    for a in all_analyses:
        all_red_flags.extend(a["red_flags"])
        all_strengths.extend(a["strengths"])
    
    # Sentiment
    if len(all_red_flags) >= 3:
        sentiment = "negative"
    elif len(all_strengths) >= len(all_red_flags) * 2:
        sentiment = "positive"
    else:
        sentiment = "neutral"
    
    return ScreeningResult(
        candidate_id=candidate_id,
        overall_score=round(overall, 1),
        category_scores=avg_category,
        communication_score=round(avg_comm, 1),
        technical_accuracy=round(technical, 1),
        culture_fit_score=round(culture, 1),
        sentiment=sentiment,
        red_flags=all_red_flags[:5],
        strengths=all_strengths[:5],
        transcript_summary=f"Analyzed {len(all_analyses)} responses across {len(avg_category)} categories. "
                          f"Communication: {avg_comm:.0f}/100. Technical: {technical:.0f}/100. "
                          f"Culture: {culture:.0f}/100.",
        recommendation=recommendation,
    )
