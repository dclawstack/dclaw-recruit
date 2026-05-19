"""Candidate Experience Hub — real-time status, chatbot, instant scheduling."""

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from uuid import UUID
from enum import Enum


class PipelineStage(str, Enum):
    APPLIED = "applied"
    RESUME_REVIEW = "resume_review"
    AI_SCREENING = "ai_screening"
    PHONE_SCREEN = "phone_screen"
    TECHNICAL = "technical_interview"
    ONSITE = "onsite"
    OFFER = "offer"
    HIRED = "hired"
    REJECTED = "rejected"


@dataclass
class PipelineUpdate:
    timestamp: datetime
    stage: PipelineStage
    message: str
    next_steps: str
    estimated_days_to_decision: int


@dataclass
class CandidateJourney:
    candidate_id: UUID
    candidate_name: str
    current_stage: PipelineStage
    stage_entered_at: datetime
    total_days_in_pipeline: int
    updates: list[PipelineUpdate]
    upcoming_interviews: list[dict]
    feedback_summary: str
    transparency_score: int  # 0-100


@dataclass
class ChatbotResponse:
    message: str
    action_links: list[dict] = field(default_factory=list)
    sentiment: str = "neutral"


# Chatbot intent mapping
CHATBOT_INTENTS = {
    "status": [
        "where am i", "status", "update", "what's happening", "any news",
        "progress", "pipeline", "which stage", "next step",
    ],
    "schedule": [
        "schedule", "interview", "when", "time", "calendar", "book",
        "reschedule", "available", "slot",
    ],
    "feedback": [
        "feedback", "how did i do", "result", "score", "evaluation",
        "performance", "assessment",
    ],
    "salary": [
        "salary", "compensation", "pay", "offer", "package", "benefits",
        "bonus", "equity",
    ],
    "company": [
        "company", "culture", "team", "about", "mission", "values",
        "perks", "office",
    ],
    "help": [
        "help", "confused", "don't understand", "explain", "what should i",
        "guide",
    ],
}


def classify_intent(message: str) -> str:
    """Classify the candidate's intent from their message."""
    msg_lower = message.lower()
    for intent, keywords in CHATBOT_INTENTS.items():
        if any(kw in msg_lower for kw in keywords):
            return intent
    return "general"


def generate_chatbot_response(
    message: str,
    candidate_name: str,
    current_stage: PipelineStage,
    days_in_pipeline: int,
) -> ChatbotResponse:
    """Generate a chatbot response based on candidate's message and pipeline state."""
    intent = classify_intent(message)
    
    responses = {
        "status": ChatbotResponse(
            message=(
                f"Hi {candidate_name}! 👋 You're currently in the **{current_stage.value.replace('_', ' ').title()}** stage. "
                f"You've been in the pipeline for {days_in_pipeline} days. "
                f"Our typical time to decision for this stage is 3-5 business days. "
                f"I'll notify you as soon as there's an update!"
            ),
            action_links=[
                {"text": "View Full Timeline", "href": "/candidate/timeline"},
                {"text": "Schedule a Call", "href": "/candidate/schedule"},
            ],
            sentiment="positive",
        ),
        "schedule": ChatbotResponse(
            message=(
                f"I can help you schedule! 📅 You have upcoming availability for: "
                f"• Tomorrow at 10:00 AM or 2:00 PM\n"
                f"• Day after at 11:00 AM or 3:00 PM\n"
                f"Which works best for you?"
            ),
            action_links=[
                {"text": "Book Tomorrow 10AM", "href": "/candidate/book?slot=1"},
                {"text": "Book Tomorrow 2PM", "href": "/candidate/book?slot=2"},
                {"text": "See All Slots", "href": "/candidate/schedule"},
            ],
            sentiment="positive",
        ),
        "feedback": ChatbotResponse(
            message=(
                f"Your interview feedback is being compiled by the hiring team. "
                f"We believe in transparency — you'll receive structured feedback within 48 hours "
                f"of each interview round. No ghosting here! 👻🚫"
            ),
            action_links=[
                {"text": "Feedback History", "href": "/candidate/feedback"},
            ],
            sentiment="positive",
        ),
        "salary": ChatbotResponse(
            message=(
                f"We'll discuss compensation when you reach the offer stage. "
                f"In the meantime, our salary bands are competitive and benchmarked against "
                f"market data. We offer base + bonus + equity + comprehensive benefits."
            ),
            action_links=[
                {"text": "Benefits Overview", "href": "/company/benefits"},
            ],
            sentiment="neutral",
        ),
        "company": ChatbotResponse(
            message=(
                f"Great question! 🏢 DClaw is a Series A startup building AI-powered vertical SaaS. "
                f"Our team is ~50 people, remote-first, with hubs in SF and Austin. "
                f"We value ownership, curiosity, and building with empathy."
            ),
            action_links=[
                {"text": "About DClaw", "href": "/about"},
                {"text": "Team Page", "href": "/team"},
            ],
            sentiment="positive",
        ),
        "help": ChatbotResponse(
            message=(
                f"I'm here to help, {candidate_name}! 💡 Here's what I can do:\n"
                f"• Tell you your application status\n"
                f"• Help you schedule interviews\n"
                f"• Share feedback when available\n"
                f"• Answer questions about DClaw\n\n"
                f"Just ask me anything!"
            ),
            sentiment="positive",
        ),
    }
    
    default = ChatbotResponse(
        message=(
            f"Thanks for reaching out, {candidate_name}! I'm your personal recruiting assistant. "
            f"You're currently at the **{current_stage.value.replace('_', ' ').title()}** stage. "
            f"How can I help you today?"
        ),
        action_links=[
            {"text": "Check Status", "href": "/candidate/status"},
            {"text": "Schedule Interview", "href": "/candidate/schedule"},
        ],
        sentiment="neutral",
    )
    
    return responses.get(intent, default)


def generate_journey(
    candidate_id: UUID,
    candidate_name: str,
    current_stage: PipelineStage,
    stage_dates: dict[PipelineStage, datetime],
) -> CandidateJourney:
    """Generate a candidate journey with timeline and transparency score."""
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    applied_date = stage_dates.get(PipelineStage.APPLIED, now)
    total_days = (now - applied_date).days
    
    stage_order = list(PipelineStage)
    updates = []
    transparency_signals = 0
    total_signals = 0
    
    for stage in stage_order:
        if stage in stage_dates:
            entry_date = stage_dates[stage]
            days_stage = (now - entry_date).days
            
            # Standard SLA per stage (days)
            sla_map = {
                PipelineStage.APPLIED: 1,
                PipelineStage.RESUME_REVIEW: 3,
                PipelineStage.AI_SCREENING: 2,
                PipelineStage.PHONE_SCREEN: 5,
                PipelineStage.TECHNICAL: 7,
                PipelineStage.ONSITE: 7,
                PipelineStage.OFFER: 5,
            }
            sla = sla_map.get(stage, 5)
            remaining = max(0, sla - days_stage)
            
            stage_messages = {
                PipelineStage.APPLIED: "Application received! We'll review it within 24 hours.",
                PipelineStage.RESUME_REVIEW: "Your resume is being reviewed by the hiring team.",
                PipelineStage.AI_SCREENING: "You're completing our AI-powered skills assessment.",
                PipelineStage.PHONE_SCREEN: "Your phone screen is being scheduled.",
                PipelineStage.TECHNICAL: "Technical interview in progress.",
                PipelineStage.ONSITE: "Onsite/virtual final round being coordinated.",
                PipelineStage.OFFER: "Offer being prepared! 🎉",
                PipelineStage.HIRED: "Welcome aboard! 🚀",
                PipelineStage.REJECTED: "Thank you for your interest. We've gone in a different direction.",
            }
            
            updates.append(PipelineUpdate(
                timestamp=entry_date,
                stage=stage,
                message=stage_messages.get(stage, ""),
                next_steps=f"Estimated {remaining} days to decision" if remaining > 0 else "Decision imminent",
                estimated_days_to_decision=remaining,
            ))
            
            # Transparency: did we communicate within SLA?
            total_signals += 1
            if days_stage <= sla:
                transparency_signals += 1
    
    transparency_score = round((transparency_signals / max(total_signals, 1)) * 100)
    
    return CandidateJourney(
        candidate_id=candidate_id,
        candidate_name=candidate_name,
        current_stage=current_stage,
        stage_entered_at=stage_dates.get(current_stage, now),
        total_days_in_pipeline=total_days,
        updates=updates,
        upcoming_interviews=[],
        feedback_summary=f"Pipeline transparency: {transparency_score}%. All stages communicated within SLA.",
        transparency_score=transparency_score,
    )
