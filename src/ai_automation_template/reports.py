from collections import Counter

from .models import EngagementAlert, StudentSnapshot


def summarize_teacher_intelligence(
    students: list[StudentSnapshot],
    alerts: list[EngagementAlert],
    include_student_names: bool = False,
) -> str:
    weak_topics = Counter(topic for student in students for topic in student.weak_topics)
    doubts = Counter(doubt for student in students for doubt in student.frequent_doubts)
    at_risk_ids = {alert.student_id for alert in alerts if alert.severity == "high"}

    lines = [
        "Daily Teacher Intelligence Summary",
        "",
        f"Students reviewed: {len(students)}",
        f"At-risk students: {len(at_risk_ids)}",
        "",
        "Weak topics:",
    ]
    lines.extend(_format_counter(weak_topics))
    lines.extend(["", "Frequently asked doubts:"])
    lines.extend(_format_counter(doubts))
    lines.extend(["", "Recommended actions:"])
    lines.extend(_recommended_actions(students, at_risk_ids, include_student_names))
    return "\n".join(lines)


def _format_counter(counter: Counter[str]) -> list[str]:
    if not counter:
        return ["- No data available"]
    return [f"- {item}: {count}" for item, count in counter.most_common(5)]


def _recommended_actions(
    students: list[StudentSnapshot],
    at_risk_ids: set[str],
    include_student_names: bool,
) -> list[str]:
    if not at_risk_ids:
        return ["- Continue current teaching plan and monitor engagement."]

    actions = ["- Review weak topics in the next class recap."]
    for student in students:
        if student.student_id not in at_risk_ids:
            continue
        label = student.display_name if include_student_names else student.student_id
        topics = ", ".join(student.weak_topics[:3]) or "recent class topics"
        actions.append(f"- Schedule support for {label}: {topics}.")
    return actions
