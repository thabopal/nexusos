from pathlib import Path

from .audit import JsonlAuditLog
from .control_plane import ControlPlane
from .policy import PolicyEngine
from .registry import ManifestRegistry


def main() -> None:
    root = Path.cwd()
    registry = ManifestRegistry(root / "contracts/agent-manifest.schema.json")
    manifest = registry.load(root / "agents/tender-scout/agent.json")
    plane = ControlPlane(registry, PolicyEngine(), JsonlAuditLog(root / "data/audit.jsonl"))
    job = plane.create_job("tender.scan", "local-cli")
    plane.assign(job, manifest["metadata"]["id"])
    decision = plane.authorize(job, "discord.report")
    print(f"NexusOS {job.id}: discord.report -> {decision.reason}")


if __name__ == "__main__":
    main()
