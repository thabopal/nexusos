import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


class ManifestRegistry:
    def __init__(self, schema_path: Path) -> None:
        self.schema = json.loads(schema_path.read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(self.schema)
        self._agents: dict[str, dict[str, Any]] = {}

    def load(self, manifest_path: Path) -> dict[str, Any]:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.validator.validate(manifest)
        agent_id = manifest["metadata"]["id"]
        if agent_id in self._agents:
            raise ValueError(f"Agent already registered: {agent_id}")
        self._agents[agent_id] = manifest
        return manifest

    def get(self, agent_id: str) -> dict[str, Any]:
        try:
            return self._agents[agent_id]
        except KeyError as exc:
            raise KeyError(f"Unknown agent: {agent_id}") from exc
