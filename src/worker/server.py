# connect to the server
# send dummy data (fake logs)
# handle disconnection

import asyncio
import os

import socketio

MASTER_URL: str = os.getenv("MASTER_URL", "http://localhost:8080")
sio = socketio.AsyncClient()

jobs = []


@sio.event
async def connect():
    print("Connected to the Master")


@sio.event
async def disconnect():
    print("Disconnected from the Master")


@sio.event
async def new_job(data):
    print(f"New job available: {data}")
    jobs.append(data)


async def do_job(job: str) -> None:
    print(f"Doing job: {job}")
    await asyncio.sleep(1)
    jobs.remove(job)
    print(f"Done job: {job}")
    await sio.emit("logs_message", {"job": job, "logs": "Some fake stuff"})


async def poll_jobs() -> None:
    for _ in range(1, 3):
        print("Polling for jobs...")
        await sio.emit("job_poll")
        await asyncio.sleep(5)


async def job_worker_initializer() -> None:
    while True:
        print("Initializing workers...")
        for job in jobs:
            # TODO: threading...
            await do_job(job)

        await asyncio.sleep(1)


async def main():
    await sio.connect(url=MASTER_URL, auth={"api_key": "tmp-api-key"})
    await asyncio.gather(poll_jobs(), job_worker_initializer())

    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
