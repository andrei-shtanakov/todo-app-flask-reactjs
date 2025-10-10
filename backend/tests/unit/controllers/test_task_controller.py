"""
Unit tests for TaskController

Tests business logic without making real database calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from flask_smorest import abort
from flaskr.controllers.task_controller import TaskController
from flaskr.models.task_model import TaskModel, TaskStatus


@pytest.mark.unit
@pytest.mark.tasks
class TestTaskController:
    """Test TaskController methods with mocked dependencies."""
    
    @patch('flaskr.controllers.task_controller.get_jwt_identity')
    @patch('flaskr.controllers.task_controller.db.session')
    def test_get_all_on_user_returns_tasks(self, mock_db_session, mock_get_jwt):
        """Test get_all_on_user returns tasks for authenticated user."""
        # Arrange
        mock_get_jwt.return_value = "1"
        mock_query_result = [
            (1, "Task 1", "Content 1", TaskStatus.PENDING, "2024-01-01", "Work"),
            (2, "Task 2", "Content 2", TaskStatus.COMPLETED, "2024-01-02", "Personal"),
        ]
        mock_db_session.query.return_value.where.return_value.join.return_value.all.return_value = mock_query_result
        
        # Act
        result = TaskController.get_all_on_user()
        
        # Assert
        assert result == mock_query_result
        mock_get_jwt.assert_called_once()
    
    @patch('flaskr.controllers.task_controller.get_jwt_identity')
    @patch('flaskr.controllers.task_controller.db.session')
    def test_create_adds_task_to_session(self, mock_db_session, mock_get_jwt):
        """Test create adds new task to database session."""
        # Arrange
        mock_get_jwt.return_value = "1"
        task_data = {
            "title": "New Task",
            "content": "New content",
            "status": "PENDING",
            "tag_id": 1
        }
        
        # Act
        TaskController.create(task_data)
        
        # Assert
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_get_jwt.assert_called_once()
    
    @patch('flaskr.controllers.task_controller.get_jwt_identity')
    @patch('flaskr.controllers.task_controller.db.session')
    def test_create_rolls_back_on_error(self, mock_db_session, mock_get_jwt):
        """Test create rolls back transaction on database error."""
        # Arrange
        mock_get_jwt.return_value = "1"
        mock_db_session.commit.side_effect = Exception("Database error")
        task_data = {"title": "Task", "content": "Content", "tag_id": 1}
        
        # Act & Assert
        with pytest.raises(Exception):
            TaskController.create(task_data)
        
        mock_db_session.rollback.assert_called_once()
    
    @patch('flaskr.controllers.task_controller.db.session')
    def test_update_modifies_existing_task(self, mock_db_session):
        """Test update modifies task fields correctly."""
        # Arrange
        mock_task = Mock(spec=TaskModel)
        mock_db_session.execute.return_value.scalar_one.return_value = mock_task
        
        update_data = {
            "title": "Updated Title",
            "content": "Updated Content",
            "status": TaskStatus.IN_PROGRESS
        }
        task_id = 1
        
        # Act
        TaskController.update(update_data, task_id)
        
        # Assert
        assert mock_task.title == "Updated Title"
        assert mock_task.content == "Updated Content"
        assert mock_task.status == TaskStatus.IN_PROGRESS
        mock_db_session.add.assert_called_once_with(mock_task)
        mock_db_session.commit.assert_called_once()
    
    @patch('flaskr.controllers.task_controller.db.session')
    def test_delete_removes_task(self, mock_db_session):
        """Test delete removes task from database."""
        # Arrange
        mock_task = Mock(spec=TaskModel)
        mock_db_session.execute.return_value.scalar_one.return_value = mock_task
        task_id = 1
        
        # Act
        TaskController.delete(task_id)
        
        # Assert
        mock_db_session.delete.assert_called_once_with(mock_task)
        mock_db_session.commit.assert_called_once()



