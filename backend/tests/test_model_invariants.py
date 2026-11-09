from sqlalchemy import CheckConstraint, ForeignKeyConstraint

from app.db.base import Base
from app.db.models import (
    AgentRun,
    Chapter,
    ChapterVersion,
    Novel,
    OutboxEvent,
    ReviewIssue,
    ReviewReport,
    StoryMemory,
)


def _checks(table_name: str) -> set[str]:
    table = Base.metadata.tables[table_name]
    return {
        str(constraint.sqltext)
        for constraint in table.constraints
        if isinstance(constraint, CheckConstraint)
    }


def test_domain_statuses_are_database_constrained() -> None:
    assert any("draft" in check and "archived" in check for check in _checks("novels"))
    assert any("in_review" in check and "approved" in check for check in _checks("chapters"))
    assert any("human_required" in check for check in _checks("review_reports"))
    assert any("queued" in check and "cancelled" in check for check in _checks("agent_runs"))
    assert any("superseded" in check for check in _checks("story_memories"))


def test_review_and_memory_numeric_ranges_are_constrained() -> None:
    assert any("BETWEEN 0 AND 100" in check for check in _checks("review_reports"))
    assert any("BETWEEN 0.0 AND 1.0" in check for check in _checks("story_memories"))


def test_chapter_version_is_idempotent_and_monotonic() -> None:
    table = Base.metadata.tables["chapter_versions"]
    unique_sets = {
        tuple(column.name for column in constraint.columns)
        for constraint in table.constraints
        if getattr(constraint, "name", None)
        and constraint.__class__.__name__ == "UniqueConstraint"
    }
    assert ("chapter_id", "version_no") in unique_sets
    assert ("chapter_id", "idempotency_key") in unique_sets
    assert any("version_no > 0" in check for check in _checks("chapter_versions"))


def test_review_report_and_issue_are_bound_to_same_chapter() -> None:
    report_fks = [
        constraint
        for constraint in Base.metadata.tables["review_reports"].constraints
        if isinstance(constraint, ForeignKeyConstraint)
    ]
    issue_fks = [
        constraint
        for constraint in Base.metadata.tables["review_issues"].constraints
        if isinstance(constraint, ForeignKeyConstraint)
    ]
    assert any(len(fk.elements) == 2 for fk in report_fks)
    assert any(len(fk.elements) == 2 for fk in issue_fks)


def test_outbox_retry_counter_cannot_be_negative() -> None:
    assert any("attempts >= 0" in check for check in _checks("outbox_events"))
