"""
Authentication Controller Module

This module handles user authentication operations including sign-in
and JWT token generation.
"""

from flask_jwt_extended import create_access_token
from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from flaskr.db import db
from flaskr.models.user_model import UserModel
from flaskr.utils import check_password


class AuthController:
    """
    Controller for authentication operations.

    This controller handles user authentication including credential verification
    and JWT token generation for authenticated sessions.

    Methods:
        sign_in: Authenticate user and generate JWT access token
    """

    @staticmethod
    def sign_in(data: dict) -> dict:
        """
        Authenticate user and generate JWT access token.

        This method validates user credentials (email and password) and returns
        a JWT access token upon successful authentication.

        Args:
            data (dict): Authentication credentials containing:
                - email (str): User's email address
                - password (str): User's plain-text password

        Returns:
            dict: Dictionary containing JWT access token:
                {
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                }

        Raises:
            HTTPException 401: Invalid credentials (user not found or wrong password)
            HTTPException 500: Database error during authentication

        Security:
            - Passwords are compared using constant-time comparison
            - Failed login attempts don't reveal whether email exists
            - JWT token expires based on app configuration

        Example:
            >>> credentials = {
            ...     "email": "user@example.com",
            ...     "password": "mypassword123"
            ... }
            >>> result = AuthController.sign_in(credentials)
            >>> print(result["token"])
            eyJ0eXAiOiJKV1QiLCJhbGc...

        Note:
            This method performs database rollback automatically on errors
            to maintain database consistency.
        """
        try:
            # Query database for user by email
            user_registered = db.session.execute(
                select(UserModel).where(UserModel.email == data["email"])
            ).scalar_one_or_none()

            # Verify user exists and password is correct
            if (
                user_registered is None
                or check_password(user_registered.password, data["password"]) is False
            ):
                abort(401, message="Incorrect credentials")

            # Generate JWT access token with user ID as identity
            token = create_access_token(identity=str(user_registered.id))

            return {"token": token}

        except SQLAlchemyError:
            # Rollback transaction on database error
            db.session.rollback()
            abort(500, message="Internal server error while sign in")
