from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from ai_automation_template.chatbot import answer_support_question, build_faqs
from ai_automation_template.config import get_nested, load_json
from ai_automation_template.engagement import build_students, evaluate_all_students
from ai_automation_template.messaging import build_counselor_queue, build_parent_whatsapp_messages
from ai_automation_template.reports import summarize_teacher_intelligence


class TemplateFlowTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_json(ROOT / "config" / "client_profile.synthetic.json")
        cls.faqs = build_faqs(load_json(ROOT / "data" / "synthetic_faqs.json"))
        cls.students = build_students(load_json(ROOT / "data" / "synthetic_students.json"))
        cls.contacts = load_json(ROOT / "data" / "synthetic_contacts.json")
        cls.handoff = get_nested(
            cls.config,
            "support_assistant.handoff_message",
            "A counselor will help with this.",
        )

    def test_support_assistant_answers_fee_question(self) -> None:
        answer = answer_support_question(
            "Can I pay my course fees in installments?",
            self.faqs,
            self.handoff,
        )

        self.assertIn("Installment options", answer)

    def test_support_assistant_answers_schedule_question(self) -> None:
        answer = answer_support_question(
            "Where can I check the batch schedule?",
            self.faqs,
            self.handoff,
        )

        self.assertIn("AsterLearn student portal", answer)

    def test_support_assistant_answers_scholarship_question(self) -> None:
        answer = answer_support_question(
            "How do students apply for scholarship?",
            self.faqs,
            self.handoff,
        )

        self.assertIn("diagnostic test", answer)

    def test_support_assistant_answers_missed_class_question(self) -> None:
        answer = answer_support_question(
            "I missed a live class, what should I do?",
            self.faqs,
            self.handoff,
        )

        self.assertIn("Recordings", answer)

    def test_support_assistant_hands_off_sensitive_request(self) -> None:
        answer = answer_support_question(
            "Can you send my password and bank account details?",
            self.faqs,
            self.handoff,
        )

        self.assertEqual(self.handoff, answer)

    def test_support_assistant_hands_off_unknown_question(self) -> None:
        answer = answer_support_question(
            "Can the AI tutor me live for two hours tonight?",
            self.faqs,
            self.handoff,
        )

        self.assertEqual(self.handoff, answer)

    def test_engagement_alerts_cover_contract_triggers(self) -> None:
        alerts = evaluate_all_students(
            self.students,
            get_nested(self.config, "engagement_rules", {}),
        )
        alert_types = {alert.alert_type for alert in alerts}

        self.assertIn("inactive_student", alert_types)
        self.assertIn("missed_classes", alert_types)
        self.assertIn("low_score", alert_types)
        self.assertIn("score_decline", alert_types)

    def test_teacher_report_summarizes_risk_and_topics(self) -> None:
        alerts = evaluate_all_students(
            self.students,
            get_nested(self.config, "engagement_rules", {}),
        )
        report = summarize_teacher_intelligence(self.students, alerts)

        self.assertIn("At-risk students: 5", report)
        self.assertIn("algebra", report)
        self.assertIn("quadratic equations", report)

    def test_parent_whatsapp_messages_are_prepared_from_alerts(self) -> None:
        alerts = evaluate_all_students(
            self.students,
            get_nested(self.config, "engagement_rules", {}),
        )
        messages = build_parent_whatsapp_messages(
            alerts,
            self.students,
            self.contacts,
            get_nested(self.config, "client.name"),
        )

        self.assertEqual(6, len(messages))
        self.assertIn("AsterLearn Academy", messages[0]["message"])
        self.assertEqual("WhatsApp", messages[0]["channel"])

    def test_counselor_queue_prioritizes_high_risk_students(self) -> None:
        alerts = evaluate_all_students(
            self.students,
            get_nested(self.config, "engagement_rules", {}),
        )
        queue = build_counselor_queue(alerts, self.students, self.contacts)

        self.assertEqual(6, len(queue))
        self.assertEqual("High", queue[0]["priority"])
        self.assertIn("Call parent/student today", queue[0]["next_action"])


if __name__ == "__main__":
    unittest.main()
