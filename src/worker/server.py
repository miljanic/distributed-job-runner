import asyncio
import fcntl
import os
import stat
import subprocess  # nosec
import time
from concurrent.futures import Future, ThreadPoolExecutor

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


# async def do_job(job: str) -> None:
#     print(f"Doing job: {job}")
#     await asyncio.sleep(1)
#     jobs.remove(job)
#     print(f"Done job: {job}")
#     await sio.emit("logs_message", {"job": job, "logs": "Some fake stuff"})


async def poll_jobs() -> None:
    for _ in range(1, 2):
        print("Polling for jobs...")
        await sio.emit("job_poll")
        await asyncio.sleep(5)


def work(job_id: str) -> None:
    def __non_block_read(output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except Exception:
            return ""

    async def __execute() -> None:
        # TODO run new docker container or subprocess

        with open("/tmp/script.sh", mode="w") as script:  # nosec
            # TODO read script from job config
            script.writelines(
                "%s\n" % line
                for line in [
                    "#!/usr/bin/env bash",
                    "",
                    f'echo "Job - {job_id} internal logging"',
                    "ls",
                    "sleep 15",
                    "ls -lah",
                    "pwd",
                ]
            )
            script_path = script.name

        current_permissions = stat.S_IMODE(os.stat(script_path).st_mode)
        os.chmod(script_path, current_permissions | stat.S_IXUSR | stat.S_IXGRP)
        print(f"Script prepared, {script_path}")

        process = subprocess.Popen(  # nosec
            f"bash {script_path}",
            shell=True,
            text=True,
            encoding="UTF-8",
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        print("Subprocess started")
        while True:
            process_output = __non_block_read(process.stdout)
            if process_output != "":
                print(f"OUTPUT: [{job_id}] - {process_output}", flush=True)
                await sio.emit("logs_message", {"job": job_id, "logs": process_output})
            if process.poll() is not None:
                await sio.emit(
                    "job_finished", {"job": job_id, "return_code": process.returncode}
                )
                print(f"RETURN CODE: {process.returncode}")
                break

            time.sleep(1)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(__execute())


def finished_callback(job_id: str) -> callable:
    def callback(fn) -> None:
        # TODO should be removed from the futures dict also
        print(f"JOBS: {jobs}")
        print(f"JOB_ID: {job_id}")
        jobs.remove(job_id)
        print(f"Job {job_id} done, or failed.")

    return callback


async def job_worker_initializer() -> None:
    pool = ThreadPoolExecutor(max_workers=2)

    futures: dict[str, Future] = {}

    while True:
        new_jobs = {
            job_id: pool.submit(work, job_id)
            for job_id in jobs
            if job_id not in futures
        }
        print(f"NEW {new_jobs}")
        futures.update(new_jobs)
        for job_id, future in new_jobs.items():
            future.add_done_callback(finished_callback(job_id=job_id))

        await asyncio.sleep(3)


async def main():
    await sio.connect(url=MASTER_URL, auth={"api_key": "tmp-api-key"})
    await asyncio.gather(poll_jobs(), job_worker_initializer())

    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
