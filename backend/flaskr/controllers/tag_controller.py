"""
Tag Controller Module

This module handles all tag-related operations including tag retrieval
and creation for organizing and categorizing tasks.
"""

from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from flaskr.db import db
from flaskr.models.tag_model import TagModel


class TagController:
    """
    Controller for tag management operations.

    This controller handles retrieval and creation of tags used for
    categorizing tasks. Tags are global and shared across all users.

    Methods:
        get_all: Retrieve all available tags (limited to 15)
        create: Create a new tag
    """

    @staticmethod
    def get_all() -> list[TagModel]:
        """
        Retrieve all available tags from the database.

        This method fetches all tags with a limit of 15 results for
        performance and UI considerations.

        Args:
            None

        Returns:
            list[TagModel]: List of tag objects (maximum 15)

        Raises:
            HTTPException 500: Database error during retrieval

        Behavior:
            - Returns maximum 15 tags
            - No authentication required
            - Tags are global (not user-specific)

        Example:
            >>> tags = TagController.get_all()
            >>> for tag in tags:
            ...     print(tag.name)
            Work
            Personal
            Urgent

        Note:
            The limit of 15 may need adjustment based on UI requirements.
            Consider adding pagination for applications with many tags.
        """
        try:
            return db.session.execute(select(TagModel).limit(15)).scalars().all()
        except SQLAlchemyError:
            abort(500, message="Internal server error while fetching tags")

    @staticmethod
    def create(data: dict) -> None:
        """
        Create a new tag.

        This method creates a new tag after validating that the tag name
        is unique. Tags are global and can be used by all users.

        Args:
            data (dict): Tag creation data containing:
                - name (str): Tag name (max 20 chars, must be unique)

        Returns:
            None

        Raises:
            HTTPException 409: Tag name already exists
            HTTPException 500: Database error during creation

        Validation:
            - Checks tag name uniqueness before creation
            - Returns specific conflict error if tag exists
            - Name length limited to 20 characters (model constraint)

        Example:
            >>> tag_data = {"name": "Important"}
            >>> TagController.create(tag_data)
            # Tag created successfully

            >>> # Attempting to create duplicate
            >>> TagController.create(tag_data)
            # Raises 409: Tag already registered

        Design Note:
            Tags are global across all users. Consider adding user_id
            if you need user-specific tags in the future.

        Note:
            Transaction is automatically rolled back on any error to
            maintain database consistency.
        """
        try:
            # Check if tag with same name already exists
            tag_registered = db.session.execute(
                select(TagModel).where(TagModel.name == data["name"])
            ).scalar_one_or_none()

            # Prevent duplicate tag names
            if tag_registered:
                abort(409, message="Tag already registered")

            # Create new tag instance
            new_tag = TagModel(**data)

            # Save to database
            db.session.add(new_tag)
            db.session.commit()

        except SQLAlchemyError:
            # Rollback on database errors
            db.session.rollback()
            abort(500, message="Internal server error while creating tag")
