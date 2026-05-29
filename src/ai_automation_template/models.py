from dataclasses import dataclass, field


@dataclass(frozen=True)
class FAQ:
    id: str
    category: str
    question: str
    answer: str


@dataclass(frozen=True)
class StudentSnapshot:
    student_id: str
    display_name: str
    last_active_days_ago: int
    missed_classes_last_14_days: int
    latest_score_percent: int
    previous_score_percent: int
    frequent_doubts: list[str] = field(default_factory=list)
    weak_topics: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EngagementAlert:
    student_id: str
    display_name: str
    alert_type: str
    severity: str
    message: str
    notify_parent: bool
    escalate_to_counselor: bool
