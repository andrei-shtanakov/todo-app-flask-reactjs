"""
Task Routes Module

This module defines RESTful API endpoints for task management operations
including listing, creating, updating, and deleting tasks with JWT authentication.
"""

from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint
from flask.views import MethodView

from flaskr.controllers.task_controller import TaskController
from flaskr.schemas.schema import TaskSchema, UpdateTaskSchema

# Create tasks blueprint
bp = Blueprint("tasks", __name__)


@bp.route("/tasks")
class Tasks(MethodView):
    """
    Task collection endpoint.

    This class-based view handles task creation. All operations require
    JWT authentication to ensure tasks are properly associated with users.

    Endpoints:
        POST /api/v1/tasks - Create a new task (requires JWT)
    """

    @jwt_required()
    @bp.arguments(TaskSchema)
    @bp.response(201)
    def post(self, data):
        """
        Create a new task for the authenticated user.

        This protected endpoint creates a new task and automatically
        associates it with the authenticated user from the JWT token.

        Args:
            data (dict): Request body validated by TaskSchema:
                - title (str): Task title (max 40 characters)
                - content (str): Task description (max 600 characters)
                - status (str): Task status (PENDING, IN_PROGRESS, COMPLETED)
                - tagId (int): ID of associated tag

        Returns:
            None (HTTP 201 Created on success)

        Status Codes:
            201: Task successfully created
            401: Unauthorized (missing or invalid JWT token)
            422: Validation error (invalid status, missing fields, etc.)
            500: Internal server error

        Example Request:
            POST /api/v1/tasks
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
            Content-Type: application/json

            {
                "title": "Complete documentation",
                "content": "Write comprehensive API documentation",
                "status": "PENDING",
                "tagId": 1
            }

        Example Response:
            HTTP/1.1 201 Created

        Validation:
            - Title: Required, max 40 characters
            - Content: Required, max 600 characters
            - Status: Must be PENDING, IN_PROGRESS, or COMPLETED
            - TagId: Required, must reference existing tag

        Authorization:
            - Requires valid JWT token
            - Task automatically linked to authenticated user
            - User ID from token, not request body

        Security:
            - JWT authentication prevents unauthorized task creation
            - User cannot create tasks for other users
            - Tag must exist (foreign key constraint)

        Note:
            The task is automatically associated with the user from the JWT
            token, ensuring proper ownership and access control.
        """
        return TaskController.create(data)


@bp.route("/tasks/user")
class TasksOnUser(MethodView):
    """
    User-specific task collection endpoint.

    This class-based view retrieves all tasks belonging to the
    authenticated user.

    Endpoints:
        GET /api/v1/tasks/user - Get all tasks for authenticated user (requires JWT)
    """

    @jwt_required()
    @bp.response(200, TaskSchema(many=True))
    def get(self):
        """
        Retrieve all tasks for the authenticated user.

        This protected endpoint returns all tasks owned by the currently
        authenticated user, including associated tag information.

        Args:
            None (uses JWT token identity)

        Returns:
            list[dict]: List of task objects with tag names:
                [
                    {
                        "id": 1,
                        "title": "Complete project",
                        "content": "Finish documentation",
                        "status": "IN_PROGRESS",
                        "createdAt": "2025-01-15T10:30:00Z",
                        "tagName": "Work"
                    },
                    ...
                ]

        Status Codes:
            200: Successfully retrieved tasks
            401: Unauthorized (missing or invalid JWT token)
            500: Internal server error

        Example Request:
            GET /api/v1/tasks/user
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
            Accept: application/json

        Example Response:
            HTTP/1.1 200 OK
            Content-Type: application/json

            [
                {
                    "id": 1,
                    "title": "Write tests",
                    "content": "Add unit tests for controllers",
                    "status": "IN_PROGRESS",
                    "createdAt": "2025-01-15T10:30:00Z",
                    "tagName": "Development"
                },
                {
                    "id": 2,
                    "title": "Review PR",
                    "content": "Review pull request #42",
                    "status": "PENDING",
                    "createdAt": "2025-01-15T14:20:00Z",
                    "tagName": "Code Review"
                }
            ]

        Authorization:
            - Requires valid JWT token
            - Returns only tasks owned by authenticated user
            - Automatic user filtering via JWT identity

        Performance:
            - Uses JOIN query to fetch task with tag in single query
            - Efficient retrieval with proper indexing

        Note:
            Tasks are automatically filtered by user_id from JWT token,
            ensuring proper data isolation between users.
        """
        return TaskController.get_all_on_user()


@bp.route("/tasks/<task_id>")
class TaskById(MethodView):
    """
    Individual task endpoint.

    This class-based view handles operations on individual tasks
    identified by their unique ID. All operations require JWT authentication.

    Endpoints:
        PUT    /api/v1/tasks/<task_id> - Update task (requires JWT)
        DELETE /api/v1/tasks/<task_id> - Delete task (requires JWT)
    """

    @jwt_required()
    @bp.arguments(UpdateTaskSchema)
    @bp.response(200)
    def put(self, data, task_id):
        """
        Update an existing task.

        This protected endpoint updates the title, content, and status
        of an existing task.

        Args:
            data (dict): Request body validated by UpdateTaskSchema:
                - title (str): Updated task title
                - content (str): Updated task description
                - status (str): Updated task status
            task_id (int): ID of task to update (URL parameter)

        Returns:
            None (HTTP 200 OK on success)

        Status Codes:
            200: Task successfully updated
            401: Unauthorized (missing or invalid JWT token)
            404: Task not found
            422: Validation error
            500: Internal server error

        Example Request:
            PUT /api/v1/tasks/5
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
            Content-Type: application/json

            {
                "title": "Updated title",
                "content": "Updated description",
                "status": "COMPLETED"
            }

        Example Response:
            HTTP/1.1 200 OK

        Validation:
            - Title: Required, max 40 characters
            - Content: Required, max 600 characters
            - Status: Must be PENDING, IN_PROGRESS, or COMPLETED

        Authorization:
            - Requires valid JWT token
            - WARNING: Currently does NOT verify task ownership
            - Any authenticated user can update any task

        Security Warning:
            This endpoint has a security issue - it does not verify that
            the authenticated user owns the task. Any authenticated user
            can update any task. This should be fixed by adding:

            if task.user_id != get_jwt_identity():
                abort(403, message="Not authorized")

        Note:
            Updates all three fields. Consider supporting partial updates
            (PATCH method) for better API design.
        """
        return TaskController.update(data, task_id)

    @jwt_required()
    @bp.response(204)
    def delete(self, task_id):
        """
        Delete a task.

        This protected endpoint permanently removes a task from the database.

        Args:
            task_id (int): ID of task to delete (URL parameter)

        Returns:
            None (HTTP 204 No Content on success)

        Status Codes:
            204: Task successfully deleted
            401: Unauthorized (missing or invalid JWT token)
            404: Task not found
            500: Internal server error

        Example Request:
            DELETE /api/v1/tasks/5
            Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...

        Example Response:
            HTTP/1.1 204 No Content

        Authorization:
            - Requires valid JWT token
            - WARNING: Currently does NOT verify task ownership
            - Any authenticated user can delete any task

        Security Warning:
            This endpoint has a security issue - it does not verify that
            the authenticated user owns the task. Any authenticated user
            can delete any task. This should be fixed by adding:

            if task.user_id != get_jwt_identity():
                abort(403, message="Not authorized")

        Cascade Effects:
            - Task is permanently deleted
            - No cascade effects (tasks don't have dependent records)

        Note:
            This is a permanent deletion. Consider implementing soft delete
            for production to allow recovery or maintain audit history.
        """
        return TaskController.delete(task_id)
