"""
Root conftest.py - Shared fixtures for all tests

This module provides pytest fixtures for testing Flask applications.
All imports are at module level for better performance and maintainability.
"""

from typing import Generator, Dict
import pytest
from flask import Flask
from flask.testing import FlaskClient, FlaskCliRunner
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import Session, sessionmaker

from flaskr import create_app
from flaskr.db import db as _db
from flaskr.models.user_model import UserModel
from flaskr.models.tag_model import TagModel
from flaskr.models.task_model import TaskModel, TaskStatus
from flaskr.utils import generate_password
from config import TestConfig


# =============================================================================
# CORE FIXTURES - Application & Database
# =============================================================================

@pytest.fixture(scope='function')
def flask_app() -> Generator[Flask, None, None]:
    """
    Create and configure a Flask application for testing.
    
    Scope: function - fresh app instance per test for complete isolation
    
    Yields:
        Flask: Configured Flask application instance
    """
    app = create_app(test_config=TestConfig)
    
    # Create application context
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    # Cleanup
    ctx.pop()


@pytest.fixture(scope='function')
def database(flask_app: Flask) -> Generator:
    """
    Create database and tables for testing.
    
    Scope: function - fresh database per test ensures complete isolation
    
    Args:
        flask_app: Flask application instance
        
    Yields:
        SQLAlchemy db instance
    """
    _db.create_all()
    yield _db
    _db.drop_all()
    _db.session.remove()


@pytest.fixture(scope='function')
def database_session(database) -> Generator[Session, None, None]:
    """
    Create a new database session for each test with automatic rollback.
    
    This fixture ensures test isolation by rolling back all changes after each test.
    
    Scope: function - new session for each test
    
    Args:
        database: Database instance from database fixture
        
    Yields:
        Session: SQLAlchemy session for database operations
    """
    # Create a new connection and transaction
    connection = database.engine.connect()
    transaction = connection.begin()
    
    # Create a new session bound to the connection
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()
    
    # Temporarily replace the global session
    old_session = database.session
    database.session = session
    
    yield session
    
    # Cleanup: rollback transaction and close connection
    session.close()
    transaction.rollback()
    connection.close()
    database.session = old_session


@pytest.fixture(scope='function')
def client(flask_app: Flask, database_session: Session) -> FlaskClient:
    """
    Create a test client for making HTTP requests.
    
    Args:
        flask_app: Flask application instance
        database_session: Database session (ensures db is set up)
    
    Returns:
        FlaskClient: Test client for HTTP requests
        
    Usage:
        def test_example(client):
            response = client.get('/api/v1/tasks')
            assert response.status_code == 200
    """
    return flask_app.test_client()


@pytest.fixture(scope='function')
def runner(flask_app: Flask) -> FlaskCliRunner:
    """
    Create a CLI runner for testing Flask commands.
    
    Args:
        flask_app: Flask application instance
        
    Returns:
        FlaskCliRunner: CLI runner for testing commands
    """
    return flask_app.test_cli_runner()


# =============================================================================
# AUTHENTICATION FIXTURES
# =============================================================================

@pytest.fixture(scope='function')
def auth_headers(client: FlaskClient, database_session: Session, test_user: UserModel) -> Dict[str, str]:
    """
    Generate authentication headers with a valid JWT token.
    
    Args:
        client: Test client (unused but ensures setup)
        database_session: Database session (unused but ensures setup)
        test_user: Test user instance to create token for
    
    Returns:
        dict: Headers dictionary with Authorization Bearer token
        
    Usage:
        def test_protected_route(client, auth_headers):
            response = client.get('/api/v1/tasks/user', headers=auth_headers)
            assert response.status_code == 200
    """
    # Create access token for test user
    token = create_access_token(identity=str(test_user.id))
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


# =============================================================================
# ENTITY FIXTURES - Users, Tags, Tasks
# =============================================================================

@pytest.fixture(scope='function')
def test_user(database_session: Session) -> UserModel:
    """
    Create a test user in the database.
    
    Args:
        database_session: Database session for operations
    
    Returns:
        UserModel: Test user instance with default credentials
        
    Default credentials:
        - username: testuser
        - email: test@example.com
        - password: password123
    """
    user = UserModel(
        username="testuser",
        email="test@example.com",
        password=generate_password("password123")
    )
    
    database_session.add(user)
    database_session.commit()
    database_session.refresh(user)
    
    return user


@pytest.fixture(scope='function')
def another_user(database_session: Session) -> UserModel:
    """
    Create a second test user for isolation testing.
    
    Used to test user data isolation and permission scenarios.
    
    Args:
        database_session: Database session for operations
    
    Returns:
        UserModel: Another test user instance
        
    Default credentials:
        - username: anotheruser
        - email: another@example.com
        - password: password456
    """
    user = UserModel(
        username="anotheruser",
        email="another@example.com",
        password=generate_password("password456")
    )
    
    database_session.add(user)
    database_session.commit()
    database_session.refresh(user)
    
    return user


@pytest.fixture(scope='function')
def test_tag(database_session: Session) -> TagModel:
    """
    Create a test tag in the database.
    
    Args:
        database_session: Database session for operations
    
    Returns:
        TagModel: Test tag instance
        
    Default values:
        - name: Work
    """
    tag = TagModel(
        name="Work"
    )
    
    database_session.add(tag)
    database_session.commit()
    database_session.refresh(tag)
    
    return tag


@pytest.fixture(scope='function')
def test_task(database_session: Session, test_user: UserModel, test_tag: TagModel) -> TaskModel:
    """
    Create a test task in the database.
    
    Args:
        database_session: Database session for operations
        test_user: User who owns the task
        test_tag: Tag associated with the task
    
    Returns:
        TaskModel: Test task instance
        
    Default values:
        - title: Test Task
        - content: Test task content
        - status: PENDING
    """
    task = TaskModel(
        title="Test Task",
        content="Test task content",
        status=TaskStatus.PENDING,
        user_id=test_user.id,
        tag_id=test_tag.id
    )
    
    database_session.add(task)
    database_session.commit()
    database_session.refresh(task)
    
    return task


@pytest.fixture(scope='function')
def multiple_tasks(database_session: Session, test_user: UserModel, test_tag: TagModel) -> list[TaskModel]:
    """
    Create multiple test tasks with different statuses.
    
    Args:
        database_session: Database session for operations
        test_user: User who owns the tasks
        test_tag: Tag associated with the tasks
    
    Returns:
        list[TaskModel]: List of test task instances with different statuses
        
    Creates 3 tasks:
        1. Pending Task (PENDING)
        2. In Progress Task (IN_PROGRESS)
        3. Completed Task (COMPLETED)
    """
    tasks = [
        TaskModel(
            title="Pending Task",
            content="Task with pending status",
            status=TaskStatus.PENDING,
            user_id=test_user.id,
            tag_id=test_tag.id
        ),
        TaskModel(
            title="In Progress Task",
            content="Task currently in progress",
            status=TaskStatus.IN_PROGRESS,
            user_id=test_user.id,
            tag_id=test_tag.id
        ),
        TaskModel(
            title="Completed Task",
            content="Task that is completed",
            status=TaskStatus.COMPLETED,
            user_id=test_user.id,
            tag_id=test_tag.id
        ),
    ]
    
    # Use add_all for better performance
    database_session.add_all(tasks)
    database_session.commit()
    
    # Refresh all tasks
    for task in tasks:
        database_session.refresh(task)
    
    return tasks


# =============================================================================
# FACTORY FIXTURES - For Flexible Test Data Creation
# =============================================================================

@pytest.fixture(scope='function')
def user_factory(database_session: Session):
    """
    Factory fixture for creating test users with custom data.
    
    Args:
        database_session: Database session for operations
        
    Returns:
        Callable: Function to create users with custom attributes
        
    Usage:
        def test_example(user_factory):
            user1 = user_factory(username="user1", email="custom@example.com")
            user2 = user_factory(username="user2", email="another@example.com")
    """
    def _create_user(
        username: str = "factoryuser",
        email: str = "factory@example.com",
        password: str = "password123"
    ) -> UserModel:
        """Create a user with custom attributes."""
        user = UserModel(
            username=username,
            email=email,
            password=generate_password(password)
        )
        database_session.add(user)
        database_session.commit()
        database_session.refresh(user)
        return user
    
    return _create_user


@pytest.fixture(scope='function')
def tag_factory(database_session: Session):
    """
    Factory fixture for creating test tags with custom data.
    
    Args:
        database_session: Database session for operations
        
    Returns:
        Callable: Function to create tags with custom attributes
        
    Usage:
        def test_example(tag_factory):
            tag1 = tag_factory(name="Personal")
            tag2 = tag_factory(name="Urgent")
    """
    def _create_tag(
        name: str = "Default Tag"
    ) -> TagModel:
        """Create a tag with custom attributes."""
        tag = TagModel(
            name=name
        )
        database_session.add(tag)
        database_session.commit()
        database_session.refresh(tag)
        return tag
    
    return _create_tag


@pytest.fixture(scope='function')
def task_factory(database_session: Session):
    """
    Factory fixture for creating test tasks with custom data.
    
    Args:
        database_session: Database session for operations
        
    Returns:
        Callable: Function to create tasks with custom attributes
        
    Usage:
        def test_example(task_factory, test_user, test_tag):
            task1 = task_factory(
                user_id=test_user.id,
                tag_id=test_tag.id,
                title="Custom Task"
            )
            task2 = task_factory(
                user_id=test_user.id,
                tag_id=test_tag.id,
                status=TaskStatus.COMPLETED
            )
    """
    def _create_task(
        user_id: int,
        tag_id: int,
        title: str = "Default Task",
        content: str = "Default task content",
        status: TaskStatus = TaskStatus.PENDING
    ) -> TaskModel:
        """Create a task with custom attributes."""
        task = TaskModel(
            title=title,
            content=content,
            status=status,
            user_id=user_id,
            tag_id=tag_id
        )
        database_session.add(task)
        database_session.commit()
        database_session.refresh(task)
        return task
    
    return _create_task


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================

def pytest_configure(config):
    """
    Register custom pytest markers for test categorization.
    
    Markers allow filtering and organizing tests by category:
    - pytest -m unit        # Run only unit tests
    - pytest -m integration # Run only integration tests
    - pytest -m "not slow"  # Skip slow tests
    """
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "auth: mark test as authentication related"
    )
    config.addinivalue_line(
        "markers", "tasks: mark test as task management related"
    )
    config.addinivalue_line(
        "markers", "tags: mark test as tag related"
    )
    config.addinivalue_line(
        "markers", "users: mark test as user related"
    )
