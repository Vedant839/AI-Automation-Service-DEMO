# Deployment Guide

## Environments

- Local development
- Client staging
- Production

## Pre-Deployment

- Confirm client configuration
- Verify secrets are stored outside source control
- Confirm approved FAQs and policies
- Test chatbot handoff rules
- Test engagement triggers with synthetic or staging-safe data
- Test teacher report delivery

## Deployment Steps

1. Deploy backend service or automation workflows.
2. Configure environment variables.
3. Connect CRM/staging integrations.
4. Connect chat widget or app chat channel.
5. Connect WhatsApp provider if included.
6. Configure report schedule.
7. Run smoke tests.
8. Switch approved channels to production.

## Monitoring

- Chatbot unresolved questions
- Escalation volume
- Failed CRM calls
- Failed WhatsApp sends
- Teacher report delivery failures
- Response quality review notes

## Rollback

- Disable AI assistant channel routing.
- Revert to existing human support workflow.
- Pause engagement notifications.
- Keep teacher reports manual until issue is resolved.
