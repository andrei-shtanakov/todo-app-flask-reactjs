"""
Authentication Routes Module

This module defines RESTful API endpoints for user authentication operations
including sign-in and JWT token generation.
"""

from flask_smorest import Blueprint
from flask.views import MethodView

from flaskr.controllers.auth_controller import AuthController
from flaskr.schemas.schema import SignInSchema

# Create authentication blueprint
bp = Blueprint("auth", __name__)


@bp.route("/auth/sign-in")
class SignIn(MethodView):
    """
    Authentication endpoint for user sign-in.

    This class-based view handles user authentication by accepting
    credentials and returning a JWT access token.

    Endpoints:
        POST /api/v1/auth/sign-in - Authenticate user and get JWT token
    """

    @bp.arguments(SignInSchema)
    @bp.response(200)
    def post(self, data):
        """
        Authenticate user and generate JWT access token.

        This endpoint validates user credentials (email and password) and
        returns a JWT access token for subsequent authenticated requests.

        Args:
            data (dict): Request body validated by SignInSchema:
                - email (str): User's email address
                - password (str): User's plain-text password

        Returns:
            dict: Response body containing JWT token:
                {
                    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
                }

        Status Codes:
            200: Successful authentication, returns JWT token
            401: Invalid credentials (email not found or password incorrect)
            500: Internal server error

        Example Request:
            POST /api/v1/auth/sign-in
            Content-Type: application/json

            {
                "email": "user@example.com",
                "password": "mypassword123"
            }

        Example Response:
            HTTP/1.1 200 OK
            Content-Type: application/json

            {
                "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
            }

        Security:
            - Passwords verified using constant-time comparison
            - JWT tokens expire based on application configuration
            - Failed attempts don't reveal if email exists

        Note:
            The returned JWT token should be included in the Authorization
            header for subsequent authenticated requests:
            Authorization: Bearer <token>
        """
        return AuthController.sign_in(data)
