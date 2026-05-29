# Privacy And Risk Notes

## Contract Constraints

The consultant should access only data necessary for project functionality. Sensitive information such as payment records, government IDs, passwords, and banking information should not be shared unless explicitly required.

## Default Data-Minimization Rules

- Send only the current query and approved context to AI providers.
- Prefer student IDs over names in reports.
- Remove payment, government ID, password, and banking fields from automation payloads.
- Disable unnecessary logging where supported by vendors.
- Keep staging data anonymized where possible.

## Risk Register

| Risk | Mitigation |
| --- | --- |
| AI hallucination | Use approved content retrieval, confidence thresholds, and counselor escalation |
| Sensitive data exposure | Redact restricted fields before AI calls and logs |
| Incorrect escalation | Test trigger rules with historical examples |
| Third-party API outage | Add fallback handoff and retry behavior |
| Unsupported policy question | Route to counselor instead of guessing |

## Client Responsibility Reminder

The client remains responsible for data legality, student consent compliance, and internal policy approvals.
