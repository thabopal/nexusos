# NexusOS Architecture

NexusOS is the control plane for NexusHub's digital workforce. It accepts goals/events, creates jobs, delegates bounded work, records evidence and escalates consequential decisions.

## Components

- **Orchestrator:** decomposes goals, routes jobs and tracks state.
- **Agent Registry:** versioned manifests for identity, runtime, capabilities and authority.
- **Capability Gateway:** default-deny policy boundary between agents and tools.
- **Job Store:** queued -> planned -> running -> awaiting_approval -> succeeded/failed/cancelled.
- **Approval Service:** tamper-evident human gates for consequential actions.
- **Audit Log:** append-only events with job, agent and correlation identity.
- **Memory:** job-local, agent-operational and curated organisational context. Secrets excluded.

## Autonomy

T0 Observe: read/analyse/report. T1 Prepare: drafts/branches/proposals. T2 Execute bounded: reversible pre-approved actions. T3 Human gate: production, external client communication, money, credentials/privileges and destructive actions. An agent cannot approve its own T3 request.

## Runtime abstraction

Hermes is the first supported runtime adapter, not the architecture boundary. NexusOS owns identity, policy, jobs, approvals and audit so runtimes/models remain replaceable.

## Delivery pattern

Goal/issue -> Orchestrator -> implementation branch -> Developer -> CI -> independent Reviewer -> Security -> approval packet -> human approval -> Deployment -> verification.
