from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class JobStatus(StrEnum):
    QUEUED = "queued"
    PLANNED = "planned"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Job:
    type: str
    requested_by: str
    input: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: f"job_{uuid4().hex}")
    correlation_id: str = field(default_factory=lambda: f"cor_{uuid4().hex}")
    status: JobStatus = JobStatus.QUEUED
    assigned_agent: str | None = None
    created_at: str = field(default_factory=utc_now)
    artifacts: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    requires_approval: bool
    reason: str


@dataclass
class ApprovalRequest:
    job_id: str
    requested_by_agent: str
    action: str
    risk_tier: str
    reason: str
    id: str = field(default_factory=lambda: f"apr_{uuid4().hex}")
    status: str = "pending"
    approved_by: str | None = None
    created_at: str = field(default_factory=utc_now)
