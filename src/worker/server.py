import asyncio
import fcntl
import json
import os
import stat
import subprocess  # nosec
import time
from abc import ABCMeta, abstractmethod
from concurrent.futures import Future, ThreadPoolExecutor
from threading import Thread

import docker
import socketio

MASTER_URL: str = os.getenv("MASTER_URL", "http://localhost:8080")
sio = socketio.AsyncClient()


class Job(metaclass=ABCMeta):
    def __init__(self, job_data: dict):
        self.job_data = job_data
        self.job_id = job_data["job_id"]

    @abstractmethod
    def stream_logs(self):
        pass

    @abstractmethod
    def is_finished(self):
        pass

    @abstractmethod
    def return_code(self):
        pass

    @abstractmethod
    def run(self):
        pass


class HostJob(Job):
    def __init__(self, job_data: dict):
        super().__init__(job_data)
        self.__checking_thread = None
        self.__return_code = None
        self.__is_finished = False
        self.__process = None

    @staticmethod
    def __non_block_read(output):
        fd = output.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)
        try:
            return output.read()
        except Exception:
            return ""

    def stream_logs(self):
        return self.__non_block_read(self.__process.stdout)

    def is_finished(self):
        return self.__is_finished

    def return_code(self):
        return self.__return_code

    def __check_process(self):
        while True:
            if self.__process.poll() is not None:
                self.__is_finished = True
                self.__return_code = self.__process.returncode
                break
            time.sleep(1)

    def run(self):
        with open(f"/tmp/script-{self.job_id}.sh", mode="w") as script:  # nosec
            script.writelines(
                "%s\n" % line for line in self.job_data["command"].splitlines()
            )
            script_path = script.name

        current_permissions = stat.S_IMODE(os.stat(script_path).st_mode)
        os.chmod(script_path, current_permissions | stat.S_IXUSR | stat.S_IXGRP)
        print(f"Script prepared, {script_path}")

        self.__process = subprocess.Popen(  # nosec
            f"bash {script_path}",
            shell=True,
            text=True,
            encoding="UTF-8",
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )
        print("Subprocess started")

        self.__checking_thread = Thread(target=self.__check_process)
        self.__checking_thread.start()


class DockerJob(Job):
    def __init__(self, job_data: dict):
        super().__init__(job_data)
        self.__logs_streamed = False
        self.__logs_thread = None
        self.__saved_logs = ""
        self.__container = None

    def stream_logs(self):
        output = self.__saved_logs
        self.__saved_logs = ""
        return output

    def __is_run_finished(self):
        self.__container.reload()
        return self.__container.status == "exited"

    def is_finished(self):
        return self.__is_run_finished() and self.__logs_streamed

    def return_code(self):
        # TODO fetch return code
        return 123

    def __save_logs(self):
        for line in self.__container.logs(timestamps=True, stream=True):
            self.__saved_logs = f"{self.__saved_logs}\n{line.decode('utf-8')}".strip()
            if self.__is_run_finished():
                self.__logs_streamed = True

    def run(self):
        client = docker.from_env()
        # TODO run image from job config
        self.__container = client.containers.run(
            "alpine:latest",
            command="sh -c 'echo FIRST && echo SECOND && sleep 5 && echo THIRD'",
            detach=True,
        )

        self.__logs_thread = Thread(target=self.__save_logs)
        self.__logs_thread.start()


class InvalidJobData(Exception):
    pass


class JobFactory:
    @staticmethod
    def make_job(job_data: dict):
        if job_data["run_type"] == "HOST":
            return HostJob(job_data=job_data)
        elif job_data["run_type"] == "DOCKER":
            return DockerJob(job_data=job_data)
        else:
            raise InvalidJobData()


jobs: list[Job] = []


@sio.event
async def connect():
    print("Connected to the Master")


@sio.event
async def disconnect():
    print("Disconnected from the Master")


@sio.event
async def new_job(data):
    job_data = json.loads(data)
    job: Job = JobFactory.make_job(job_data=job_data)
    print(f"New job available: {job.job_id}")
    jobs.append(job)


async def poll_jobs() -> None:
    for _ in range(1, 2):
        print("Polling for jobs...")
        await sio.emit("job_poll")
        await asyncio.sleep(5)


def work(job: Job) -> None:
    async def __execute() -> None:
        # TODO run new docker container or subprocess
        job.run()

        while True:
            process_output = job.stream_logs()

            print("work.while.process_output - ", process_output)

            if process_output != "":
                await sio.emit(
                    "logs_message", {"job": job.job_id, "logs": process_output}
                )

            if job.is_finished():
                return_code = job.return_code()
                await sio.emit(
                    "job_finished", {"job": job.job_id, "return_code": return_code}
                )
                break

            time.sleep(1)

    loop = asyncio.new_event_loop()
    loop.run_until_complete(__execute())


def finished_callback(job_id: str) -> callable:
    def callback(fn) -> None:
        # TODO should be removed from the futures dict also
        print(f"JOBS: {jobs}")
        print(f"JOB_ID: {job_id}")

        index = next((i for i, job in enumerate(jobs) if job.job_id == job_id), -1)
        del jobs[index]
        print(f"Job {job_id} done, or failed.")

    return callback


async def job_worker_initializer() -> None:
    pool = ThreadPoolExecutor(max_workers=2)

    futures: dict[str, Future] = {}

    while True:
        new_jobs = {
            job.job_id: pool.submit(work, job)
            for job in jobs
            if job.job_id not in futures
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
