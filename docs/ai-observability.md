# AI Observability

Production AI systems need monitoring because correctness, cost, and reliability can drift over time.

## What To Track

Quality:

- Low-confidence responses
- Hallucination reports
- User thumbs up/down
- Escalation rate
- Repeated unresolved questions
- Retrieval source coverage

Reliability:

- AI provider failures
- Vector DB failures
- CRM failures
- WhatsApp provider failures
- Retry count
- Queue backlog

Performance:

- End-to-end latency
- Retrieval latency
- AI provider latency
- Report generation time
- Campaign send time

Cost:

- Input tokens
- Output tokens
- Cost per conversation
- Cost per report
- Cost per client
- Cost by model/provider

Safety:

- Sensitive data detected
- Blocked requests
- Policy-exception escalations
- Prompt/config version used

## Minimum AI Log Record

Each AI call should record:

- Request ID
- Client ID
- Workflow type
- User role or channel
- Model/provider
- Prompt version
- Knowledge base version
- Retrieved source IDs
- Input token count
- Output token count
- Latency
- Status
- Error type if failed
- Escalated or auto-answered
- Cost estimate

## Monitoring Views

Admin view:

- Daily AI usage
- Escalation rate
- Failed jobs
- Cost trend
- Risk alerts

Support reviewer view:

- Bad answers
- Low-confidence answers
- Hallucination reports
- Missing knowledge base content

Engineering view:

- API failures
- Latency p95
- Queue backlog
- Provider rate limits
- Token usage spikes

## Alert Conditions

Trigger an operational alert when:

- AI provider failures exceed threshold
- WhatsApp sends fail repeatedly
- Queue backlog grows beyond threshold
- Escalation rate spikes suddenly
- Token cost exceeds daily budget
- Knowledge base indexing fails
- Teacher report generation fails

## Feedback Loop

Monitoring should lead to improvement:

1. Review failed or bad response.
2. Identify cause: missing content, retrieval issue, prompt issue, policy issue, model issue.
3. Update source content, prompt, rule, or model route.
4. Run regression tests on known cases.
5. Deploy with a new prompt/config version.
