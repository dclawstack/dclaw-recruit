"""Repositories for DClaw Recruit."""

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.job import JobRequisition
from app.models.candidate import Candidate
from app.models.interview import Interview
from app.repositories.base_repo import BaseRepository


class JobRepository(BaseRepository[JobRequisition]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, JobRequisition)

    async def search(
        self, query: str | None = None, status: str | None = None, limit: int = 20, offset: int = 0
    ) -> tuple[list[JobRequisition], int]:
        stmt = select(JobRequisition)
        count_stmt = select(func.count()).select_from(JobRequisition)

        if query:
            ilike = f"%{query}%"
            stmt = stmt.where(
                (JobRequisition.title.ilike(ilike)) | (JobRequisition.department.ilike(ilike))
            )
            count_stmt = count_stmt.where(
                (JobRequisition.title.ilike(ilike)) | (JobRequisition.department.ilike(ilike))
            )
        if status:
            stmt = stmt.where(JobRequisition.status == status)
            count_stmt = count_stmt.where(JobRequisition.status == status)

        stmt = stmt.order_by(JobRequisition.created_at.desc()).limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        return items, total


class CandidateRepository(BaseRepository[Candidate]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Candidate)

    async def search(
        self,
        query: str | None = None,
        stage: str | None = None,
        job_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Candidate], int]:
        stmt = select(Candidate)
        count_stmt = select(func.count()).select_from(Candidate)

        if query:
            ilike = f"%{query}%"
            stmt = stmt.where(
                (Candidate.name.ilike(ilike)) | (Candidate.email.ilike(ilike))
            )
            count_stmt = count_stmt.where(
                (Candidate.name.ilike(ilike)) | (Candidate.email.ilike(ilike))
            )
        if stage:
            stmt = stmt.where(Candidate.stage == stage)
            count_stmt = count_stmt.where(Candidate.stage == stage)
        if job_id:
            stmt = stmt.where(Candidate.job_id == job_id)
            count_stmt = count_stmt.where(Candidate.job_id == job_id)

        stmt = stmt.order_by(Candidate.created_at.desc()).limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        return items, total


class InterviewRepository(BaseRepository[Interview]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Interview)

    async def search(
        self,
        candidate_id: UUID | None = None,
        job_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[Interview], int]:
        stmt = select(Interview)
        count_stmt = select(func.count()).select_from(Interview)

        if candidate_id:
            stmt = stmt.where(Interview.candidate_id == candidate_id)
            count_stmt = count_stmt.where(Interview.candidate_id == candidate_id)
        if job_id:
            stmt = stmt.where(Interview.job_id == job_id)
            count_stmt = count_stmt.where(Interview.job_id == job_id)

        stmt = stmt.order_by(Interview.scheduled_at.desc().nullslast()).limit(limit).offset(offset)

        result = await self.db.execute(stmt)
        items = list(result.scalars().all())
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar() or 0
        return items, total
