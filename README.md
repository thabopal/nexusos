# NexusOS

**The AI-native operating system for NexusHub Solutions.**

NexusOS coordinates specialist agents that discover work, build software, review changes, monitor systems, inspect security, and prepare business actions while keeping consequential authority with a human operator.

> Maximum useful leverage with accountable control.

## Phase 0

This repository is the canonical home for NexusOS architecture, contracts, policies, agent manifests, and platform code.

### Initial workforce

- **Tender Scout** — Agent 001; discovers and ranks opportunities relevant to NexusHub.
- **Orchestrator** — decomposes goals into bounded jobs and routes them to specialist agents.
- Planned: Developer, Reviewer, Security, Ops, Business and Executive agents.

## Design principles

1. Least privilege by default.
2. Agents operate inside explicit capability boundaries.
3. Builders do not approve their own work.
4. Production, money, client communication, credentials and destructive actions require stronger approval.
5. Every consequential action is attributable and auditable.
6. Models and agent runtimes are replaceable components.
7. Secrets never live in prompts, manifests or source control.

## Repository map

```
agents/        Agent manifests and role definitions
contracts/     Shared JSON Schemas and platform contracts
docs/          Architecture, security, ADRs and operating guidance
platform/      Orchestrator and shared-service implementation
tests/         Contract and policy tests
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/ROADMAP.md](docs/ROADMAP.md).

## Status

**Phase 0 — Foundation.** Tender Scout is the first production agent to be brought under the common NexusOS contract.
