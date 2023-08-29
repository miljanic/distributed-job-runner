from typing import List

from djb_api.domain.auth.dto import User
from djb_api.domain.jobs.actions import JobCreateAction, JobGetAction, JobsListAction
from djb_api.domain.jobs.dto import Job, JobCreate
from djb_api.util.auth import get_current_user
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/", response_model=List[Job], tags=["jobs"])
async def jobs_list(
    authed_user: User = Depends(get_current_user),
    jobs_list_action: JobsListAction = Depends(JobsListAction),
):
    return [
        Job.parse_obj(job) for job in await jobs_list_action(user_id=authed_user.id)
    ]


@router.post("/", response_model=Job, tags=["jobs"])
async def jobs_create(
    form_data: JobCreate,
    authed_user: User = Depends(get_current_user),
    job_create_action: JobCreateAction = Depends(JobCreateAction),
):
    print("START")
    job = await job_create_action(user_id=authed_user.id, job=form_data)
    print("END 1")
    print(job)
    return job


@router.get("/{id}", response_model=Job, tags=["jobs"])
async def jobs_get(
    id: str,
    authed_user: User = Depends(get_current_user),
    job_get_action: JobGetAction = Depends(JobGetAction),
):
    return await job_get_action(user_id=authed_user.id, id=id)
