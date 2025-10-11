"""
Integration tests for Task API routes

Tests complete request/response cycle with database.
"""

import pytest
import json
from flaskr.models.task_model import TaskStatus


@pytest.mark.integration
@pytest.mark.tasks
class TestTaskRoutes:
    """Test task API endpoints with real database."""
    
    def test_get_tasks_user_requires_authentication(self, client):
        """Test that getting user tasks requires authentication."""
        response = client.get('/api/v1/tasks/user')
        
        assert response.status_code == 401
    
    def test_get_tasks_user_returns_user_tasks(self, client, auth_headers, test_task):
        """Test that authenticated user can retrieve their tasks."""
        response = client.get('/api/v1/tasks/user', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]['title'] == test_task.title
    
    def test_get_tasks_user_isolation(self, client, auth_headers, test_task, another_user, test_tag, db_session):
        """Test that users only see their own tasks."""
        from flaskr.models.task_model import TaskModel
        
        # Create task for another user
        other_task = TaskModel(
            title="Other User Task",
            content="Should not be visible",
            status=TaskStatus.PENDING,
            user_id=another_user.id,
            tag_id=test_tag.id
        )
        db_session.add(other_task)
        db_session.commit()
        
        # Request tasks as test_user
        response = client.get('/api/v1/tasks/user', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        
        # Should only see test_user's tasks
        task_titles = [task['title'] for task in data]
        assert test_task.title in task_titles
        assert "Other User Task" not in task_titles
    
    def test_create_task_with_valid_data(self, client, auth_headers, test_tag):
        """Test creating a task with valid data."""
        task_data = {
            "title": "New Task",
            "content": "New task content",
            "status": "PENDING",
            "tag_id": test_tag.id
        }
        
        response = client.post(
            '/api/v1/tasks',
            data=json.dumps(task_data),
            headers=auth_headers
        )
        
        assert response.status_code == 201
    
    def test_create_task_requires_authentication(self, client, test_tag):
        """Test that creating a task requires authentication."""
        task_data = {
            "title": "New Task",
            "content": "Content",
            "status": "PENDING",
            "tag_id": test_tag.id
        }
        
        response = client.post(
            '/api/v1/tasks',
            data=json.dumps(task_data),
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 401
    
    def test_update_task_with_valid_data(self, client, auth_headers, test_task):
        """Test updating a task with valid data."""
        update_data = {
            "title": "Updated Title",
            "content": "Updated content",
            "status": "IN_PROGRESS"
        }
        
        response = client.put(
            f'/api/v1/tasks/{test_task.id}',
            data=json.dumps(update_data),
            headers=auth_headers
        )
        
        assert response.status_code == 200
    
    def test_update_nonexistent_task_returns_404(self, client, auth_headers):
        """Test updating non-existent task returns 404."""
        update_data = {
            "title": "Updated",
            "content": "Content",
            "status": "PENDING"
        }
        
        response = client.put(
            '/api/v1/tasks/99999',
            data=json.dumps(update_data),
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_task_success(self, client, auth_headers, test_task, db_session):
        """Test successfully deleting a task."""
        task_id = test_task.id
        
        response = client.delete(
            f'/api/v1/tasks/{task_id}',
            headers=auth_headers
        )
        
        assert response.status_code == 204
        
        # Verify task was actually deleted
        from flaskr.models.task_model import TaskModel
        from sqlalchemy import select
        
        deleted_task = db_session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        ).scalar_one_or_none()
        
        assert deleted_task is None
    
    def test_delete_nonexistent_task_returns_404(self, client, auth_headers):
        """Test deleting non-existent task returns 404."""
        response = client.delete(
            '/api/v1/tasks/99999',
            headers=auth_headers
        )
        
        assert response.status_code == 404
    
    def test_delete_task_requires_authentication(self, client, test_task):
        """Test that deleting a task requires authentication."""
        response = client.delete(f'/api/v1/tasks/{test_task.id}')
        
        assert response.status_code == 401


@pytest.mark.integration
@pytest.mark.tasks
@pytest.mark.slow
class TestTaskLifecycle:
    """Test complete task lifecycle from creation to deletion."""
    
    def test_full_task_lifecycle(self, client, auth_headers, test_tag, db_session):
        """Test creating, updating, and deleting a task."""
        # 1. Create task
        create_data = {
            "title": "Lifecycle Task",
            "content": "Testing full lifecycle",
            "status": "PENDING",
            "tag_id": test_tag.id
        }
        
        create_response = client.post(
            '/api/v1/tasks',
            data=json.dumps(create_data),
            headers=auth_headers
        )
        assert create_response.status_code == 201
        
        # 2. Get tasks and find the created one
        get_response = client.get('/api/v1/tasks/user', headers=auth_headers)
        assert get_response.status_code == 200
        tasks = get_response.get_json()
        task = next(t for t in tasks if t['title'] == "Lifecycle Task")
        task_id = task['id']
        
        # 3. Update task
        update_data = {
            "title": "Updated Lifecycle Task",
            "content": "Updated content",
            "status": "COMPLETED"
        }
        
        update_response = client.put(
            f'/api/v1/tasks/{task_id}',
            data=json.dumps(update_data),
            headers=auth_headers
        )
        assert update_response.status_code == 200
        
        # 4. Verify update
        get_updated_response = client.get('/api/v1/tasks/user', headers=auth_headers)
        updated_tasks = get_updated_response.get_json()
        updated_task = next(t for t in updated_tasks if t['id'] == task_id)
        assert updated_task['title'] == "Updated Lifecycle Task"
        assert updated_task['status'] == "COMPLETED"
        
        # 5. Delete task
        delete_response = client.delete(
            f'/api/v1/tasks/{task_id}',
            headers=auth_headers
        )
        assert delete_response.status_code == 204
        
        # 6. Verify deletion
        final_get_response = client.get('/api/v1/tasks/user', headers=auth_headers)
        final_tasks = final_get_response.get_json()
        assert not any(t['id'] == task_id for t in final_tasks)




