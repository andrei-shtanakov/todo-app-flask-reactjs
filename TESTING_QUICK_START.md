# Testing Quick Start Guide

Get up and running with the testing suite in minutes.

## Prerequisites

- Python 3.13+ (backend)
- Node.js 20+ (frontend)
- Git

## Setup

### 1. Backend Testing Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Verify installation
pytest --version
```

### 2. Frontend Testing Setup

```bash
cd frontend

# Install dependencies
npm install

# Install Playwright browsers (for E2E tests)
npx playwright install

# Verify installation
npm test -- --version
```

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=flaskr --cov-report=html

# Run only unit tests
pytest tests/unit/ -v

# Run only integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/unit/test_utils.py -v

# Run tests matching pattern
pytest -k "password" -v

# View coverage report
open htmlcov/index.html
```

### Frontend Tests

```bash
cd frontend

# Run all unit/integration tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage
npm run test:coverage

# Run with UI
npm run test:ui

# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui

# Run E2E tests in debug mode
npm run test:e2e:debug

# View coverage report
open coverage/index.html
```

## Test Examples

### Backend: Testing a Controller

```python
# tests/unit/controllers/test_auth_controller.py
import pytest
from unittest.mock import patch
from flaskr.controllers.auth_controller import AuthController

@pytest.mark.unit
@pytest.mark.auth
def test_sign_in_success(test_user, db_session):
    """Test successful sign in."""
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    result = AuthController.sign_in(data)
    
    assert "token" in result
    assert result["token"] is not None
```

### Backend: Testing an API Endpoint

```python
# tests/integration/routes/test_auth_routes.py
import pytest

@pytest.mark.integration
def test_sign_in_endpoint(client, test_user):
    """Test sign in API endpoint."""
    response = client.post('/api/v1/auth/sign-in', json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
```

### Frontend: Testing a Component

```typescript
// src/components/ui/__tests__/button.test.tsx
import { describe, it, expect } from 'vitest';
import { renderWithProviders, screen } from '@/tests/helpers/test-utils';
import { Button } from '../button';

describe('Button', () => {
  it('renders with text', () => {
    renderWithProviders(<Button>Click me</Button>);
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });
});
```

### Frontend: Testing API Calls

```typescript
// src/services/api/__tests__/tasks.test.ts
import { describe, it, expect } from 'vitest';
import { getTasksOnUserAPI } from '../tasks';

describe('Tasks API', () => {
  it('fetches user tasks', async () => {
    const tasks = await getTasksOnUserAPI();
    
    expect(tasks).toBeDefined();
    expect(Array.isArray(tasks)).toBe(true);
  });
});
```

### E2E: Testing User Flow

```typescript
// e2e/tasks.spec.ts
import { test, expect } from '@playwright/test';

test('user can create a task', async ({ page }) => {
  // Sign in
  await page.goto('/');
  await page.getByPlaceholder(/email/i).fill('test@example.com');
  await page.getByPlaceholder(/password/i).fill('password123');
  await page.getByRole('button', { name: /sign in/i }).click();
  
  // Create task
  await page.getByRole('button', { name: /create task/i }).click();
  await page.getByPlaceholder(/title/i).fill('New Task');
  await page.getByPlaceholder(/content/i).fill('Task content');
  await page.getByRole('button', { name: /save/i }).click();
  
  // Verify task created
  await expect(page.getByText('New Task')).toBeVisible();
});
```

## Continuous Integration

The test suite runs automatically on:

- Push to any branch
- Pull request to main/develop

### View CI Results

1. Go to GitHub Actions tab
2. Click on latest workflow run
3. View test results and coverage reports

### Required Checks

Before merging to main:
- ✅ All backend tests pass
- ✅ All frontend tests pass
- ✅ All E2E tests pass
- ✅ Code coverage ≥ 70%

## Common Issues

### Backend: Import Errors

**Problem:** `ModuleNotFoundError: No module named 'flaskr'`

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend
# Ensure virtual environment is activated
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements-dev.txt
```

### Frontend: MSW Warnings

**Problem:** `[MSW] Warning: captured a request without a matching request handler`

**Solution:** Add handler to `tests/mocks/handlers.ts`:
```typescript
http.get('http://localhost:5000/api/v1/your-endpoint', () => {
  return HttpResponse.json({ data: 'mock response' });
})
```

### E2E: Browser Not Found

**Problem:** `browserType.launch: Executable doesn't exist`

**Solution:**
```bash
cd frontend
npx playwright install chromium firefox
```

### Coverage Not 70%

**Problem:** Tests pass but coverage check fails

**Solution:**
1. Run coverage report: `pytest --cov=flaskr --cov-report=html`
2. Open `htmlcov/index.html` to see uncovered lines
3. Write tests for uncovered code
4. Focus on critical paths first

## Next Steps

1. **Read the full strategy:** See `TESTING_STRATEGY.md`
2. **Explore examples:** Check `tests/` directories for examples
3. **Write your first test:** Start with a simple unit test
4. **Run tests locally:** Make sure they pass before pushing
5. **Check coverage:** Aim for 70%+ coverage

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [MSW Documentation](https://mswjs.io/)

## Getting Help

- Check test examples in `tests/` directories
- Read test fixture documentation in `conftest.py`
- Review existing tests for patterns
- Ask team for code review

---

Happy Testing! 🎉





