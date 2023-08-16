import json
from random import randint

import socketio

sio = socketio.AsyncServer(async_mode="asgi")
app = socketio.ASGIApp(sio)


@sio.event
def connect(sid, environ, auth) -> None:
    if auth["api_key"] != "tmp-api-key":
        raise Exception("Auth failed")
    print(f"Connected: {sid}")


@sio.event
async def logs_message(sid, data) -> None:
    print(f"Job [{data['job']}]: {data['logs']}")


@sio.event
async def job_poll(sid) -> None:
    print("Job poll")
    job_id = randint(1000, 9999)  # nosec
    await sio.emit(
        "new_job",
        json.dumps(
            {
                "job_id": job_id,
                "run_type": "DOCKER",  # HOST or DOCKER
                "command": f"""
            #!/usr/bin/env bash"
            echo "Echo from the job {job_id}"
            sleep 2
            echo "second output from the job {job_id}"
            """,
            }
        ),
    )


@sio.event
def disconnect(sid) -> None:
    print("disconnect ", sid)
