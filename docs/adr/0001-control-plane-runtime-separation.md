# ADR 0001: Separate control plane from agent runtimes

Status: Accepted

## Decision
NexusOS owns identity, jobs, policy, approvals, audit and capability access. Runtime adapters execute bounded agent loops. Hermes is the first supported adapter.

## Why
The platform must survive changes in models and frameworks. Authority cannot be hidden inside runtime prompts.

## Consequence
Agents can move between runtimes without redefining permissions, at the cost of a small adapter layer.
