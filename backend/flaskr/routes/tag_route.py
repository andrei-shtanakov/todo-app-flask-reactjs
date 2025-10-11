"""
Tag Routes Module

This module defines RESTful API endpoints for tag management operations
including listing available tags and creating new tags.
"""

from flask.views import MethodView
from flask_smorest import Blueprint

from flaskr.controllers.tag_controller import TagController
from flaskr.schemas.schema import TagSchema

# Create tags blueprint
bp = Blueprint("tags", __name__)


@bp.route("/tags")
class Tags(MethodView):
    """
    Tag collection endpoint.

    This class-based view handles operations on the tag collection
    including listing available tags and creating new tags.

    Tags are used to categorize and organize tasks. They are global
    resources shared across all users.

    Endpoints:
        GET  /api/v1/tags - List all available tags
        POST /api/v1/tags - Create a new tag
    """

    @bp.response(200, TagSchema(many=True))
    def get(self):
        """
        Retrieve all available tags.

        This endpoint returns a list of all tags that can be assigned
        to tasks. The list is limited to 15 tags.

        Args:
            None

        Returns:
            list[dict]: List of tag objects:
                [
                    {
                        "id": 1,
                        "name": "Work"
                    },
                    {
                        "id": 2,
                        "name": "Personal"
                    },
                    ...
                ]

        Status Codes:
            200: Successfully retrieved tags
            500: Internal server error

        Example Request:
            GET /api/v1/tags
            Accept: application/json

        Example Response:
            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {"id": 1, "name": "Work"},
                {"id": 2, "name": "Personal"},
                {"id": 3, "name": "Urgent"}
            ]

        Behavior:
            - No authentication required
            - Maximum 15 tags returned
            - Tags are global (not user-specific)
            - Results are not paginated

        Note:
            Consider adding pagination if the number of tags grows beyond 15.
        """
        return TagController.get_all()

    @bp.arguments(TagSchema)
    @bp.response(201)
    def post(self, data):
        """
        Create a new tag.

        This endpoint creates a new tag that can be assigned to tasks.
        Tag names must be unique.

        Args:
            data (dict): Request body validated by TagSchema:
                - name (str): Tag name (max 20 characters, unique)

        Returns:
            None (HTTP 201 Created on success)

        Status Codes:
            201: Tag successfully created
            409: Tag name already exists
            422: Validation error (name too long, etc.)
            500: Internal server error

        Example Request:
            POST /api/v1/tags
            Content-Type: application/json

            {
                "name": "Important"
            }

        Example Response:
            HTTP/1.1 201 Created

        Validation:
            - Name: Required, max 20 characters, must be unique
            - Case-sensitive uniqueness check

        Security:
            - No authentication required (consider adding)
            - Any user can create tags
            - Consider restricting to admin users

        Design Note:
            Tags are currently global across all users. If you need
            user-specific tags, add user_id to the TagModel and update
            the controller logic.

        Note:
            Consider adding tag categories or tag hierarchies for better
            organization in applications with many tags.
        """
        return TagController.create(data)
