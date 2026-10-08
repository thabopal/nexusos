from typing import Any

from .models import PolicyDecision


class PolicyEngine:
    """Default-deny authorization against an agent manifest."""

    def evaluate(self, manifest: dict[str, Any], capability: str, action: str | None = None) -> PolicyDecision:
        spec = manifest["spec"]

        if action and action in spec.get("prohibitedActions", []):
            return PolicyDecision(False, False, f"Action is explicitly prohibited: {action}")

        if capability not in spec.get("capabilities", []):
            return PolicyDecision(False, False, f"Capability not granted: {capability}")

        approval_actions = spec.get("requiresHumanApprovalFor", [])
        if action and action in approval_actions:
            return PolicyDecision(False, True, f"Human approval required: {action}")

        if spec["autonomyTier"] == "T3":
            return PolicyDecision(False, True, "T3 agent action requires human approval")

        return PolicyDecision(True, False, "Allowed by manifest policy")
