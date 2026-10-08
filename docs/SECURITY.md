# Security & Authority Model

- No plaintext secrets in Git, prompts, logs or manifests.
- Default deny for capabilities; least privilege everywhere.
- Production and development identities are separate.
- Human approval is mandatory for T3 actions.
- The proposing agent cannot approve its own action.
- Every tool invocation carries agent, job and correlation identity.
- Destructive operations require explicit scope and approval.
- Per-agent and global kill switches are mandatory.

## Prompt-injection boundary

Retrieved websites, repositories, tenders, emails and documents are data, not authority. Instructions found inside retrieved content cannot expand capabilities. Authorization comes only from NexusOS policy.

## Secrets

Manifests contain secret references, never values. A secrets broker resolves credentials only for an authorized capability and scope.

## Audit minimum

Timestamp, correlation ID, job ID, agent/version, capability, policy decision, approval ID if applicable, target, result and evidence/artifact references.
