import os

import model
import psycopg2

conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
)


def get_job_by_id(job_id: str) -> model.Job:
    sql = """
        SELECT id, user_id, name, run_type, image, command, status
        FROM jobs
        WHERE id=%s;
    """
    cursor = conn.cursor()
    cursor.execute(sql, (str(job_id),))
    job: model.Job = model.Job(raw_job=cursor.fetchone())
    cursor.close()

    return job


def get_first_pending_job_by_user_id(user_id: str) -> model.Job:
    sql = """
        SELECT id, user_id, name, run_type, image, command, status
        FROM jobs
        WHERE user_id=%s AND status like %s;
    """
    cursor = conn.cursor()
    cursor.execute(
        sql,
        (
            str(user_id),
            model.JobStatus.PENDING.value,
        ),
    )
    job: model.Job = model.Job(raw_job=cursor.fetchone())
    cursor.close()

    return job


def append_job_logs(job_id: str, logs: str) -> None:
    sql = """
        UPDATE jobs
        SET logs = logs || '\n' || %s
        WHERE id=%s
    """
    cursor = conn.cursor()
    cursor.execute(
        sql,
        (
            logs,
            job_id,
        ),
    )
    conn.commit()
    cursor.close()


def get_user_by_api_key(api_key: str) -> model.User:
    sql = """
        SELECT id, username, api_key
        FROM users
        WHERE api_key like %s
    """
    cursor = conn.cursor()
    cursor.execute(sql, (api_key,))
    users = cursor.fetchall()
    cursor.close()

    return model.User(users[0])


def update_job_status(job_id: str, status: str) -> None:
    sql = """
        UPDATE jobs
        SET status = %s
        WHERE id = %s
    """
    cursor = conn.cursor()
    cursor.execute(
        sql,
        (
            status,
            job_id,
        ),
    )
    conn.commit()
    cursor.close()


def is_job_of_user(job_id: str, user_id: str) -> bool:
    print(f"is_job_of_user   job_id: {job_id}, user_id: {user_id}")
    job: model.Job = get_job_by_id(job_id=job_id)
    print(f"is_job_of_user.get_job_by_id  {job.user_id}")
    return job.user_id == user_id
