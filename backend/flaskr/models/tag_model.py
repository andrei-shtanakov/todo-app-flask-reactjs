"""
Tag Model Module

This module defines the TagModel class for categorizing and organizing tasks.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flaskr.db import db


class TagModel(db.Model):
    """
    Tag database model for categorizing tasks.

    This model represents categories or labels that can be assigned to tasks
    for organization and filtering purposes.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier
        name (str): Tag name, max 20 characters, unique and indexed
        tasks (relationship): One-to-many relationship with TaskModel, cascades delete

    Table:
        tags

    Constraints:
        - name must be unique across all tags
        - name is required (non-nullable)

    Indexes:
        - name: For fast tag lookup and search

    Cascade Behavior:
        - When a tag is deleted, all associated tasks are also deleted

    Example:
        >>> tag = TagModel(name="Work")
        >>> db.session.add(tag)
        >>> db.session.commit()

        >>> # Later, assign to a task
        >>> task.tag_id = tag.id
    """

    __tablename__ = "tags"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # Tag information
    name: Mapped[str] = mapped_column(
        String(20), nullable=False, index=True, unique=True
    )

    # Relationships - one tag can have many tasks
    tasks = relationship(
        "TaskModel", back_populates="tag", cascade="all, delete-orphan"
    )
