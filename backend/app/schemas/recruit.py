"""Pydantic v2 schemas for DClaw Recruit."""

from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


# ── Job Requisition ──────────────────────────────────────────────

class JobRequisitionBase(BaseModel):
    title: str = Field(..., max_length=255)
    department: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=255)
    salary_range: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=5000)
    status: str = "open"


class JobRequisitionCreate(JobRequisitionBase):
    pass


class JobRequisitionUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    department: str | None = Field(None, max_length=100)
    location: str | None = Field(None, max_length=255)
    salary_range: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=5000)
    status: str | None = None


class JobRequisitionResponse(JobRequisitionBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime
    candidate_count: int = 0


# ── Candidate ────────────────────────────────────────────────────

class CandidateBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: str = Field(..., max_length=255)
    phone: str | None = Field(None, max_length=50)
    resume_url: str | None = Field(None, max_length=1024)
    source: str | None = Field(None, max_length=100)
    stage: str = "applied"
    job_id: UUID | None = None


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    email: str | None = Field(None, max_length=255)
    phone: str | None = Field(None, max_length=50)
    resume_url: str | None = Field(None, max_length=1024)
    source: str | None = Field(None, max_length=100)
    stage: str | None = None
    job_id: UUID | None = None


class CandidateResponse(CandidateBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


# ── Interview ────────────────────────────────────────────────────

class InterviewBase(BaseModel):
    candidate_id: UUID
    job_id: UUID | None = None
    scheduled_at: datetime | None = None
    interviewer: str | None = Field(None, max_length=255)
    feedback: str | None = Field(None, max_length=5000)
    rating: int | None = Field(None, ge=1, le=5)


class InterviewCreate(InterviewBase):
    pass


class InterviewUpdate(BaseModel):
    scheduled_at: datetime | None = None
    interviewer: str | None = Field(None, max_length=255)
    feedback: str | None = Field(None, max_length=5000)
    rating: int | None = Field(None, ge=1, le=5)


class InterviewResponse(InterviewBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime


# ── Pagination ───────────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    items: list
    total: int
    limit: int
    offset: int
