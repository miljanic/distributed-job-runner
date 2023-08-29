import logging
import os

import model
import repository
import socketio

logger = logging.getLogger("uvicorn")
logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG"))

sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(sio)

connections: dict[str, str] = {}


@sio.event
def connect(sid, environ, auth) -> None:
    try:
        user = repository.get_user_by_api_key(api_key=auth["api_key"])
        connections[sid] = user.id
    except Exception:
        raise Exception("Auth failed")


@sio.event
async def logs_message(sid, data) -> None:
    print("logs_message")
    job_id: str = data["job"]
    logs: str = data["logs"]

    try:
        print("logs_message.repository.is_job_of_user")
        repository.is_job_of_user(job_id=job_id, user_id=connections[sid])
        print("logs_message.repository.append_job_logs")
        repository.append_job_logs(job_id=job_id, logs=logs)
    except Exception:
        logger.info("Unauthorized to update the job!")

    print("logs_message.DONE")


@sio.event
async def job_finished(sid, data) -> None:
    job_id: str = data["job_id"]
    status: model.JobStatus = model.JobStatus[data["status"]]
    # return_code: str = data["return_code"]
    try:
        repository.is_job_of_user(job_id=job_id, user_id=connections[sid])
        repository.update_job_status(job_id=job_id, status=status.value)
    except Exception:
        logger.info("Unauthorized to update the job!")


@sio.event
async def job_poll(sid) -> None:
    logger.debug("Job poll")
    user_id: str = connections[sid]

    try:
        job: model.Job = repository.get_first_pending_job_by_user_id(user_id)
        await sio.emit(
            event="new_job",
            data=job.toJSON(),
            to=sid,
        )
        repository.update_job_status(
            job_id=job.id, status=model.JobStatus.RUNNING.value
        )
    except Exception:
        logger.debug(f"No pending jobs for {user_id}")


@sio.event
def disconnect(sid) -> None:
    logger.debug(f"disconnect {sid}")
    del connections[sid]
