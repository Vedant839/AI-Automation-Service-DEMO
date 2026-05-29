# RBAC And Audit

## Roles

Super Admin:

- Manages platform-level settings and tenants if multi-tenant mode is enabled.

Client Admin:

- Manages client configuration, users, knowledge base approvals, campaigns, reports, and monitoring.

Teacher:

- Views assigned batches, weak topics, common doubts, student risk summaries, and daily reports.

Counselor:

- Views assigned student alerts, conversation history, parent message previews, and follow-up tasks.

Knowledge Manager:

- Uploads and manages documents, schedules, policies, and approved FAQ content.

Support Reviewer:

- Reviews failed AI responses, hallucination reports, and low-confidence conversations.

## Permission Matrix

| Feature | Client Admin | Teacher | Counselor | Knowledge Manager | Support Reviewer |
| --- | --- | --- | --- | --- | --- |
| View admin dashboard | Yes | No | No | No | Limited |
| View teacher reports | Yes | Yes | Limited | No | Limited |
| View counselor queue | Yes | No | Yes | No | Limited |
| Upload knowledge docs | Yes | No | No | Yes | No |
| Approve knowledge docs | Yes | No | No | Limited | No |
| View AI monitoring | Yes | No | No | No | Yes |
| Approve campaigns | Yes | No | Limited | No | No |
| Export data | Yes | Limited | Limited | No | No |
| Change automation rules | Yes | No | No | No | No |

## Audit Log Events

Track:

- User login
- Role changes
- Knowledge document upload
- Knowledge document approval
- Prompt/config change
- Automation rule change
- AI response sent
- AI response escalated
- Parent message prepared
- Parent message approved
- Parent message sent
- Counselor task resolved
- Report generated
- Data export

Each audit event should store:

- Event ID
- Client/tenant ID
- Actor user ID or system actor
- Entity type
- Entity ID
- Action
- Before/after values when safe
- Timestamp
- Request ID
- IP/user agent when available

## Data Access Rules

- Teachers should only see assigned batches or students.
- Counselors should only see assigned queues unless admin access is granted.
- Knowledge managers should not need student-level records.
- Support reviewers should see enough context to diagnose AI quality without unnecessary sensitive data.
- Admin exports should be logged.
