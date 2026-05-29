# Personalization Guide

## Testing Mode

Use the synthetic files for local testing:

- `config/client_profile.synthetic.json`
- `data/synthetic_faqs.json`
- `data/synthetic_students.json`

These files use fictional names, providers, students, course details, CRM names, and URLs. They are safe for demos and internal testing because they do not represent real students or real client systems.

## Client Mode

When personalizing for a real client:

1. Copy `config/client_profile.template.json` to `config/client_profile.<client>.json`.
2. Replace placeholder values such as `{{CLIENT_LEGAL_NAME}}`.
3. Copy `data/synthetic_faqs.json` to a client-specific FAQ file.
4. Replace all FAQ answers with approved client content.
5. Replace `data/synthetic_students.json` with staging-safe records from the client, preferably anonymized.
6. Keep secrets in `.env` or the deployment secret manager, not in JSON files.

## Keep Synthetic Data Separate

Do not mix real student data into synthetic files. Synthetic files should remain reusable for demos, tests, and sales walkthroughs.

## Recommended Naming

- Synthetic config: `client_profile.synthetic.json`
- Client config: `client_profile.<client_slug>.json`
- Synthetic FAQ data: `synthetic_faqs.json`
- Client FAQ data: `client_faqs.<client_slug>.json`
- Synthetic student data: `synthetic_students.json`
- Client test data: `client_students.<client_slug>.json`
