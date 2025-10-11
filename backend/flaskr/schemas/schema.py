"""
Schema Module

This module defines extended Marshmallow schemas that include relationships
and additional fields for complex API responses. These schemas inherit from
plain schemas and add nested relationships or computed fields.
"""

from marshmallow import fields

from flaskr.schemas.plain_schema import (
    PlainSignInSchema,
    PlainTagSchema,
    PlainTaskSchema,
    PlainUserSchema,
)


class UserSchema(PlainUserSchema):
    """
    Extended user schema with relationships.

    This schema extends PlainUserSchema and can include nested relationships
    such as user's tasks. Currently identical to PlainUserSchema but available
    for future extensions.

    Inherits:
        PlainUserSchema: Base user fields (id, username, email, password)

    Usage:
        >>> user = UserModel(id=1, username="john", email="j@ex.com")
        >>> schema = UserSchema()
        >>> schema.dump(user)
        {'id': 1, 'username': 'john', 'email': 'j@ex.com'}

    Future Extensions:
        - Add nested tasks field to include user's tasks
        - Add computed fields like task_count
        - Add profile information fields

    Example with nested tasks (future):
        >>> class UserSchema(PlainUserSchema):
        ...     tasks = fields.Nested(TaskSchema, many=True, dump_only=True)

    Note:
        Password is excluded from responses (load_only in PlainUserSchema).
    """

    pass


class SignInSchema(PlainSignInSchema):
    """
    Extended sign-in schema.

    This schema extends PlainSignInSchema for authentication requests.
    Currently identical to PlainSignInSchema but available for future
    additions like "remember_me" or "device_id" fields.

    Inherits:
        PlainSignInSchema: Base auth fields (email, password)

    Usage:
        >>> data = {"email": "user@ex.com", "password": "secret"}
        >>> schema = SignInSchema()
        >>> validated = schema.load(data)

    Future Extensions:
        - Add remember_me boolean field
        - Add device_id for multi-device session management
        - Add captcha_token for bot protection

    Note:
        This is the schema used by the /auth/sign-in endpoint.
    """

    pass


class TagSchema(PlainTagSchema):
    """
    Extended tag schema with relationships.

    This schema extends PlainTagSchema and can include nested task
    relationships. Currently identical to PlainTagSchema but available
    for future extensions.

    Inherits:
        PlainTagSchema: Base tag fields (id, name)

    Usage:
        >>> tag = TagModel(id=1, name="Work")
        >>> schema = TagSchema()
        >>> schema.dump(tag)
        {'id': 1, 'name': 'Work'}

    Future Extensions:
        - Add nested tasks field to show all tasks with this tag
        - Add task_count computed field
        - Add tag color or icon fields

    Example with task count (future):
        >>> class TagSchema(PlainTagSchema):
        ...     task_count = fields.Method("get_task_count")
        ...     
        ...     def get_task_count(self, obj):
        ...         return len(obj.tasks)

    Note:
        Tags are global resources shared across all users.
    """

    pass


class TaskSchema(PlainTaskSchema):
    """
    Extended task schema with tag relationship.

    This schema extends PlainTaskSchema and adds tag-related fields:
    - tag_name: For displaying tag name in responses (dump_only)
    - tag_id: For associating task with tag in requests (load_only)

    Inherits:
        PlainTaskSchema: Base task fields (id, title, content, status, created_at)

    Additional Fields:
        tag_name (str): Name of associated tag, read-only (dump_only)
        tag_id (int): ID of tag to associate with task, write-only (load_only)

    Field Mapping:
        - tag_name → tagName (camelCase for frontend)
        - tag_id → tagId (camelCase for frontend)

    Usage - Serialization (dump):
        >>> task = TaskModel(id=1, title="Task", tag=TagModel(name="Work"))
        >>> schema = TaskSchema()
        >>> schema.dump(task)
        {
            'id': 1,
            'title': 'Task',
            'content': '...',
            'status': 'PENDING',
            'createdAt': '2025-01-15T10:30:00Z',
            'tagName': 'Work'
        }

    Usage - Deserialization (load):
        >>> data = {
        ...     "title": "New task",
        ...     "content": "Description",
        ...     "status": "PENDING",
        ...     "tagId": 1
        ... }
        >>> schema.load(data)
        {
            'title': 'New task',
            'content': 'Description',
            'status': 'PENDING',
            'tag_id': 1
        }

    Validation:
        - tag_id must reference existing tag (enforced by database)
        - All PlainTaskSchema validations apply

    Design Pattern:
        This schema demonstrates a common pattern:
        - dump_only field (tag_name) for display in responses
        - load_only field (tag_id) for creating relationships
        - Avoids nested object complexity in requests

    Note:
        tag_name is populated by the controller's JOIN query, not by
        Marshmallow. The controller query must include the tag name.
    """

    tag_name = fields.Str(dump_only=True, data_key="tagName")
    tag_id = fields.Int(required=True, load_only=True, data_key="tagId")


class UpdateTaskSchema(PlainTaskSchema):
    """
    Schema for updating existing tasks.

    This schema is used for task update operations (PUT requests).
    It includes the core task fields but excludes tag_id since
    the current implementation doesn't support changing tags.

    Inherits:
        PlainTaskSchema: Base task fields (id, title, content, status, created_at)

    Fields for Update:
        - title: Updated task title
        - content: Updated task description
        - status: Updated task status

    Not Included:
        - tag_id: Tag cannot be changed via update (design limitation)
        - user_id: User ownership never changes
        - created_at: Timestamp is immutable

    Usage:
        >>> data = {
        ...     "title": "Updated title",
        ...     "content": "Updated description",
        ...     "status": "IN_PROGRESS"
        ... }
        >>> schema = UpdateTaskSchema()
        >>> validated = schema.load(data)

    Validation:
        - All fields required (title, content, status)
        - Status must be valid enum value
        - Length constraints from PlainTaskSchema apply

    Design Limitation:
        Currently, the tag cannot be changed after task creation.
        To support tag updates, add:
        >>> tag_id = fields.Int(load_only=True, data_key="tagId")

    Note:
        This is used by the PUT /api/v1/tasks/<task_id> endpoint.
        Consider creating a PATCH schema for partial updates.
    """

    pass
