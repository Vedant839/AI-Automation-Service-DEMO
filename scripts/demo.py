from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from ai_automation_template.chatbot import answer_support_question, build_faqs
from ai_automation_template.config import get_nested, load_json
from ai_automation_template.engagement import build_students, evaluate_all_students
from ai_automation_template.reports import summarize_teacher_intelligence


def main() -> None:
    config = load_json(ROOT / "config" / "client_profile.synthetic.json")
    faqs = build_faqs(load_json(ROOT / "data" / "synthetic_faqs.json"))
    students = build_students(load_json(ROOT / "data" / "synthetic_students.json"))

    handoff_message = get_nested(
        config,
        "support_assistant.handoff_message",
        "A counselor will help with this.",
    )
    sample_question = "Can I pay course fees in installments?"
    answer = answer_support_question(sample_question, faqs, handoff_message)

    rules = get_nested(config, "engagement_rules", {})
    alerts = evaluate_all_students(students, rules)

    include_names = bool(get_nested(config, "teacher_reports.include_student_names", False))
    report = summarize_teacher_intelligence(students, alerts, include_names)

    print("Support assistant demo")
    print("----------------------")
    print(f"Student: {sample_question}")
    print(f"Assistant: {answer}")
    print()
    print("Engagement alerts")
    print("-----------------")
    for alert in alerts:
        print(f"{alert.severity.upper()} | {alert.student_id} | {alert.alert_type}: {alert.message}")
    print()
    print(report)


if __name__ == "__main__":
    main()
