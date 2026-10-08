import json
from pathlib import Path

import pytest

from nexusos.audit import JsonlAuditLog
from nexusos.control_plane import ControlPlane
from nexusos.policy import PolicyEngine
from nexusos.registry import ManifestRegistry


ROOT = Path(__file__).parents[1]


@pytest.fixture
def control_plane(tmp_path):
    registry = ManifestRegistry(ROOT / "contracts/agent-manifest.schema.json")
    registry.load(ROOT / "agents/tender-scout/agent.json")
    return ControlPlane(registry, PolicyEngine(), JsonlAuditLog(tmp_path / "audit.jsonl"))


def test_tender_scout_can_report_to_discord(control_plane):
    job = control_plane.create_job("tender.scan", "thabo")
    control_plane.assign(job, "tender-scout")
    decision = control_plane.authorize(job, "discord.report")
    assert decision.allowed is True
    assert decision.requires_approval is False


def test_default_deny_for_undeclared_capability(control_plane):
    job = control_plane.create_job("tender.scan", "thabo")
    control_plane.assign(job, "tender-scout")
    decision = control_plane.authorize(job, "github.merge")
    assert decision.allowed is False


def test_explicitly_prohibited_tender_submission(control_plane):
    job = control_plane.create_job("tender.submit", "thabo")
    control_plane.assign(job, "tender-scout")
    decision = control_plane.authorize(job, "tenders.read", "submit-tender")
    assert decision.allowed is False
    assert "prohibited" in decision.reason


def test_agent_cannot_approve_own_request(control_plane):
    job = control_plane.create_job("external.communication", "thabo")
    control_plane.assign(job, "tender-scout")
    approval = control_plane.request_approval(job, "client-or-buyer-communication", "Send clarification")
    with pytest.raises(PermissionError):
        control_plane.decide_approval(job, approval.id, "tender-scout", True)


def test_audit_log_is_jsonl(control_plane):
    job = control_plane.create_job("tender.scan", "thabo")
    control_plane.assign(job, "tender-scout")
    control_plane.authorize(job, "discord.report")
    lines = control_plane.audit.path.read_text().splitlines()
    assert len(lines) == 3
    assert [json.loads(line)["eventType"] for line in lines] == ["job.created", "job.assigned", "policy.evaluated"]
