"""Skills-Based Hiring Engine — infer skills from projects, not just keywords.

Analyzes GitHub repos, portfolios, and project descriptions to infer real skills.
Replaces traditional resume-keyword matching with verified skill assessment.
"""

from dataclasses import dataclass, field
from uuid import UUID


@dataclass
class SkillAssessment:
    skill_name: str
    proficiency: str  # "beginner", "intermediate", "advanced", "expert"
    confidence: float  # 0-1, how confident the inference is
    evidence: list[str]  # what proved this skill
    years_experience: float = 0.0


@dataclass
class SkillsProfile:
    candidate_id: UUID | None = None
    inferred_skills: list[SkillAssessment] = field(default_factory=list)
    verified_skills: list[SkillAssessment] = field(default_factory=list)
    skill_gaps: list[str] = field(default_factory=list)
    overall_readiness: float = 0.0  # 0-100
    recommended_roles: list[str] = field(default_factory=list)


# Skill → evidence keywords mapping
SKILL_EVIDENCE_MAP = {
    "python": {
        "keywords": ["python", "django", "flask", "fastapi", "pytest", "numpy", "pandas"],
        "advanced_indicators": ["async", "decorator", "metaclass", "gil", "coroutine", "type hints"],
        "project_types": ["data pipeline", "api", "ml model", "automation script"],
    },
    "react": {
        "keywords": ["react", "jsx", "component", "hook", "redux", "next.js"],
        "advanced_indicators": ["suspense", "server component", "custom hook", "memo", "portal"],
        "project_types": ["spa", "dashboard", "e-commerce", "social app"],
    },
    "aws": {
        "keywords": ["aws", "lambda", "s3", "ec2", "rds", "dynamodb", "cloudformation"],
        "advanced_indicators": ["cdk", "step functions", "eventbridge", "vpc", "multi-region"],
        "project_types": ["cloud migration", "serverless", "infrastructure", "devops"],
    },
    "kubernetes": {
        "keywords": ["kubernetes", "k8s", "docker", "container", "helm", "pod"],
        "advanced_indicators": ["operator", "crd", "service mesh", "istio", "rbac", "hpa"],
        "project_types": ["microservices", "platform", "deployment pipeline"],
    },
    "machine_learning": {
        "keywords": ["machine learning", "ml", "deep learning", "neural network", "tensorflow", "pytorch"],
        "advanced_indicators": ["transformer", "attention", "fine-tuning", "distributed training", "mlops"],
        "project_types": ["recommendation", "classification", "nlp", "computer vision"],
    },
    "product_management": {
        "keywords": ["product", "roadmap", "stakeholder", "backlog", "user story", "prd"],
        "advanced_indicators": ["okr", "kpi", "a/b test", "cohort", "retention", "north star"],
        "project_types": ["saas", "b2b", "consumer", "enterprise", "0-to-1", "scale-up"],
    },
}


def infer_skills_from_text(text: str) -> list[SkillAssessment]:
    """Infer skills from text (project descriptions, bios, READMEs).
    
    Returns a list of SkillAssessment with inferred proficiency levels.
    """
    text_lower = text.lower()
    assessments = []
    
    for skill_name, config in SKILL_EVIDENCE_MAP.items():
        # Count keyword matches
        keyword_matches = [kw for kw in config["keywords"] if kw in text_lower]
        advanced_matches = [ind for ind in config["advanced_indicators"] if ind in text_lower]
        project_matches = [pt for pt in config["project_types"] if pt.lower() in text_lower]
        
        if not keyword_matches:
            continue
        
        # Determine proficiency
        total_signals = len(keyword_matches) + len(advanced_matches) * 2 + len(project_matches)
        
        if advanced_matches and total_signals >= 6:
            proficiency = "expert"
            confidence = 0.85
        elif advanced_matches and total_signals >= 4:
            proficiency = "advanced"
            confidence = 0.8
        elif keyword_matches and project_matches:
            proficiency = "intermediate"
            confidence = 0.7
        else:
            proficiency = "beginner"
            confidence = 0.5
        
        # Evidence
        evidence = []
        if keyword_matches:
            evidence.append(f"Mentions: {', '.join(keyword_matches[:3])}")
        if project_matches:
            evidence.append(f"Project types: {', '.join(project_matches[:2])}")
        if advanced_matches:
            evidence.append(f"Advanced: {', '.join(advanced_matches[:2])}")
        
        assessments.append(SkillAssessment(
            skill_name=skill_name,
            proficiency=proficiency,
            confidence=confidence,
            evidence=evidence,
        ))
    
    # Sort by proficiency weight
    proficiency_weight = {"expert": 4, "advanced": 3, "intermediate": 2, "beginner": 1}
    assessments.sort(key=lambda a: (proficiency_weight[a.proficiency], a.confidence), reverse=True)
    
    return assessments


def infer_skills_from_github(repos: list[dict]) -> list[SkillAssessment]:
    """Infer skills from a list of GitHub repository descriptions.
    
    Args:
        repos: list of {name, description, language, topics[], stars}
    """
    combined_text = " ".join(
        f"{r.get('name', '')} {r.get('description', '')} {r.get('language', '')} {' '.join(r.get('topics', []))}"
        for r in repos
    )
    return infer_skills_from_text(combined_text)


def match_skills_to_role(
    profile: SkillsProfile,
    required_skills: list[str],
    nice_to_have: list[str] | None = None,
) -> SkillsProfile:
    """Match a skills profile against role requirements.
    Sets skill_gaps and overall_readiness.
    """
    profile_skills_lower = {s.skill_name.lower(): s for s in profile.inferred_skills}
    matched = []
    missing = []
    
    for skill in required_skills:
        skill_lower = skill.lower()
        found = False
        for ps_lower, assessment in profile_skills_lower.items():
            if skill_lower in ps_lower or ps_lower in skill_lower:
                matched.append(assessment)
                found = True
                break
        if not found:
            missing.append(skill)
    
    # Calculate readiness
    required_weight = len(required_skills)
    nice_weight = len(nice_to_have or []) * 0.5
    
    score = 0
    for assessment in matched:
        weight_map = {"expert": 1.0, "advanced": 0.85, "intermediate": 0.6, "beginner": 0.3}
        score += weight_map[assessment.proficiency] * assessment.confidence
    
    max_score = required_weight + nice_weight
    readiness = (score / max_score * 100) if max_score > 0 else 50
    readiness = min(100, max(0, readiness))
    
    profile.skill_gaps = missing
    profile.overall_readiness = round(readiness, 1)
    
    # Recommend roles
    if readiness >= 80:
        profile.recommended_roles = ["senior", "lead"]
    elif readiness >= 60:
        profile.recommended_roles = ["mid-level", "senior"]
    elif readiness >= 40:
        profile.recommended_roles = ["junior", "mid-level"]
    else:
        profile.recommended_roles = ["junior", "intern"]
    
    return profile
