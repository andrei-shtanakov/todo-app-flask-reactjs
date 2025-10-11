"""
User Model Module

This module defines the UserModel class for user authentication and management.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flaskr.db import db


class UserModel(db.Model):
    """
    User database model for authentication and user management.

    This model stores user credentials and personal information. Each user can have
    multiple tasks associated with them through a one-to-many relationship.

    Attributes:
        id (int): Primary key, auto-incremented unique identifier
        username (str): Unique username, max 20 characters, indexed for fast lookup
        email (str): Unique email address, max 120 characters, indexed for fast lookup
        password (str): Hashed password, max 300 characters (bcrypt hash)
        tasks (relationship): One-to-many relationship with TaskModel, cascades delete

    Table:
        users

    Constraints:
        - username must be unique
        - email must be unique
        - All fields are required (non-nullable)

    Example:
        >>> user = UserModel(
        ...     username="johndoe",
        ...     email="john@example.com",
        ...     password=hashed_password
        ... )
        >>> db.session.add(user)
        >>> db.session.commit()
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[int] = mapped_column(primary_key=True)

    # User credentials
    username: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True, index=True
    )
    email: Mapped[str] = mapped_column(
        String(120), nullable=False, unique=True, index=True
    )
    password: Mapped[str] = mapped_column(String(300), nullable=False)

    # Relationships - one user can have many tasks
    tasks = relationship(
        "TaskModel", back_populates="user", cascade="all, delete-orphan"
    )
