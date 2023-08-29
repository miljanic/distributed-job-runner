import json
from enum import Enum


class JobStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


class Job:
    def __init__(self, raw_job: tuple):
        self.id: str = raw_job[0]
        self.user_id: str = raw_job[1]
        self.name: str = raw_job[2]
        self.run_type: str = raw_job[3]
        self.image: str = raw_job[4]
        self.command: str = raw_job[5]
        self.status: JobStatus = JobStatus[raw_job[6]]

    def toJSON(self):
        return json.dumps(
            {
                "id": self.id,
                "user_id": self.user_id,
                "name": self.name,
                "run_type": self.run_type,
                "image": self.image,
                "command": self.command,
                "status": self.status.value,
            }
        )


class User:
    def __init__(self, raw_user: tuple):
        self.id: str = raw_user[0]
        self.username: str = raw_user[1]
        self.api_key: str = raw_user[2]
