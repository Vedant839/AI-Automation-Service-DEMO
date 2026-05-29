import re

from .models import FAQ


SENSITIVE_TERMS = {
    "password",
    "otp",
    "bank",
    "account number",
    "aadhaar",
    "government id",
    "card number",
}

STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "can",
    "do",
    "for",
    "how",
    "i",
    "in",
    "is",
    "it",
    "me",
    "my",
    "of",
    "on",
    "or",
    "the",
    "to",
    "what",
    "where",
    "with",
    "you",
}

CATEGORY_KEYWORDS = {
    "course": {"course", "courses", "subject", "subjects"},
    "schedule": {"schedule", "schedules", "batch", "batches", "timing", "timings"},
    "fees": {"fee", "fees", "payment", "payments", "pay", "installment", "installments"},
    "scholarship": {"scholarship", "scholarships", "eligibility", "apply", "application"},
    "attendance": {"attendance", "attend", "missed", "class", "classes", "recording"},
    "doubts": {"doubt", "doubts", "question", "questions", "homework"},
    "parents": {"parent", "parents", "progress", "updates", "notification"},
}


def build_faqs(raw_faqs: list[dict[str, str]]) -> list[FAQ]:
    return [FAQ(**item) for item in raw_faqs]


def contains_sensitive_request(message: str) -> bool:
    normalized = message.lower()
    return any(term in normalized for term in SENSITIVE_TERMS)


def answer_support_question(message: str, faqs: list[FAQ], handoff_message: str) -> str:
    if contains_sensitive_request(message):
        return handoff_message

    message_tokens = _meaningful_tokens(message)
    scored: list[tuple[int, FAQ]] = []
    for faq in faqs:
        question_tokens = _meaningful_tokens(faq.question)
        category_terms = CATEGORY_KEYWORDS.get(faq.category.lower(), {faq.category.lower()})
        category_match = 3 if message_tokens & category_terms else 0
        term_matches = len(question_tokens & message_tokens)
        scored.append((category_match + term_matches, faq))

    best_score, best_faq = max(scored, key=lambda item: item[0])
    if best_score < 3:
        return handoff_message
    return best_faq.answer


def _meaningful_tokens(text: str) -> set[str]:
    tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
    return {token for token in tokens if token not in STOP_WORDS}
