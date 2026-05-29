# Production Architecture

This system should be built as an operations automation product first, not as a polished dashboard first. The web app exists to operate, monitor, and improve the automations.

## Product Goal

Reduce student support load, catch at-risk students earlier, improve teacher visibility, and make AI-assisted operations measurable.

The first production question is not "does the UI look nice?" It is:

- Did support response time decrease?
- Did counselors follow up faster?
- Did parent outreach happen reliably?
- Did teachers get useful weak-topic insights?
- Did AI reduce workload without creating risk?

## Default Architecture Assumptions

- Start as a single-client deployment.
- Keep data boundaries multi-tenant-ready so the same template can later serve multiple clients.
- Use RBAC from the beginning.
- Keep audit logs from the beginning.
- Use async jobs for outbound messages, report generation, document ingestion, and slow AI tasks.
- Use synthetic data locally and staging-safe data in client testing.
- Never send real WhatsApp/SMS/email messages from local demo mode.

## Recommended Stack

Frontend:

- Next.js for the production web app
- Tailwind CSS or a small design system
- Server-side rendering only where it helps dashboards load quickly

Backend:

- FastAPI for Python-first AI workflows
- Node.js is also viable if the team is stronger there
- REST APIs first, background jobs second, GraphQL only if complexity justifies it

Database:

- PostgreSQL for users, students, conversations, alerts, reports, audit logs, and config

Vector Database:

- Qdrant for local/dev and self-hosted friendly deployments
- Pinecone if managed vector infrastructure is preferred

Queue:

- Redis plus workers for document ingestion, report generation, outbound campaigns, and retries

Auth:

- JWT/OAuth, Clerk, Auth.js, or a client enterprise IdP depending on deployment

AI Providers:

- OpenAI for strong general reasoning and support response generation
- Google Gemini or another provider as optional fallback or cost route
- Provider adapter layer so model choice is not hard-coded

Deployment:

- Vercel for frontend
- Railway or Render for early backend deployments
- AWS later for mature production deployments, private networking, and stricter compliance needs

## Core Modules

### Support Assistant

- Handles approved FAQs, schedules, fee policy, scholarship policy, and common doubts
- Uses retrieval over approved knowledge base content
- Escalates low-confidence, sensitive, policy-exception, or unsupported questions
- Stores conversation history and resolution status

### Engagement Automation

- Evaluates inactivity, missed classes, low scores, and score decline
- Creates risk alerts
- Prepares parent messages
- Creates counselor follow-up tasks
- Tracks outcomes after follow-up

### Teacher Intelligence

- Summarizes weak topics, common doubts, at-risk students, and engagement patterns
- Generates daily evening reports
- Lets teachers inspect supporting evidence before acting

### Knowledge Base Manager

- Uploads PDFs, policies, schedules, notes, and fee documents
- Extracts text
- Chunks and embeds content
- Tracks source version and approval status
- Keeps old versions auditable

### Counselor Workspace

- Shows assigned alerts and priority
- Shows conversation history
- Allows manual intervention
- Approves or rejects outbound campaign messages
- Records follow-up outcome

### AI Monitoring Panel

- Tracks failed responses, hallucination reports, latency, token usage, API failures, escalation rates, and retrieval hit quality
- Lets admins review bad answers and improve source content or prompts

## High-Level Data Flow

1. Student asks a question or student activity data changes.
2. Backend checks tenant/client config, RBAC, and data rules.
3. Support request or engagement event is persisted.
4. Retrieval fetches approved knowledge snippets when needed.
5. AI provider generates a response or summary through a provider adapter.
6. Guardrails check confidence, sensitive topics, policy exceptions, and channel rules.
7. System either responds automatically or creates an escalation.
8. Queue handles outbound messages, report generation, retries, and provider failures.
9. Monitoring records latency, cost, tokens, retrieval metadata, and result quality.
10. Admin/teacher/counselor portals show the outcome in role-specific views.

## AI Provider Layer

Do not call AI APIs directly from business logic. Use an adapter with:

- Provider name
- Model name
- Input payload
- Output payload
- Latency
- Token usage
- Cost estimate
- Failure reason
- Retry count
- Safety classification

This allows model routing later:

- Cheaper model for simple FAQ responses
- Stronger model for teacher summaries
- Fallback model during outages
- Manual review for sensitive cases

## Retrieval Layer

The retrieval system should store:

- Source document ID
- Source type
- Version
- Approval status
- Chunk text
- Embedding ID
- Last indexed timestamp
- Owner/uploader

Only approved content should be used in production responses.

## Failure Handling

Expected failures:

- AI provider timeout
- AI provider rate limit
- Vector search unavailable
- CRM API unavailable
- WhatsApp provider failure
- Low-confidence AI answer
- Missing student record
- Missing parent contact

Fallback behavior:

- Do not guess
- Queue retryable tasks
- Escalate to human if student-facing answer cannot be trusted
- Log failure with enough context for diagnosis
- Show operational status in AI Monitoring Panel

## What Not To Build First

Avoid spending early time on:

- Fancy login screens
- Heavy animations
- Complex chart themes
- Multi-tenant billing
- Full SaaS marketing site
- Advanced customization UI

Build those after the automations are proven useful.
