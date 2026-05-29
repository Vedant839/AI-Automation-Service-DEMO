from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OUTPUT_DIR = ROOT / "demo_outputs"
sys.path.insert(0, str(SRC))

from ai_automation_template.config import get_nested, load_json
from ai_automation_template.engagement import build_students, evaluate_all_students
from ai_automation_template.messaging import build_counselor_queue, build_parent_whatsapp_messages
from ai_automation_template.reports import summarize_teacher_intelligence


def main() -> None:
    config = load_json(ROOT / "config" / "client_profile.synthetic.json")
    students = build_students(load_json(ROOT / "data" / "synthetic_students.json"))
    contacts = load_json(ROOT / "data" / "synthetic_contacts.json")
    rules = get_nested(config, "engagement_rules", {})
    client_name = get_nested(config, "client.name", "Synthetic Academy")

    alerts = evaluate_all_students(students, rules)
    whatsapp_messages = build_parent_whatsapp_messages(alerts, students, contacts, client_name)
    counselor_queue = build_counselor_queue(alerts, students, contacts)
    teacher_report = summarize_teacher_intelligence(students, alerts)

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "whatsapp-message-preview.md").write_text(
        render_whatsapp_markdown(whatsapp_messages),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "counselor-action-queue.md").write_text(
        render_counselor_markdown(counselor_queue),
        encoding="utf-8",
    )
    (OUTPUT_DIR / "teacher-daily-report.md").write_text(
        teacher_report,
        encoding="utf-8",
    )
    (OUTPUT_DIR / "client-demo.html").write_text(
        render_html(client_name, alerts, whatsapp_messages, counselor_queue, teacher_report),
        encoding="utf-8",
    )

    print("Client-facing demo generated")
    print("----------------------------")
    print(f"Students reviewed: {len(students)}")
    print(f"Engagement alerts created: {len(alerts)}")
    print(f"WhatsApp parent messages prepared: {len(whatsapp_messages)}")
    print(f"Counselor follow-ups created: {len(counselor_queue)}")
    print()
    print(f"Open this file in a browser: {OUTPUT_DIR / 'client-demo.html'}")


def render_whatsapp_markdown(messages: list[dict[str, str]]) -> str:
    lines = ["# WhatsApp Message Preview", ""]
    for message in messages:
        lines.extend(
            [
                f"## {message['student_id']} - {message['student']}",
                "",
                f"- Recipient: {message['recipient']}",
                f"- Phone: {message['phone']}",
                "",
                "```text",
                message["message"],
                "```",
                "",
            ]
        )
    return "\n".join(lines)


def render_counselor_markdown(queue: list[dict[str, str]]) -> str:
    lines = ["# Counselor Action Queue", ""]
    for item in queue:
        lines.extend(
            [
                f"## {item['priority']} - {item['student_id']} - {item['student']}",
                "",
                f"- Counselor: {item['counselor']}",
                f"- Reason: {item['reason']}",
                f"- Next action: {item['next_action']}",
                "",
            ]
        )
    return "\n".join(lines)


def render_html(
    client_name: str,
    alerts: list,
    whatsapp_messages: list[dict[str, str]],
    counselor_queue: list[dict[str, str]],
    teacher_report: str,
) -> str:
    high_alerts = sum(1 for alert in alerts if alert.severity == "high")
    medium_alerts = sum(1 for alert in alerts if alert.severity == "medium")

    whatsapp_cards = "\n".join(
        f"""
        <article class="card">
          <div class="meta">{escape(message['student_id'])} · {escape(message['phone'])}</div>
          <h3>{escape(message['recipient'])}</h3>
          <p>{escape(message['message'])}</p>
        </article>
        """
        for message in whatsapp_messages
    )

    queue_rows = "\n".join(
        f"""
        <tr>
          <td><span class="pill {escape(item['priority'].lower())}">{escape(item['priority'])}</span></td>
          <td>{escape(item['student_id'])}</td>
          <td>{escape(item['student'])}</td>
          <td>{escape(item['counselor'])}</td>
          <td>{escape(item['next_action'])}</td>
        </tr>
        """
        for item in counselor_queue
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(client_name)} Automation Demo</title>
  <style>
    :root {{
      color-scheme: light;
      font-family: Arial, sans-serif;
      color: #202124;
      background: #f5f7fa;
    }}
    body {{
      margin: 0;
    }}
    header {{
      background: #0f5132;
      color: white;
      padding: 28px 32px;
    }}
    main {{
      max-width: 1180px;
      margin: 0 auto;
      padding: 28px 20px 48px;
    }}
    h1, h2, h3 {{
      margin: 0;
      letter-spacing: 0;
    }}
    h1 {{
      font-size: 30px;
      line-height: 1.2;
    }}
    h2 {{
      margin-top: 30px;
      margin-bottom: 14px;
      font-size: 22px;
    }}
    h3 {{
      font-size: 16px;
      margin-top: 6px;
    }}
    .subtitle {{
      margin-top: 8px;
      color: #d8f3dc;
      font-size: 15px;
    }}
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
    }}
    .metric, .card, .report, table {{
      background: white;
      border: 1px solid #dfe5ec;
      border-radius: 8px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
    }}
    .metric {{
      padding: 16px;
    }}
    .number {{
      display: block;
      font-size: 28px;
      font-weight: 700;
      margin-top: 6px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 12px;
    }}
    .card {{
      padding: 16px;
    }}
    .meta {{
      color: #5f6368;
      font-size: 13px;
    }}
    p {{
      line-height: 1.5;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
    }}
    th, td {{
      border-bottom: 1px solid #e8edf3;
      padding: 12px;
      text-align: left;
      vertical-align: top;
      font-size: 14px;
    }}
    th {{
      background: #eef5f0;
    }}
    .pill {{
      display: inline-block;
      border-radius: 999px;
      padding: 4px 9px;
      font-size: 12px;
      font-weight: 700;
    }}
    .high {{
      background: #ffe1dd;
      color: #9f1c0f;
    }}
    .medium {{
      background: #fff0cf;
      color: #744c00;
    }}
    .report {{
      padding: 18px;
      white-space: pre-wrap;
      line-height: 1.5;
      font-family: Consolas, monospace;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{escape(client_name)} Daily Automation Run</h1>
    <div class="subtitle">Synthetic demo showing parent messages, counselor follow-ups, and teacher intelligence output.</div>
  </header>
  <main>
    <section class="metrics">
      <div class="metric">Engagement alerts <span class="number">{len(alerts)}</span></div>
      <div class="metric">High priority <span class="number">{high_alerts}</span></div>
      <div class="metric">Medium priority <span class="number">{medium_alerts}</span></div>
      <div class="metric">WhatsApp messages <span class="number">{len(whatsapp_messages)}</span></div>
      <div class="metric">Counselor tasks <span class="number">{len(counselor_queue)}</span></div>
    </section>

    <h2>Parent WhatsApp Messages</h2>
    <section class="grid">
      {whatsapp_cards}
    </section>

    <h2>Counselor Action Queue</h2>
    <table>
      <thead>
        <tr>
          <th>Priority</th>
          <th>Student ID</th>
          <th>Student</th>
          <th>Counselor</th>
          <th>Next Action</th>
        </tr>
      </thead>
      <tbody>
        {queue_rows}
      </tbody>
    </table>

    <h2>Teacher Daily Report</h2>
    <section class="report">{escape(teacher_report)}</section>
  </main>
</body>
</html>
"""


if __name__ == "__main__":
    main()
