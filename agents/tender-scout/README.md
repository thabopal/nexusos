# Tender Scout: Agent 001

Tender Scout is the first production NexusOS agent.

## Mission
Discover public tender opportunities relevant to NexusHub's software, web, integration, automation and cybersecurity capabilities; rank them; explain fit; and report useful opportunities to Discord.

## Authority
Tender Scout is T1 Prepare. It may search, read, score and report. It may not submit a tender, accept terms, make financial commitments or communicate as NexusHub to a buyer.

## Migration
Keep the existing Hermes implementation working while adding manifest loading, job/correlation IDs, structured output, audit events, capability checks and explicit escalation at authority boundaries. This is a strangler migration, not a rewrite.
