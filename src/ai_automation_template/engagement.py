from typing import Any

from .models import EngagementAlert, StudentSnapshot


def build_students(raw_students: list[dict[str, Any]]) -> list[StudentSnapshot]:
    return [StudentSnapshot(**item) for item in raw_students]


def evaluate_student_engagement(
    student: StudentSnapshot,
    rules: dict[str, Any],
) -> list[EngagementAlert]:
    alerts: list[EngagementAlert] = []
    notify_parent = bool(rules.get("parent_notification_enabled", True))
    escalate = bool(rules.get("counselor_escalation_enabled", True))

    if student.last_active_days_ago >= int(rules.get("inactive_days_threshold", 7)):
        alerts.append(
            EngagementAlert(
                student.student_id,
                student.display_name,
                "inactive_student",
                "medium",
                f"No activity for {student.last_active_days_ago} days.",
                notify_parent,
                escalate,
            )
        )

    if student.missed_classes_last_14_days >= int(rules.get("missed_classes_threshold", 2)):
        alerts.append(
            EngagementAlert(
                student.student_id,
                student.display_name,
                "missed_classes",
                "medium",
                f"Missed {student.missed_classes_last_14_days} classes in the last 14 days.",
                notify_parent,
                escalate,
            )
        )

    if student.latest_score_percent <= int(rules.get("low_score_threshold_percent", 50)):
        alerts.append(
            EngagementAlert(
                student.student_id,
                student.display_name,
                "low_score",
                "high",
                f"Latest score is {student.latest_score_percent}%.",
                notify_parent,
                escalate,
            )
        )

    score_drop = student.previous_score_percent - student.latest_score_percent
    if score_drop >= int(rules.get("score_decline_threshold_percent", 15)):
        alerts.append(
            EngagementAlert(
                student.student_id,
                student.display_name,
                "score_decline",
                "high",
                f"Score declined by {score_drop} percentage points.",
                notify_parent,
                escalate,
            )
        )

    return alerts


def evaluate_all_students(
    students: list[StudentSnapshot],
    rules: dict[str, Any],
) -> list[EngagementAlert]:
    alerts: list[EngagementAlert] = []
    for student in students:
        alerts.extend(evaluate_student_engagement(student, rules))
    return alerts
