"""
Root conftest.py - Shared fixtures for all tests
"""

import pytest
from flaskr import create_app
from flaskr.db import db as _db
from config import Config


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'test-secret-key-do-not-use-in-production'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'


@pytest.fixture(scope='session')
def app():
    """
    Create and configure a Flask application for testing.
    
    Scope: session - created once per test session
    """
    app = create_app(test_config=TestConfig)
    
    # Create application context
    ctx = app.app_context()
    ctx.push()
    
    yield app
    
    # Cleanup
    ctx.pop()


@pytest.fixture(scope='session')
def db(app):
    """
    Create database and tables for testing.
    
    Scope: session - created once per test session
    """
    _db.create_all()
    yield _db
    _db.drop_all()


@pytest.fixture(scope='function')
def db_session(db):
    """
    Create a new database session for each test.
    Automatically rolls back changes after each test.
    
    Scope: function - new session for each test
    """
    # Start a new transaction
    connection = db.engine.connect()
    transaction = connection.begin()
    
    # Bind session to connection
    session = db.create_scoped_session(
        options={"bind": connection, "binds": {}}
    )
    db.session = session
    
    yield session
    
    # Rollback transaction and close connection
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(app, db_session):
    """
    Create a test client for making HTTP requests.
    
    Usage:
        def test_example(client):
            response = client.get('/api/v1/tasks')
            assert response.status_code == 200
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Create a CLI runner for testing Flask commands.
    """
    return app.test_cli_runner()


@pytest.fixture
def auth_headers(client, db_session, test_user):
    """
    Generate authentication headers with a valid JWT token.
    
    Returns:
        dict: Headers dictionary with Authorization Bearer token
        
    Usage:
        def test_protected_route(client, auth_headers):
            response = client.get('/api/v1/tasks/user', headers=auth_headers)
            assert response.status_code == 200
    """
    from flask_jwt_extended import create_access_token
    
    # Create access token for test user
    token = create_access_token(identity=str(test_user.id))
    
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


@pytest.fixture
def test_user(db_session):
    """
    Create a test user in the database.
    
    Returns:
        UserModel: Test user instance
    """
    from flaskr.models.user_model import UserModel
    from flaskr.utils import generate_password
    
    user = UserModel(
        email="test@example.com",
        password=generate_password("password123"),
        first_name="Test",
        last_name="User"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


@pytest.fixture
def test_tag(db_session, test_user):
    """
    Create a test tag in the database.
    
    Returns:
        TagModel: Test tag instance
    """
    from flaskr.models.tag_model import TagModel
    
    tag = TagModel(
        name="Work",
        color="#3b82f6",
        user_id=test_user.id
    )
    
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    
    return tag


@pytest.fixture
def test_task(db_session, test_user, test_tag):
    """
    Create a test task in the database.
    
    Returns:
        TaskModel: Test task instance
    """
    from flaskr.models.task_model import TaskModel, TaskStatus
    
    task = TaskModel(
        title="Test Task",
        content="Test task content",
        status=TaskStatus.PENDING,
        user_id=test_user.id,
        tag_id=test_tag.id
    )
    
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    
    return task


@pytest.fixture
def multiple_tasks(db_session, test_user, test_tag):
    """
    Create multiple test tasks with different statuses.
    
    Returns:
        list[TaskModel]: List of test task instances
    """
    from flaskr.models.task_model import TaskModel, TaskStatus
    
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
    
    for task in tasks:
        db_session.add(task)
    
    db_session.commit()
    
    for task in tasks:
        db_session.refresh(task)
    
    return tasks


@pytest.fixture
def another_user(db_session):
    """
    Create a second test user for isolation testing.
    
    Returns:
        UserModel: Another test user instance
    """
    from flaskr.models.user_model import UserModel
    from flaskr.utils import generate_password
    
    user = UserModel(
        email="another@example.com",
        password=generate_password("password456"),
        first_name="Another",
        last_name="User"
    )
    
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    return user


# Markers for test categorization
def pytest_configure(config):
    """Register custom markers."""
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



