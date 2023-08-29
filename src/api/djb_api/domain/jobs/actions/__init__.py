from djb_api.domain.jobs.dto import JobCreate
from djb_api.domain.jobs.exceptions import Unauthorized
from djb_api.domain.jobs.repository import JobRepository
from fastapi import Depends


class JobCreateAction:
    def __init__(self, job_repository: JobRepository = Depends(JobRepository)):
        self.job_repository = job_repository

    async def __call__(self, job: JobCreate, user_id: str):
        return await self.job_repository.create(data=job, user_id=user_id)


class JobsListAction:
    def __init__(self, job_repository: JobRepository = Depends(JobRepository)):
        self.job_repository = job_repository

    async def __call__(self, user_id: str):
        return await self.job_repository.get_by_user_id(user_id=user_id)


class JobGetAction:
    def __init__(self, job_repository: JobRepository = Depends(JobRepository)):
        self.job_repository = job_repository

    async def __call__(self, user_id: str, id: str):
        job = await self.job_repository.get_by_id(job_id=id)
        if str(job.user_id) != str(user_id):
            raise Unauthorized

        return job
