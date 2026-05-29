# API And Data Contracts

This document defines the production entities and API boundaries. It is intentionally framework-neutral.

## Core Entities

Client:

- id
- name
- timezone
- status
- config_version

User:

- id
- client_id
- name
- email
- role
- status

Student:

- id
- client_id
- external_student_id
- display_name
- batch_id
- assigned_counselor_id
- status

Conversation:

- id
- client_id
- student_id
- channel
- status
- started_at
- last_message_at
- escalated_at

Message:

- id
- conversation_id
- sender_type
- content
- ai_generated
- source_ids
- created_at

EngagementAlert:

- id
- client_id
- student_id
- alert_type
- severity
- status
- reason
- created_at
- resolved_at

CounselorTask:

- id
- client_id
- student_id
- counselor_id
- alert_ids
- priority
- status
- next_action
- outcome

KnowledgeDocument:

- id
- client_id
- title
- source_type
- approval_status
- version
- uploaded_by
- indexed_at

AIRequestLog:

- id
- client_id
- workflow_type
- provider
- model
- prompt_version
- status
- latency_ms
- input_tokens
- output_tokens
- cost_estimate
- escalated
- error_type

AuditLog:

- id
- client_id
- actor_id
- action
- entity_type
- entity_id
- timestamp

## API Boundaries

Support:

- `POST /support/conversations`
- `POST /support/conversations/{id}/messages`
- `POST /support/conversations/{id}/escalate`
- `GET /support/conversations/{id}`

Engagement:

- `POST /engagement/evaluate`
- `GET /engagement/alerts`
- `PATCH /engagement/alerts/{id}`

Counselor:

- `GET /counselor/tasks`
- `PATCH /counselor/tasks/{id}`
- `POST /counselor/tasks/{id}/notes`

Teacher:

- `GET /teacher/reports/daily`
- `GET /teacher/batches/{id}/weak-topics`
- `GET /teacher/batches/{id}/flagged-students`

Knowledge Base:

- `POST /knowledge/documents`
- `GET /knowledge/documents`
- `PATCH /knowledge/documents/{id}/approval`
- `POST /knowledge/documents/{id}/reindex`

Monitoring:

- `GET /monitoring/ai-requests`
- `GET /monitoring/failures`
- `GET /monitoring/costs`
- `POST /monitoring/hallucination-reports`

Campaigns:

- `POST /campaigns`
- `POST /campaigns/{id}/approve`
- `POST /campaigns/{id}/send`
- `GET /campaigns/{id}/delivery`

## Async Jobs

Use background workers for:

- Knowledge document parsing
- Embedding generation
- Daily teacher report generation
- Engagement evaluation batches
- WhatsApp/email campaign sends
- Retryable provider failures
- Cost aggregation

## Rate Limiting

Rate limit by:

- Client
- User
- Channel
- AI provider
- Outbound message provider

Student-facing channels should fail closed to human handoff when limits are exceeded.
