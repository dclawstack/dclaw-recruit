import uuid
import random
from datetime import datetime, timezone

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class JobPostCreate(BaseModel):
    title: str
    description: str


class JobPost(BaseModel):
    id: str
    title: str
    description: str
    candidate_pool_size: int
    top_candidate_match: str
    time_to_fill_days: int
    created_at: str


class Candidate(BaseModel):
    id: str
    name: str
    match_score: int
    rank: int


@router.post("/jobs", response_model=JobPost)
async def create_job(payload: JobPostCreate) -> JobPost:
    return JobPost(
        id=str(uuid.uuid4()),
        title=payload.title,
        description=payload.description,
        candidate_pool_size=random.randint(5, 200),
        top_candidate_match="Alice Johnson (94%)",
        time_to_fill_days=random.randint(14, 60),
        created_at=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/jobs/{job_id}/candidates", response_model=list[Candidate])
async def get_candidates(job_id: str) -> list[Candidate]:
    return [
        Candidate(id=str(uuid.uuid4()), name="Alice Johnson", match_score=94, rank=1),
        Candidate(id=str(uuid.uuid4()), name="Bob Smith", match_score=89, rank=2),
        Candidate(id=str(uuid.uuid4()), name="Carol White", match_score=85, rank=3),
    ]
