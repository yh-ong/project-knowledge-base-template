---
title: Architecture Overview
owner: "@tech-lead"
status: active
last_reviewed: YYYY-MM-DD
---

# Architecture Overview

> Describe the system as it **is**, not as it was planned. Planned changes go in specs / ADRs.

## 1. System context
<!-- Who/what talks to the system. A Mermaid diagram beats paragraphs. Replace this example. -->
```mermaid
flowchart LR
  user[User] --> web[Web app]
  web --> api[API]
  api --> db[(Database)]
  api --> ext[External service]
```

## 2. Components
| Component | Responsibility | Tech | Repo path | Owner |
|---|---|---|---|---|
| | | | | |

## 3. Key flows
<!-- The 2–5 flows that matter most (e.g. sign-up, checkout, nightly sync). One Mermaid sequence diagram each, or numbered steps for simple ones. Replace this example. -->

### Flow: <name>
```mermaid
sequenceDiagram
  actor User
  participant Web as Web app
  participant API
  participant DB as Database
  User->>Web: submits form
  Web->>API: POST /example
  API->>DB: write
  DB-->>API: ok
  API-->>Web: 201 Created
  Web-->>User: confirmation
```

## 4. Data
| Store | What lives there | Source of truth for | Retention | PII? |
|---|---|---|---|---|
| | | | | |

Core entities and relationships: <!-- link to the schema file; add a small Mermaid `erDiagram` of the core entities only if it helps -->

**API contracts:** the authoritative machine-readable definitions (OpenAPI / protobuf / event schemas) live at `…`. Link to them; don't copy endpoint lists here.

## 5. Integrations
| System | Direction | Protocol | Auth | Failure behaviour | Owner / contact |
|---|---|---|---|---|---|
| | in / out | REST / queue / … | | retries? degrade? | |

## 6. Cross-cutting concerns
- **AuthN / AuthZ:**
- **Config & secrets:** (see `06-operations/environments.md`)
- **Logging / tracing / metrics:**
- **Error handling convention:**
- **Background jobs / scheduling:**

## 7. Quality attributes & limits
<!-- Known limits: max throughput, largest tenant, single points of failure. -->

## 8. Key decisions
| ADR | Decision | Status |
|---|---|---|
| `ADR-0001` | | accepted |

## 9. Known tech debt
| Item | Impact | Plan / ticket |
|---|---|---|
| | | |
