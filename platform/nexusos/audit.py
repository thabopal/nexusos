import json
from pathlib import Path
from typing import Any

from .models import utc_now


class JsonlAuditLog:
    """Simple append-only JSONL audit sink for the Phase 1 slice."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event_type: str, *, job_id: str, agent_id: str | None, correlation_id: str, data: dict[str, Any] | None = None) -> None:
        event = {
            "timestamp": utc_now(),
            "eventType": event_type,
            "jobId": job_id,
            "agentId": agent_id,
            "correlationId": correlation_id,
            "data": data or {},
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, separators=(",", ":")) + "\n")
