"""
User Routes Module

This module defines RESTful API endpoints for user management operations
including user listing, retrieval, registration, and account deletion.
"""

from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask.views import MethodView

from flaskr.schemas.schema import UserSchema
from flaskr.controllers.user_controller import UserController

# Create users blueprint
bp = Blueprint("users", __name__)


@bp.route("/users")
class Users(MethodView):
    """
    User collection endpoint.

    This class-based view handles operations on the user collection
    including listing all users and creating new user accounts.

    Endpoints:
        GET  /api/v1/users - List all users
        POST /api/v1/users - Register new user
    """

    @bp.response(200, UserSchema(many=True))
    def get(self):
        """
        Retrieve all users from the system.

        This endpoint returns a list of all registered users. Typically
        used for admin interfaces or user directories.

        Args:
            None

        Returns:
            list[dict]: List of user objects (excludes passwords):
                [
                    {
                        "id": 1,
                        "username": "johndoe",
                        "email": "john@example.com"
                    },
                    ...
                ]

        Status Codes:
            200: Successfully retrieved users
            500: Internal server error

        Example Request:
            GET /api/v1/users
            Accept: application/json

        Example Response:
            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com"
                },
                {
                    "id": 2,
                    "username": "janedoe",
                    "email": "jane@example.com"
                }
            ]

        Security:
            - No authentication required (consider adding)
            - Passwords are excluded from response
            - May expose user emails (consider privacy implications)

        Note:
            Consider adding pagination for production use with many users.
        """
        return UserController.get_all()

    @bp.arguments(UserSchema)
    @bp.response(201)
    def post(self, data):
        """
        Register a new user account.

        This endpoint handles user registration by creating a new user
        account with hashed password.

        Args:
            data (dict): Request body validated by UserSchema:
                - username (str): Desired username
                - email (str): Email address
                - password (str): Plain-text password

        Returns:
            None (HTTP 201 Created on success)

        Status Codes:
            201: User successfully created
            409: Username or email already registered
            422: Validation error (invalid email format, etc.)
            500: Internal server error

        Example Request:
            POST /api/v1/users
            Content-Type: application/json

            {
                "username": "newuser",
                "email": "new@example.com",
                "password": "securepass123"
            }

        Example Response:
            HTTP/1.1 201 Created

        Validation:
            - Username: Required, max 20 characters, must be unique
            - Email: Required, valid email format, max 120 characters, unique
            - Password: Required, will be hashed before storage

        Security:
            - Password is automatically hashed using bcrypt
            - No authentication required (public registration)
            - Password never returned in response

        Note:
            Consider adding email verification or CAPTCHA for production.
        """
        return UserController.create(data)


@bp.route("/users/<user_id>")
class UserById(MethodView):
    """
    Individual user endpoint.

    This class-based view handles operations on individual users
    identified by their unique ID.

    Endpoints:
        GET /api/v1/users/<user_id> - Get user by ID
    """

    @bp.response(200, UserSchema)
    def get(self, user_id):
        """
        Retrieve a specific user by their ID.

        This endpoint returns details for a single user identified
        by their unique ID.

        Args:
            user_id (int): The unique identifier of the user (URL parameter)

        Returns:
            dict: User object (excludes password):
                {
                    "id": 1,
                    "username": "johndoe",
                    "email": "john@example.com"
                }

        Status Codes:
            200: User found and returned
            404: User not found
            500: Internal server error

        Example Request:
            GET /api/v1/users/1
            Accept: application/json

        Example Response:
            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "id": 1,
                "username": "johndoe",
                "email": "john@example.com"
            }

        Security:
            - No authentication required (consider adding)
            - Password is excluded from response
            - May expose user email (consider privacy)

        Note:
            Consider adding authorization to prevent information disclosure.
        """
        return UserController.get_by_id(user_id)


@bp.route("/users/account")
class UserAccount(MethodView):
    """
    Authenticated user account endpoint.

    This class-based view handles operations on the authenticated
    user's own account.

    Endpoints:
        DELETE /api/v1/users/account - Delete own account (requires JWT)
    """

    @jwt_required()
    @bp.response(204)
    def delete(self):
        """
        Delete the authenticated user's account.

        This protected endpoint allows authenticated users to delete
        their own account. The user ID is extracted from the JWT token.

        Args:
            None (uses JWT token identity)

        Returns:
            None (HTTP 204 No Content on success)

        Status Codes:
            204: Account successfully deleted
            401: Unauthorized (missing or invalid JWT token)
            404: User not found
            500: Internal server error

        Example Request:
            DELETE /api/v1/users/account
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

        Example Response:
            HTTP/1.1 204 No Content

        Authorization:
            - Requires valid JWT token in Authorization header
            - User can only delete their own account
            - Cannot delete other users' accounts

        Cascade Effects:
            - All tasks owned by user are also deleted
            - Deletion is permanent and cannot be undone

        Security:
            - JWT token required
            - User ID from token (not from request body)
            - Prevents unauthorized account deletion

        Note:
            This is a destructive operation. Consider adding:
            - Confirmation requirement
            - Soft delete option
            - Account recovery period
        """
        return UserController.delete()
