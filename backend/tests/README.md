# Backend Tests

This directory contains all backend tests for the Flask Todo App.

## Quick Start

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=flaskr --cov-report=html

# Run specific test category
pytest tests/unit/           # Unit tests only
pytest tests/integration/    # Integration tests only

# Run tests by marker
pytest -m unit              # All unit tests
pytest -m integration       # All integration tests
pytest -m "not slow"        # Exclude slow tests
```

## Directory Structure

```
tests/
├── conftest.py                 # Shared fixtures (app, db, client, auth_headers)
├── unit/                       # Unit tests (isolated, mocked dependencies)
│   ├── controllers/           
│   ├── models/
│   ├── schemas/
│   └── utils/
└── integration/                # Integration tests (real DB, API endpoints)
    ├── routes/
    ├── db/
    └── flows/
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.unit` - Unit tests (fast, isolated)
- `@pytest.mark.integration` - Integration tests (slower, real DB)
- `@pytest.mark.slow` - Tests that take >1 second
- `@pytest.mark.auth` - Authentication-related tests
- `@pytest.mark.tasks` - Task management tests
- `@pytest.mark.tags` - Tag-related tests
- `@pytest.mark.users` - User-related tests

## Writing Tests

### Unit Test Example

```python
import pytest
from unittest.mock import patch

@pytest.mark.unit
@pytest.mark.tasks
def test_create_task(mock_db_session):
    """Test task creation with mocked database."""
    # Your test here
```

### Integration Test Example

```python
import pytest

@pytest.mark.integration
@pytest.mark.tasks
def test_create_task_api(client, auth_headers, test_tag):
    """Test task creation via API endpoint."""
    response = client.post(
        '/api/v1/tasks',
        json={
            "title": "Test Task",
            "content": "Content",
            "status": "PENDING",
            "tag_id": test_tag.id
        },
        headers=auth_headers
    )
    
    assert response.status_code == 201
```

## Available Fixtures

See `conftest.py` for all available fixtures:

- `app` - Flask application instance
- `db` - Database instance
- `db_session` - Database session with automatic rollback
- `client` - Test client for making requests
- `auth_headers` - Authentication headers with JWT token
- `test_user` - Test user in database
- `test_tag` - Test tag in database
- `test_task` - Test task in database
- `multiple_tasks` - Multiple tasks with different statuses
- `another_user` - Second user for isolation testing

## Coverage

Target coverage: 70% overall

View coverage report:
```bash
pytest --cov=flaskr --cov-report=html
open htmlcov/index.html
```

## Tips

1. **Use appropriate markers** for test categorization
2. **Keep unit tests fast** - use mocks for external dependencies
3. **Integration tests should be realistic** - use real database
4. **Clean up after yourself** - fixtures handle this automatically
5. **Test edge cases** - empty inputs, non-existent IDs, unauthorized access
6. **Use descriptive test names** - `test_<action>_<expected_result>`




