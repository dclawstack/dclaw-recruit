"""DClaw Recruit API v1 — Jobs, Candidates, Interviews."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.job import JobRequisition
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.schemas.recruit import (
    JobRequisitionCreate,
    JobRequisitionUpdate,
    JobRequisitionResponse,
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    InterviewCreate,
    InterviewUpdate,
    InterviewResponse,
    PaginatedResponse,
)
from app.repositories.recruit import JobRepository, CandidateRepository, InterviewRepository

router = APIRouter()


# ── Helper ───────────────────────────────────────────────────────

def _job_to_response(job: JobRequisition) -> JobRequisitionResponse:
    count = len(job.candidates) if job.candidates else 0
    return JobRequisitionResponse(
        id=job.id,
        title=job.title,
        department=job.department,
        location=job.location,
        salary_range=job.salary_range,
        description=job.description,
        status=job.status.value,
        created_at=job.created_at,
        updated_at=job.updated_at,
        candidate_count=count,
    )


# ── Jobs ─────────────────────────────────────────────────────────

@router.get("/jobs", response_model=PaginatedResponse)
async def list_jobs(
    query: str | None = Query(None, description="Search by title or department"),
    status: str | None = Query(None, description="Filter: open, paused, closed"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = JobRepository(db)
    items, total = await repo.search(query=query, status=status, limit=limit, offset=offset)
    return PaginatedResponse(
        items=[_job_to_response(job) for job in items],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/jobs", response_model=JobRequisitionResponse, status_code=201)
async def create_job(payload: JobRequisitionCreate, db: AsyncSession = Depends(get_db)):
    repo = JobRepository(db)
    job = JobRequisition(**payload.model_dump())
    created = await repo.create(job)
    return _job_to_response(created)


@router.get("/jobs/{job_id}", response_model=JobRequisitionResponse)
async def get_job(job_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return _job_to_response(job)


@router.patch("/jobs/{job_id}", response_model=JobRequisitionResponse)
async def update_job(job_id: UUID, payload: JobRequisitionUpdate, db: AsyncSession = Depends(get_db)):
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(job, key, value)
    await db.commit()
    await db.refresh(job)
    return _job_to_response(job)


@router.delete("/jobs/{job_id}", status_code=204)
async def delete_job(job_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = JobRepository(db)
    job = await repo.get_by_id(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    await repo.delete(job)


# ── Candidates ───────────────────────────────────────────────────

@router.get("/candidates", response_model=PaginatedResponse)
async def list_candidates(
    query: str | None = Query(None, description="Search by name or email"),
    stage: str | None = Query(None, description="Filter by stage"),
    job_id: UUID | None = Query(None, description="Filter by job ID"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = CandidateRepository(db)
    items, total = await repo.search(
        query=query, stage=stage, job_id=job_id, limit=limit, offset=offset
    )
    return PaginatedResponse(
        items=[
            CandidateResponse(
                id=c.id,
                name=c.name,
                email=c.email,
                phone=c.phone,
                resume_url=c.resume_url,
                source=c.source,
                stage=c.stage.value,
                job_id=c.job_id,
                created_at=c.created_at,
                updated_at=c.updated_at,
            )
            for c in items
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/candidates", response_model=CandidateResponse, status_code=201)
async def create_candidate(payload: CandidateCreate, db: AsyncSession = Depends(get_db)):
    repo = CandidateRepository(db)
    candidate = Candidate(**payload.model_dump())
    created = await repo.create(candidate)
    return CandidateResponse(
        id=created.id,
        name=created.name,
        email=created.email,
        phone=created.phone,
        resume_url=created.resume_url,
        source=created.source,
        stage=created.stage.value,
        job_id=created.job_id,
        created_at=created.created_at,
        updated_at=created.updated_at,
    )


@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(candidate_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = CandidateRepository(db)
    candidate = await repo.get_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return CandidateResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        resume_url=candidate.resume_url,
        source=candidate.source,
        stage=candidate.stage.value,
        job_id=candidate.job_id,
        created_at=candidate.created_at,
        updated_at=candidate.updated_at,
    )


@router.patch("/candidates/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: UUID, payload: CandidateUpdate, db: AsyncSession = Depends(get_db)
):
    repo = CandidateRepository(db)
    candidate = await repo.get_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(candidate, key, value)
    await db.commit()
    await db.refresh(candidate)
    return CandidateResponse(
        id=candidate.id,
        name=candidate.name,
        email=candidate.email,
        phone=candidate.phone,
        resume_url=candidate.resume_url,
        source=candidate.source,
        stage=candidate.stage.value,
        job_id=candidate.job_id,
        created_at=candidate.created_at,
        updated_at=candidate.updated_at,
    )


@router.delete("/candidates/{candidate_id}", status_code=204)
async def delete_candidate(candidate_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = CandidateRepository(db)
    candidate = await repo.get_by_id(candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    await repo.delete(candidate)


# ── Interviews ───────────────────────────────────────────────────

@router.get("/interviews", response_model=PaginatedResponse)
async def list_interviews(
    candidate_id: UUID | None = Query(None),
    job_id: UUID | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    repo = InterviewRepository(db)
    items, total = await repo.search(
        candidate_id=candidate_id, job_id=job_id, limit=limit, offset=offset
    )
    return PaginatedResponse(
        items=[
            InterviewResponse(
                id=i.id,
                candidate_id=i.candidate_id,
                job_id=i.job_id,
                scheduled_at=i.scheduled_at,
                interviewer=i.interviewer,
                feedback=i.feedback,
                rating=i.rating,
                created_at=i.created_at,
                updated_at=i.updated_at,
            )
            for i in items
        ],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("/interviews", response_model=InterviewResponse, status_code=201)
async def create_interview(payload: InterviewCreate, db: AsyncSession = Depends(get_db)):
    repo = InterviewRepository(db)
    interview = Interview(**payload.model_dump())
    created = await repo.create(interview)
    return InterviewResponse(
        id=created.id,
        candidate_id=created.candidate_id,
        job_id=created.job_id,
        scheduled_at=created.scheduled_at,
        interviewer=created.interviewer,
        feedback=created.feedback,
        rating=created.rating,
        created_at=created.created_at,
        updated_at=created.updated_at,
    )


@router.get("/interviews/{interview_id}", response_model=InterviewResponse)
async def get_interview(interview_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = InterviewRepository(db)
    interview = await repo.get_by_id(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return InterviewResponse(
        id=interview.id,
        candidate_id=interview.candidate_id,
        job_id=interview.job_id,
        scheduled_at=interview.scheduled_at,
        interviewer=interview.interviewer,
        feedback=interview.feedback,
        rating=interview.rating,
        created_at=interview.created_at,
        updated_at=interview.updated_at,
    )


@router.patch("/interviews/{interview_id}", response_model=InterviewResponse)
async def update_interview(
    interview_id: UUID, payload: InterviewUpdate, db: AsyncSession = Depends(get_db)
):
    repo = InterviewRepository(db)
    interview = await repo.get_by_id(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(interview, key, value)
    await db.commit()
    await db.refresh(interview)
    return InterviewResponse(
        id=interview.id,
        candidate_id=interview.candidate_id,
        job_id=interview.job_id,
        scheduled_at=interview.scheduled_at,
        interviewer=interview.interviewer,
        feedback=interview.feedback,
        rating=interview.rating,
        created_at=interview.created_at,
        updated_at=interview.updated_at,
    )


@router.delete("/interviews/{interview_id}", status_code=204)
async def delete_interview(interview_id: UUID, db: AsyncSession = Depends(get_db)):
    repo = InterviewRepository(db)
    interview = await repo.get_by_id(interview_id)
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    await repo.delete(interview)
