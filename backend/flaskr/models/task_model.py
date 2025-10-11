"""
Task Model Module

This module defines the TaskModel class and TaskStatus enum for task management.
"""

from enum import Enum
from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Enum as SaEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flaskr.db import db


class TaskStatus(Enum):
    """
    Enumeration of possible task statuses.

    Attributes:
        PENDING: Task is created but not started
        IN_PROGRESS: Task is currently being worked on
        COMPLETED: Task has been finished

    Example:
        >>> task.status = TaskStatus.IN_PROGRESS
        >>> if task.status == TaskStatus.COMPLETED:
        ...     print("Task is done!")
    """

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class TaskModel(db.Model):
    """
    Task database model for managing user tasks.

    This model represents a task/todo item with status tracking, timestamps,
    and associations to users and tags.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier
        title (str): Task title, max 40 characters, indexed for search
        content (str): Detailed task description, max 600 characters
        status (TaskStatus): Current task status (PENDING, IN_PROGRESS, COMPLETED)
        created_at (datetime): UTC timestamp when task was created, indexed
        user_id (int): Foreign key to users table
        user (relationship): Many-to-one relationship with UserModel
        tag_id (int): Foreign key to tags table
        tag (relationship): Many-to-one relationship with TagModel

    Table:
        tasks

    Constraints:
        - All fields are required (non-nullable)
        - user_id must reference existing user
        - tag_id must reference existing tag

    Indexes:
        - title: For fast task search
        - created_at: For chronological ordering

    Example:
        >>> task = TaskModel(
        ...     title="Complete project",
        ...     content="Finish the documentation",
        ...     status=TaskStatus.PENDING,
        ...     user_id=1,
        ...     tag_id=2
        ... )
        >>> db.session.add(task)
        >>> db.session.commit()
    """

    __tablename__ = "tasks"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Task information
    title: Mapped[str] = mapped_column(String(40), nullable=False, index=True)
    content: Mapped[str] = mapped_column(String(600), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SaEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING
    )
    created_at: Mapped[datetime] = mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc)
    )

    # Foreign keys and relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user = relationship("UserModel", back_populates="tasks")

    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False)
    tag = relationship("TagModel", back_populates="tasks")
