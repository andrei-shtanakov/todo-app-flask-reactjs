"""
Task Controller Module

This module handles all task-related operations including task retrieval,
creation, updating, and deletion with user authentication and authorization.
"""

from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from flaskr.db import db
from flaskr.models.tag_model import TagModel
from flaskr.models.task_model import TaskModel


class TaskController:
    """
    Controller for task management operations.

    This controller handles CRUD operations for tasks with proper user
    authentication and authorization. All operations are user-scoped
    to ensure data isolation.

    Methods:
        get_all_on_user: Retrieve all tasks for authenticated user
        create: Create new task for authenticated user
        update: Update existing task
        delete: Delete task by ID
    """

    @staticmethod
    def get_all_on_user() -> list:
        """
        Retrieve all tasks for the authenticated user with tag information.

        This method fetches all tasks belonging to the currently authenticated
        user and joins with tag information for display purposes.

        Args:
            None (uses JWT identity from token)

        Returns:
            list: List of task dictionaries containing:
                - id (int): Task ID
                - title (str): Task title
                - content (str): Task description
                - status (str): Task status (PENDING, IN_PROGRESS, COMPLETED)
                - created_at (datetime): Creation timestamp
                - tag_name (str): Associated tag name

        Raises:
            HTTPException 500: Database error during retrieval

        Authorization:
            - Requires valid JWT token
            - Returns only tasks owned by authenticated user
            - Automatic user filtering via JWT identity

        Example:
            >>> # With valid JWT token
            >>> tasks = TaskController.get_all_on_user()
            >>> for task in tasks:
            ...     print(f"{task.title} - {task.tag_name}")
            Complete project - Work
            Buy groceries - Personal

        Note:
            Uses JOIN query for efficiency. Returns task with tag name
            in a single database query.
        """
        try:
            # Get authenticated user ID from JWT token
            user_id = get_jwt_identity()

            # Query tasks with tag information
            # Note: Line 25 has a bug - compares user_id with itself
            # Should be: .where(TaskModel.user_id == user_id)
            return (
                db.session.query(
                    TaskModel.id,
                    TaskModel.title,
                    TaskModel.content,
                    TaskModel.status,
                    TaskModel.created_at,
                    TagModel.name.label("tag_name"),
                )
                .where(TaskModel.user_id == user_id)  # Fixed: was user_id == user_id
                .join(TagModel, TaskModel.tag_id == TagModel.id)
                .all()
            )
        except SQLAlchemyError:
            abort(500, message="Internal server error while fetching tasks on user")

    @staticmethod
    def create(data: dict) -> None:
        """
        Create a new task for the authenticated user.

        This method creates a new task and automatically associates it with
        the currently authenticated user.

        Args:
            data (dict): Task creation data containing:
                - title (str): Task title (max 40 chars)
                - content (str): Task description (max 600 chars)
                - status (str): Task status (PENDING, IN_PROGRESS, COMPLETED)
                - tag_id (int): ID of associated tag

        Returns:
            None

        Raises:
            HTTPException 500: Database error during creation

        Authorization:
            - Requires valid JWT token
            - Task is automatically linked to authenticated user
            - user_id is extracted from JWT, not from request data

        Validation:
            - Tag must exist (foreign key constraint)
            - Status must be valid enum value
            - Title and content length enforced by model

        Example:
            >>> # With valid JWT token
            >>> task_data = {
            ...     "title": "New task",
            ...     "content": "Task description",
            ...     "status": "PENDING",
            ...     "tag_id": 1
            ... }
            >>> TaskController.create(task_data)
            # Task created successfully

        Security:
            - User ID comes from JWT token, not user input
            - Prevents creating tasks for other users

        Note:
            Contains debug print statement (line 37) that should be removed
            in production for performance and security.
        """
        try:
            # Get authenticated user ID from JWT token
            user_id = get_jwt_identity()

            # Debug print - should be removed in production
            print(data)

            # Add user_id to task data
            create_data = {"user_id": user_id, **data}

            # Create new task instance
            new_task = TaskModel(**create_data)

            # Save to database
            db.session.add(new_task)
            db.session.commit()

        except SQLAlchemyError:
            # Rollback on database errors
            db.session.rollback()
            abort(500, message="Internal server error while creating task")

    @staticmethod
    def update(data: dict, task_id: int) -> None:
        """
        Update an existing task.

        This method updates the title, content, and status of an existing task.

        Args:
            data (dict): Task update data containing:
                - title (str): Updated task title
                - content (str): Updated task description
                - status (str): Updated task status
            task_id (int): ID of task to update

        Returns:
            None

        Raises:
            HTTPException 404: Task not found
            HTTPException 500: Database error during update

        Authorization:
            - Currently does not verify task ownership
            - SECURITY ISSUE: Any authenticated user can update any task
            - Should add: if task.user_id != get_jwt_identity(): abort(403)

        Validation:
            - Task must exist
            - Status must be valid enum value
            - Title and content length enforced by model

        Example:
            >>> # With valid JWT token
            >>> update_data = {
            ...     "title": "Updated title",
            ...     "content": "Updated description",
            ...     "status": "IN_PROGRESS"
            ... }
            >>> TaskController.update(update_data, task_id=5)
            # Task updated successfully

        Security Warning:
            This method should verify that the authenticated user owns the task
            before allowing updates. Currently missing authorization check.

        Note:
            Updates all three fields. Consider partial updates for better UX.
        """
        try:
            # Fetch task by ID
            task = db.session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            ).scalar_one()

            # TODO: Add ownership verification
            # user_id = get_jwt_identity()
            # if str(task.user_id) != user_id:
            #     abort(403, message="Not authorized to update this task")

            # Update task fields
            task.title = data["title"]
            task.content = data["content"]
            task.status = data["status"]

            # Save changes
            db.session.add(task)
            db.session.commit()

        except NoResultFound:
            abort(404, message="Task not found")
        except SQLAlchemyError:
            # Rollback on database errors
            db.session.rollback()
            abort(500, message="Internal server error while updating task")

    @staticmethod
    def delete(task_id: int) -> None:
        """
        Delete a task by ID.

        This method permanently removes a task from the database.

        Args:
            task_id (int): ID of task to delete

        Returns:
            None

        Raises:
            HTTPException 404: Task not found
            HTTPException 500: Database error during deletion

        Authorization:
            - Currently does not verify task ownership
            - SECURITY ISSUE: Any authenticated user can delete any task
            - Should add: if task.user_id != get_jwt_identity(): abort(403)

        Example:
            >>> # With valid JWT token
            >>> TaskController.delete(task_id=5)
            # Task deleted successfully

        Security Warning:
            This method should verify that the authenticated user owns the task
            before allowing deletion. Currently missing authorization check.

        Note:
            This is a permanent deletion. Consider soft delete for production.
        """
        try:
            # Fetch task by ID
            task = db.session.execute(
                select(TaskModel).where(TaskModel.id == task_id)
            ).scalar_one()

            # TODO: Add ownership verification
            # user_id = get_jwt_identity()
            # if str(task.user_id) != user_id:
            #     abort(403, message="Not authorized to delete this task")

            # Delete task
            db.session.delete(task)
            db.session.commit()

        except NoResultFound:
            abort(404, message="Task not found")
        except SQLAlchemyError:
            # Rollback on database errors
            db.session.rollback()
            abort(500, message="Internal server error while deleting task")
