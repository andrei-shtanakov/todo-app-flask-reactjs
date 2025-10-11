"""
User Controller Module

This module handles all user-related operations including user retrieval,
creation, and deletion with proper authentication and authorization.
"""

from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from flaskr.db import db
from flaskr.models.user_model import UserModel
from flaskr.utils import generate_password


class UserController:
    """
    Controller for user management operations.

    This controller handles CRUD operations for users including listing,
    retrieving, creating, and deleting user accounts.

    Methods:
        get_all: Retrieve all users from database
        get_by_id: Retrieve specific user by ID
        create: Create new user account
        delete: Delete authenticated user's account
    """

    @staticmethod
    def get_all() -> list[UserModel]:
        """
        Retrieve all users from the database.

        This method fetches all user records from the database. Typically used
        for admin interfaces or user listings.

        Returns:
            list[UserModel]: List of all user objects

        Raises:
            HTTPException 500: Database error during retrieval

        Example:
            >>> users = UserController.get_all()
            >>> for user in users:
            ...     print(user.username, user.email)
            johndoe john@example.com
            janedoe jane@example.com

        Note:
            This endpoint may need pagination for production use with many users.
        """
        try:
            return db.session.execute(select(UserModel)).scalars().all()
        except SQLAlchemyError:
            abort(500, message="Internal server error while fetching users")

    @staticmethod
    def get_by_id(user_id: int) -> UserModel:
        """
        Retrieve a specific user by their ID.

        This method fetches a single user record by their unique identifier.

        Args:
            user_id (int): The unique identifier of the user

        Returns:
            UserModel: The requested user object

        Raises:
            HTTPException 404: User not found
            HTTPException 500: Database error during retrieval

        Example:
            >>> user = UserController.get_by_id(1)
            >>> print(f"{user.username}: {user.email}")
            johndoe: john@example.com

        Note:
            This method does not check authorization. Add JWT checks if needed.
        """
        try:
            return db.session.execute(
                select(UserModel).where(UserModel.id == user_id)
            ).scalar_one()
        except NoResultFound:
            abort(404, message="User not found")
        except SQLAlchemyError:
            abort(500, message="Internal server error while fetching user")

    @staticmethod
    def create(data: dict) -> None:
        """
        Create a new user account.

        This method handles user registration by validating uniqueness of
        username and email, hashing the password, and storing the user.

        Args:
            data (dict): User registration data containing:
                - username (str): Desired username
                - email (str): Email address
                - password (str): Plain-text password (will be hashed)

        Returns:
            None

        Raises:
            HTTPException 409: Username or email already registered
            HTTPException 500: Database error during creation

        Validation:
            - Checks username uniqueness
            - Checks email uniqueness
            - Returns specific error message for each conflict

        Security:
            - Password is automatically hashed before storage
            - Uses bcrypt with salt for secure password storage

        Example:
            >>> user_data = {
            ...     "username": "newuser",
            ...     "email": "new@example.com",
            ...     "password": "securepass123"
            ... }
            >>> UserController.create(user_data)
            # User created successfully

        Note:
            Transaction is automatically rolled back on any error to maintain
            database consistency.
        """
        try:
            # Check if username or email already exists
            user_registered = db.session.execute(
                select(UserModel).where(
                    (UserModel.username == data["username"])
                    | (UserModel.email == data["email"])
                )
            ).scalar_one_or_none()

            # If user exists, determine which field conflicts
            if user_registered:
                if user_registered.username == data["username"]:
                    abort(409, message="Username already registered")
                if user_registered.email == data["email"]:
                    abort(409, message="Email already registered")

            # Create new user instance
            new_user = UserModel(**data)

            # Hash password before storing
            new_user.password = generate_password(data["password"])

            # Save to database
            db.session.add(new_user)
            db.session.commit()

        except SQLAlchemyError:
            # Rollback on database errors
            db.session.rollback()
            abort(500, message="Internal server error while creating user")

    @staticmethod
    def delete() -> None:
        """
        Delete the authenticated user's account.

        This method deletes the currently authenticated user's account based
        on their JWT token identity. Cascades to delete all related tasks.

        Args:
            None (uses JWT identity from token)

        Returns:
            None

        Raises:
            HTTPException 404: User not found (token may be invalid)
            HTTPException 500: Database error during deletion

        Authorization:
            - Requires valid JWT token
            - User can only delete their own account
            - JWT identity must match existing user

        Cascade Behavior:
            - Deletes all tasks associated with the user
            - Maintains referential integrity

        Example:
            >>> # With JWT token in request headers
            >>> UserController.delete()
            # User account deleted successfully

        Security:
            - Uses JWT token to identify user (no user_id parameter)
            - Prevents users from deleting other accounts
            - Requires authentication

        Note:
            This is a destructive operation and cannot be undone.
            Consider adding soft delete or confirmation in production.
        """
        try:
            # Get authenticated user ID from JWT token
            user_id = get_jwt_identity()

            # Fetch user to delete
            user = db.session.execute(
                select(UserModel).where(UserModel.id == user_id)
            ).scalar_one()

            # Delete user (cascades to tasks)
            db.session.delete(user)
            db.session.commit()

        except NoResultFound:
            abort(404, message="User not found")
        except SQLAlchemyError:
            # Rollback on database errors
            db.session.rollback()
            abort(500, message="Internal server error while deleting user")
