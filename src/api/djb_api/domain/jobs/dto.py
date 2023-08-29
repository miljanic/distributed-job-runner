from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel


class JobStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAIL = "FAIL"
    SUCCESS = "SUCCESS"


class Job(BaseModel):
    name: str
    run_type: str
    status: str
    id: str
    user_id: str
    created_at: Any
    logs: str
    image: Optional[str]
    command: Optional[str]


class JobCreate(BaseModel):
    name: str
    run_type: str
    command: Optional[str]
    image: Optional[str]
