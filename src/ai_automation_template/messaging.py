from collections import defaultdict
from typing import Any

from .models import EngagementAlert, StudentSnapshot


def build_parent_whatsapp_messages(
    alerts: list[EngagementAlert],
    students: list[StudentSnapshot],
    contacts: list[dict[str, Any]],
    client_name: str,
) -> list[dict[str, str]]:
    student_by_id = {student.student_id: student for student in students}
    contact_by_id = {contact["student_id"]: contact for contact in contacts}
    grouped_alerts: dict[str, list[EngagementAlert]] = defaultdict(list)

    for alert in alerts:
        if alert.notify_parent:
            grouped_alerts[alert.student_id].append(alert)

    messages: list[dict[str, str]] = []
    for student_id, student_alerts in grouped_alerts.items():
        student = student_by_id[student_id]
        contact = contact_by_id.get(student_id, {})
        message = _parent_message_text(student, student_alerts, contact, client_name)
        messages.append(
            {
                "channel": "WhatsApp",
                "student_id": student_id,
                "student": student.display_name,
                "recipient": contact.get("parent_name", "Parent/Guardian"),
                "phone": contact.get("parent_phone_label", "Not configured"),
                "message": message,
            }
        )

    return messages


def build_counselor_queue(
    alerts: list[EngagementAlert],
    students: list[StudentSnapshot],
    contacts: list[dict[str, Any]],
) -> list[dict[str, str]]:
    student_by_id = {student.student_id: student for student in students}
    contact_by_id = {contact["student_id"]: contact for contact in contacts}
    grouped_alerts: dict[str, list[EngagementAlert]] = defaultdict(list)

    for alert in alerts:
        if alert.escalate_to_counselor:
            grouped_alerts[alert.student_id].append(alert)

    queue: list[dict[str, str]] = []
    for student_id, student_alerts in grouped_alerts.items():
        student = student_by_id[student_id]
        contact = contact_by_id.get(student_id, {})
        high_count = sum(1 for alert in student_alerts if alert.severity == "high")
        priority = "High" if high_count else "Medium"
        reasons = "; ".join(alert.message for alert in student_alerts)
        queue.append(
            {
                "priority": priority,
                "student_id": student_id,
                "student": student.display_name,
                "counselor": contact.get("counselor_name", "Unassigned"),
                "reason": reasons,
                "next_action": _next_counselor_action(priority),
            }
        )

    priority_order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(queue, key=lambda item: (priority_order[item["priority"]], item["student_id"]))


def _parent_message_text(
    student: StudentSnapshot,
    alerts: list[EngagementAlert],
    contact: dict[str, Any],
    client_name: str,
) -> str:
    parent_name = contact.get("parent_name", "Parent")
    alert_types = {alert.alert_type for alert in alerts}

    if "low_score" in alert_types or "score_decline" in alert_types:
        concern = "recent test performance shows that extra support would help"
    elif "missed_classes" in alert_types:
        concern = f"{student.display_name} has missed recent live classes"
    elif "inactive_student" in alert_types:
        concern = f"{student.display_name} has not been active on the learning portal"
    else:
        concern = f"{student.display_name} may need additional support"

    return (
        f"Hi {parent_name}, this is {client_name}. "
        f"Our learning system noticed that {concern}. "
        "Please ask them to complete pending work today. "
        "A counselor will follow up if support is needed."
    )


def _next_counselor_action(priority: str) -> str:
    if priority == "High":
        return "Call parent/student today and schedule a support plan."
    return "Send reminder and review progress in the next daily check."
