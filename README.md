# AI Automation Service Template

Reusable project template for education-platform AI automation engagements.

This repository is designed to be personalized per client while keeping the core framework reusable. The contract can reference a specific client, but client-specific names, integrations, FAQs, escalation rules, dashboards, and deployment settings should live in configuration and documentation rather than hard-coded business logic.

Local testing uses fully synthetic data for a fictional client, AsterLearn Academy. None of the synthetic names, CRM providers, students, URLs, schedules, or policies represent real systems or real people.

## Contract-Aligned Deliverables

- AI support assistant workflows for FAQs, scheduling, fees, scholarships, and student doubts
- Student engagement automation for inactivity, missed classes, low scores, score decline, parent notifications, and counselor alerts
- Teacher intelligence reporting with weak topics, frequent doubts, at-risk students, and engagement summaries
- Deployment documentation
- Admin usage instructions

## Project Structure

```text
AI Automation Service/
  contract.txt
  ARCHITECTURE.md
  README.md
  PROJECT_PLAN.md
  .env.example
  config/
    client_profile.synthetic.json
    client_profile.template.json
  data/
    synthetic_contacts.json
    synthetic_faqs.json
    synthetic_students.json
  docs/
    acceptance-checklist.md
    admin-usage-instructions.md
    ai-observability.md
    api-and-data-contracts.md
    change-request-template.md
    deployment-guide.md
    discovery-questionnaire.md
    integration-checklist.md
    personalization-guide.md
    production-roadmap.md
    privacy-risk-notes.md
    rbac-and-audit.md
    web-app-modules.md
  prompts/
    counselor_escalation.md
    support_assistant.md
    teacher_summary.md
  src/
    ai_automation_template/
      __init__.py
      chatbot.py
      config.py
      engagement.py
      models.py
      reports.py
  scripts/
    demo.py
  workflows/
    chatbot_workflow.md
    engagement_workflows.md
    teacher_report_spec.md
```

## Quick Demo

From this folder:

```powershell
python .\scripts\demo.py
```

The demo uses local synthetic data only. It does not call external AI providers, CRMs, WhatsApp APIs, or production systems.

For a client-facing real-life use demo:

```powershell
python .\scripts\client_demo.py
```

This creates `demo_outputs/client-demo.html` plus message/report previews that show what parents, counselors, and teachers would see in a real deployment.

## Tests

Run the automated checks with:

```powershell
python -m unittest discover -s tests -v
```

The tests exercise synthetic FAQ matching, sensitive-question handoff, unsupported-question handoff, engagement alerts, and teacher report generation.

## Personalization Steps

1. Use `config/client_profile.synthetic.json` and `data/synthetic_*.json` for local testing and demos.
2. Copy `config/client_profile.template.json` to a client-specific config file.
3. Replace placeholders such as `{{CLIENT_LEGAL_NAME}}`.
4. Copy `data/synthetic_faqs.json` into a client-specific FAQ file and replace every answer with approved client content.
5. Confirm integrations in `docs/integration-checklist.md`.
6. Adjust engagement thresholds in the client profile.
7. Review privacy notes and remove unnecessary sensitive data from payloads.
8. Connect the skeleton services to actual website chat, app chat, WhatsApp, CRM, and dashboard delivery channels.

## Out of Scope by Default

The base template excludes voice agents, native mobile app development, full CRM rebuilds, human support staffing, live tutoring AI, and advanced multilingual fine-tuning unless separately approved.

## Architecture Notes

Start with [ARCHITECTURE.md](</c:/Projects1/Client_Projects(Mock)/AI Automation Service/ARCHITECTURE.md>) for the production design. The roadmap, RBAC, web app modules, AI observability, and API/data contracts live under `docs/`.
