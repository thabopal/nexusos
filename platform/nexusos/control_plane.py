from .audit import JsonlAuditLog
from .models import ApprovalRequest, Job, JobStatus, PolicyDecision
from .policy import PolicyEngine
from .registry import ManifestRegistry


class ControlPlane:
    def __init__(self, registry: ManifestRegistry, policy: PolicyEngine, audit: JsonlAuditLog) -> None:
        self.registry = registry
        self.policy = policy
        self.audit = audit
        self.jobs: dict[str, Job] = {}
        self.approvals: dict[str, ApprovalRequest] = {}

    def create_job(self, job_type: str, requested_by: str, input: dict | None = None) -> Job:
        job = Job(type=job_type, requested_by=requested_by, input=input or {})
        self.jobs[job.id] = job
        self.audit.append("job.created", job_id=job.id, agent_id=None, correlation_id=job.correlation_id, data={"type": job.type})
        return job

    def assign(self, job: Job, agent_id: str) -> None:
        self.registry.get(agent_id)
        job.assigned_agent = agent_id
        job.status = JobStatus.PLANNED
        self.audit.append("job.assigned", job_id=job.id, agent_id=agent_id, correlation_id=job.correlation_id)

    def authorize(self, job: Job, capability: str, action: str | None = None) -> PolicyDecision:
        if not job.assigned_agent:
            raise ValueError("Job has no assigned agent")
        manifest = self.registry.get(job.assigned_agent)
        decision = self.policy.evaluate(manifest, capability, action)
        self.audit.append("policy.evaluated", job_id=job.id, agent_id=job.assigned_agent, correlation_id=job.correlation_id, data={"capability": capability, "action": action, "allowed": decision.allowed, "requiresApproval": decision.requires_approval, "reason": decision.reason})
        return decision

    def request_approval(self, job: Job, action: str, reason: str, risk_tier: str = "T3") -> ApprovalRequest:
        if not job.assigned_agent:
            raise ValueError("Job has no assigned agent")
        approval = ApprovalRequest(job_id=job.id, requested_by_agent=job.assigned_agent, action=action, risk_tier=risk_tier, reason=reason)
        self.approvals[approval.id] = approval
        job.status = JobStatus.AWAITING_APPROVAL
        self.audit.append("approval.requested", job_id=job.id, agent_id=job.assigned_agent, correlation_id=job.correlation_id, data={"approvalId": approval.id, "action": action, "riskTier": risk_tier})
        return approval

    def decide_approval(self, job: Job, approval_id: str, approver: str, approved: bool) -> ApprovalRequest:
        approval = self.approvals[approval_id]
        if approver == approval.requested_by_agent:
            raise PermissionError("An agent cannot approve its own request")
        approval.status = "approved" if approved else "rejected"
        approval.approved_by = approver
        job.status = JobStatus.PLANNED if approved else JobStatus.CANCELLED
        self.audit.append("approval.decided", job_id=job.id, agent_id=job.assigned_agent, correlation_id=job.correlation_id, data={"approvalId": approval.id, "approved": approved, "approver": approver})
        return approval
