# Frontend Tests

This directory contains test setup and utilities for the React Todo App.

## Quick Start

```bash
# Install dependencies
npm install

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui

# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npm run test:e2e:ui
```

## Directory Structure

```
src/
├── components/
│   └── ui/
│       └── __tests__/          # Component tests
├── stores/
│   └── __tests__/              # Store tests
├── services/
│   └── api/
│       └── __tests__/          # API integration tests
└── schemas/
    └── __tests__/              # Schema validation tests

tests/
├── setup.ts                    # Global test setup
├── mocks/
│   ├── handlers.ts            # MSW request handlers
│   ├── server.ts              # MSW server setup
│   └── data.ts                # Mock data generators
└── helpers/
    └── test-utils.tsx         # Custom render function

e2e/
└── auth.spec.ts               # E2E tests with Playwright
```

## Writing Tests

### Component Test Example

```typescript
import { describe, it, expect } from 'vitest';
import { renderWithProviders, screen, userEvent } from '@/tests/helpers/test-utils';
import { Button } from './button';

describe('Button', () => {
  it('should render with text', () => {
    renderWithProviders(<Button>Click me</Button>);
    
    expect(screen.getByText('Click me')).toBeInTheDocument();
  });

  it('should call onClick when clicked', async () => {
    const handleClick = vi.fn();
    renderWithProviders(<Button onClick={handleClick}>Click me</Button>);
    
    await userEvent.click(screen.getByText('Click me'));
    
    expect(handleClick).toHaveBeenCalledOnce();
  });
});
```

### Store Test Example

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { useAuthStore } from '../auth-store';

describe('AuthStore', () => {
  beforeEach(() => {
    useAuthStore.setState({ token: null });
    localStorage.clear();
  });

  it('should set token', () => {
    useAuthStore.getState().setToken('test-token');
    
    expect(useAuthStore.getState().token).toBe('test-token');
  });
});
```

### API Integration Test with MSW

```typescript
import { describe, it, expect } from 'vitest';
import { getTasksOnUserAPI } from './tasks';

describe('Task API', () => {
  it('should fetch tasks', async () => {
    // MSW will intercept the request automatically
    const tasks = await getTasksOnUserAPI();
    
    expect(tasks).toHaveLength(4);
    expect(tasks[0].title).toBe('Complete project documentation');
  });
});
```

### E2E Test Example

```typescript
import { test, expect } from '@playwright/test';

test('should sign in successfully', async ({ page }) => {
  await page.goto('/');
  
  await page.getByPlaceholder(/email/i).fill('test@example.com');
  await page.getByPlaceholder(/password/i).fill('password123');
  await page.getByRole('button', { name: /sign in/i }).click();
  
  await expect(page).toHaveURL('/dashboard');
});
```

## Test Utilities

### `renderWithProviders`

Custom render function that wraps components with necessary providers:

```typescript
import { renderWithProviders } from '@/tests/helpers/test-utils';

const { getByText } = renderWithProviders(<MyComponent />);
```

### Mock Service Worker (MSW)

API mocks are automatically applied. To customize:

```typescript
import { server } from '@/tests/mocks/server';
import { http, HttpResponse } from 'msw';

// Override handler for specific test
server.use(
  http.get('http://localhost:5000/api/v1/tasks/user', () => {
    return HttpResponse.json([]);
  })
);
```

## Coverage

Target coverage: 70% overall

View coverage report:
```bash
npm run test:coverage
open coverage/index.html
```

## Tips

1. **Use `renderWithProviders`** for components that need context
2. **MSW mocks are automatic** - just import and call your API functions
3. **Clean up is automatic** - localStorage, MSW, and React state are reset
4. **Use realistic selectors** - `getByRole`, `getByLabelText`, `getByPlaceholder`
5. **Test user behavior** - use `userEvent` instead of `fireEvent`
6. **E2E tests are expensive** - focus on critical user journeys
7. **Use Playwright's auto-wait** - no need for manual waits

## Debugging

### Vitest UI

```bash
npm run test:ui
```

Opens a browser interface to run and debug tests.

### Playwright Debug

```bash
npm run test:e2e:debug
```

Opens Playwright Inspector for step-by-step debugging.

### Debug Single Test

```typescript
import { describe, it, expect } from 'vitest';

it.only('should debug this test', () => {
  // Only this test will run
});
```

