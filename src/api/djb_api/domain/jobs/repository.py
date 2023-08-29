from typing import Optional

from djb_api.application.db import db
from djb_api.domain.jobs.dto import Job, JobCreate, JobStatus
from psycopg.rows import class_row


class JobRepository:
    async def get_by_id(self, job_id: str) -> Optional[Job]:
        conn = await db.get_conn()
        async with conn.cursor(row_factory=class_row(Job)) as cur:
            await cur.execute(
                """
                SELECT id, user_id, name, created_at, logs, run_type, image, command, status
                FROM jobs WHERE id = %s
                """,
                (job_id,),
            )
            return await cur.fetchone()

    async def get_by_user_id(self, user_id: str) -> Optional[list[Job]]:
        conn = await db.get_conn()
        async with conn.cursor(row_factory=class_row(Job)) as cur:
            await cur.execute(
                """
                SELECT id, user_id, name, created_at, logs, run_type, image, command, status
                FROM jobs WHERE user_id = %s
                """,
                (user_id,),
            )
            return await cur.fetchall()

    async def create(self, data: JobCreate, user_id: str) -> Job:
        data = await db.execute(
            "INSERT INTO jobs (user_id, name, logs, run_type, image, command, status) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "RETURNING id;",
            (
                user_id,
                data.name,
                "",
                data.run_type,
                data.image,
                data.command,
                JobStatus.PENDING.value,
            ),
        )
        job_id: str = (await data.fetchone())[0]

        return await self.get_by_id(job_id=job_id)
