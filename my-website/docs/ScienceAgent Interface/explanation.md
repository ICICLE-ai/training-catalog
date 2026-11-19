---
tags:
  - Foundation-AI
  - Software
  - CI4AI
title: "ScienceAgent Interface: Explanation"
sidebar_label: "Explanation"
pagination_label: "Explanation"
description: "Explanation for ScienceAgent Interface. Science Agent helps researchers carry out tasks using ICICLE services and resources through natural language."
---
# Explanation

The HTTP API specification is served at /openapi.json and saved in openapi.json
for release submission. Regenerate the file with
`uv run python -m science_agent_backend.openapi --output openapi.json` after API
changes. This exports documentation without connecting to PostgreSQL or the pod.
WebSocket behavior is documented separately in the x-websockets extension.

## User context, not a new agent per account

The backend verifies the `X-Tapis-Token` cookie and uses the validated identity to scope conversation, attachment, and S3 profile access. It sends the user's token in private request-specific context so the agent can call Smart Labeler and Tapis on that user's behalf.

The remote agent is shared. Each request receives its own files, recent conversation messages, selected S3 credentials, and workflow observations. This is application-level context separation, not a dedicated pod or an operating-system security boundary for every user.

## Responsibility boundaries

The frontend handles interaction, the backend handles authentication and persistence, and the agent pod performs service operations. PostgreSQL stores conversations, uploaded file bytes, S3 profiles, and recorded workflow observations. ArrayMorph and Smart Labeler work runs on the agent side rather than inside the backend container.

Migration history is maintained automatically by the backend. Uploaded files and credentials must be protected through restricted DB access, secure backups, and HTTPS. S3 secrets are currently stored without application-level encryption; they are not returned in public profile responses.

## Current scope

The integrated labeling flow accepts exactly one image. It reports observed submission and status information rather than treating submission as completed labeling.

The shared-agent guard currently serializes requests within one backend instance; multi-instance coordination is not implemented. The S3 browser API and original coding-agent execution commands have not been migrated. Hub cookie delivery, service permissions, and external job readiness remain deployment prerequisites.
