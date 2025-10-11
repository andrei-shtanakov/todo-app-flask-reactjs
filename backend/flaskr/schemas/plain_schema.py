"""
Plain Schema Module

This module defines base Marshmallow schemas for serialization and validation
of request/response data without nested relationships.

These schemas are used as base classes for more complex schemas that may
include nested relationships or additional fields.
"""

from marshmallow import Schema, fields, validate


class PlainUserSchema(Schema):
    """
    Base schema for user serialization and validation.

    This schema handles user data without relationships. It includes
    password handling with load_only to prevent exposure in responses.

    Fields:
        id (int): User ID, read-only (dump_only)
        username (str): Username, required, max 20 chars
        email (str): Email address, required, validated format
        password (str): Password, required, write-only (load_only)

    Usage:
        Serialization (dump):
            >>> user = UserModel(id=1, username="john", email="j@ex.com")
            >>> schema = PlainUserSchema()
            >>> schema.dump(user)
            {'id': 1, 'username': 'john', 'email': 'j@ex.com'}
            # Note: password is excluded

        Deserialization (load):
            >>> data = {"username": "john", "email": "j@ex.com", "password": "pass"}
            >>> schema.load(data)
            {'username': 'john', 'email': 'j@ex.com', 'password': 'pass'}

    Security:
        - password is load_only: never included in API responses
        - email format is validated
        - All fields required by default

    Note:
        This is a plain schema without relationships. For full user schema
        with tasks relationship, see UserSchema in schema.py
    """

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class PlainSignInSchema(Schema):
    """
    Schema for user sign-in/authentication requests.

    This schema validates login credentials without exposing unnecessary
    user information. Used exclusively for authentication endpoints.

    Fields:
        email (str): User's email address, required
        password (str): User's password, required (plain-text in request)

    Usage:
        >>> data = {"email": "user@example.com", "password": "secret"}
        >>> schema = PlainSignInSchema()
        >>> validated = schema.load(data)

    Security:
        - Both fields are required
        - Password is transmitted as plain-text (use HTTPS in production)
        - No sensitive data in response (handled by controller)

    Note:
        This schema is intentionally minimal. JWT token is returned by
        the controller, not defined in the schema.
    """

    email = fields.Str(required=True)
    password = fields.Str(required=True)


class PlainTagSchema(Schema):
    """
    Base schema for tag serialization and validation.

    This schema handles tag data without task relationships. Tags are
    simple labels used to categorize tasks.

    Fields:
        id (int): Tag ID, read-only (dump_only)
        name (str): Tag name, required, max 20 chars

    Usage:
        Serialization (dump):
            >>> tag = TagModel(id=1, name="Work")
            >>> schema = PlainTagSchema()
            >>> schema.dump(tag)
            {'id': 1, 'name': 'Work'}

        Deserialization (load):
            >>> data = {"name": "Personal"}
            >>> schema.load(data)
            {'name': 'Personal'}

    Validation:
        - name is required
        - name uniqueness enforced by database, not schema
        - Maximum 20 characters (enforced by model)

    Note:
        This is a plain schema without relationships. For tags with
        associated tasks, extend this schema with nested fields.
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTaskSchema(Schema):
    """
    Base schema for task serialization and validation.

    This schema handles core task data without user or tag relationships.
    It includes status validation and timestamp handling.

    Fields:
        id (int): Task ID, read-only (dump_only)
        title (str): Task title, required, max 40 chars
        content (str): Task description, required, max 600 chars
        status (str): Task status, required, validated enum
        created_at (datetime): Creation timestamp, read-only (dump_only)

    Status Values:
        - PENDING: Task not started
        - IN_PROGRESS: Task being worked on
        - COMPLETED: Task finished

    Usage:
        Serialization (dump):
            >>> task = TaskModel(id=1, title="Task", status="PENDING")
            >>> schema = PlainTaskSchema()
            >>> schema.dump(task)
            {
                'id': 1,
                'title': 'Task',
                'content': '...',
                'status': 'PENDING',
                'createdAt': '2025-01-15T10:30:00Z'
            }

        Deserialization (load):
            >>> data = {
            ...     "title": "New task",
            ...     "content": "Description",
            ...     "status": "PENDING"
            ... }
            >>> schema.load(data)

    Validation:
        - All fields except id and created_at are required
        - status must be one of: PENDING, IN_PROGRESS, COMPLETED
        - Length constraints enforced by model (title: 40, content: 600)

    Field Mapping:
        - created_at → createdAt (camelCase for frontend)

    Note:
        This is a plain schema. For tasks with tag and user relationships,
        see TaskSchema in schema.py which extends this base schema.
    """

    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    status = fields.Str(
        validate=validate.OneOf(["PENDING", "IN_PROGRESS", "COMPLETED"]),
        required=True
    )
    created_at = fields.DateTime(dump_only=True, data_key="createdAt")
