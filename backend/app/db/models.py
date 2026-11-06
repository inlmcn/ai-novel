from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import UUID

from sqlalchemy import (
    CheckConstraint, DateTime, ForeignKey, ForeignKeyConstraint, Index,
    Integer, JSON, String, Text, UniqueConstraint, Uuid
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKey

JSON_DOCUMENT = JSON().with_variant(JSONB(), "postgresql")


class NovelStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class ChapterStatus(str, Enum):
    OUTLINE = "outline"
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    REVISION_REQUIRED = "revision_required"
    APPROVED = "approved"
    REJECTED = "rejected"


class ReviewDecision(str, Enum):
    PASS = "pass"
    REVISE = "revise"
    REJECT = "reject"
    HUMAN_REQUIRED = "human_required"


class MemoryStatus(str, Enum):
    CANDIDATE = "candidate"
    ACTIVE = "active"
    SUPERSEDED = "superseded"
    REJECTED = "rejected"


class Novel(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "novels"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    genre: Mapped[str | None] = mapped_column(String(80))
    synopsis: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(24), default=NovelStatus.DRAFT.value, nullable=False)
    settings: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)


class Chapter(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "chapters"
    __table_args__ = (
        ForeignKeyConstraint(
            ["current_version_id", "id"],
            ["chapter_versions.id", "chapter_versions.chapter_id"],
            name="fk_chapters_current_version_same_chapter",
            use_alter=True,
        ),
        UniqueConstraint("novel_id", "chapter_no", name="uq_chapters_novel_chapter_no"),
        CheckConstraint("chapter_no > 0", name="chapter_no_positive"),
        CheckConstraint("version >= 1", name="version_positive"),
        Index("ix_chapters_novel_status", "novel_id", "status"),
    )

    novel_id: Mapped[UUID] = mapped_column(ForeignKey("novels.id", ondelete="CASCADE"), nullable=False)
    chapter_no: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default=ChapterStatus.OUTLINE.value, nullable=False)
    current_version_id: Mapped[UUID | None] = mapped_column(Uuid(as_uuid=True))
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    outline: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)


class ChapterVersion(UUIDPrimaryKey, Base):
    __tablename__ = "chapter_versions"
    __table_args__ = (
        UniqueConstraint("id", "chapter_id", name="uq_chapter_versions_id_chapter_id"),
        UniqueConstraint("chapter_id", "version_no", name="uq_chapter_versions_chapter_version"),
        UniqueConstraint("chapter_id", "idempotency_key", name="uq_chapter_versions_idempotency"),
        CheckConstraint("version_no > 0", name="version_no_positive"),
        Index("ix_chapter_versions_chapter_created", "chapter_id", "created_at"),
    )

    chapter_id: Mapped[UUID] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    version_no: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    idempotency_key: Mapped[str] = mapped_column(String(128), nullable=False)
    created_by: Mapped[str] = mapped_column(String(80), default="system", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)


class ReviewReport(UUIDPrimaryKey, Base):
    __tablename__ = "review_reports"
    __table_args__ = (
        ForeignKeyConstraint(
            ["chapter_version_id", "chapter_id"],
            ["chapter_versions.id", "chapter_versions.chapter_id"],
            name="fk_review_reports_version_same_chapter",
            ondelete="CASCADE",
        ),
        UniqueConstraint("id", "chapter_id", name="uq_review_reports_id_chapter_id"),
        Index("ix_review_reports_chapter_created", "chapter_id", "created_at"),
    )

    chapter_id: Mapped[UUID] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    chapter_version_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    reviewer_type: Mapped[str] = mapped_column(String(64), nullable=False)
    model_name: Mapped[str] = mapped_column(String(120), nullable=False)
    rubric_version: Mapped[str] = mapped_column(String(40), nullable=False)
    score: Mapped[int | None] = mapped_column(Integer)
    decision: Mapped[str] = mapped_column(String(32), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    evidence: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class ReviewIssue(UUIDPrimaryKey, Base):
    __tablename__ = "review_issues"
    __table_args__ = (
        ForeignKeyConstraint(
            ["review_report_id", "chapter_id"],
            ["review_reports.id", "review_reports.chapter_id"],
            name="fk_review_issues_report_same_chapter",
            ondelete="CASCADE",
        ),
        Index("ix_review_issues_report_severity", "review_report_id", "severity"),
    )

    review_report_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    chapter_id: Mapped[UUID] = mapped_column(ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    category: Mapped[str] = mapped_column(String(64), nullable=False)
    severity: Mapped[str] = mapped_column(String(24), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_quote: Mapped[str] = mapped_column(Text, nullable=False)
    location: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="open", nullable=False)


class AgentRun(UUIDPrimaryKey, Base):
    __tablename__ = "agent_runs"
    __table_args__ = (Index("ix_agent_runs_status_created", "status", "created_at"),)

    novel_id: Mapped[UUID] = mapped_column(ForeignKey("novels.id", ondelete="CASCADE"), nullable=False)
    chapter_id: Mapped[UUID | None] = mapped_column(ForeignKey("chapters.id", ondelete="SET NULL"))
    workflow_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(24), default="queued", nullable=False)
    input_payload: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)
    output_payload: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)


class StoryMemory(UUIDPrimaryKey, TimestampMixin, Base):
    __tablename__ = "story_memories"
    __table_args__ = (
        Index("ix_story_memories_novel_status_type", "novel_id", "status", "memory_type"),
    )

    novel_id: Mapped[UUID] = mapped_column(ForeignKey("novels.id", ondelete="CASCADE"), nullable=False)
    memory_type: Mapped[str] = mapped_column(String(48), nullable=False)
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    fact: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(24), default=MemoryStatus.CANDIDATE.value, nullable=False)
    source_version_id: Mapped[UUID | None] = mapped_column(ForeignKey("chapter_versions.id", ondelete="SET NULL"))
    confidence: Mapped[float | None] = mapped_column()
    attributes: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)


class OutboxEvent(UUIDPrimaryKey, Base):
    __tablename__ = "outbox_events"
    __table_args__ = (Index("ix_outbox_events_published_created", "published_at", "created_at"),)

    aggregate_type: Mapped[str] = mapped_column(String(80), nullable=False)
    aggregate_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False)
    event_type: Mapped[str] = mapped_column(String(120), nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON_DOCUMENT, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
