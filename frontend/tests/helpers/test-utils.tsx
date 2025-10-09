/**
 * Custom Render Function with Providers
 * Wraps components with necessary context providers for testing
 */

import { render, RenderOptions } from '@testing-library/react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter } from 'react-router-dom';
import { ReactElement, ReactNode } from 'react';

/**
 * Creates a fresh QueryClient for each test
 * Disables retries and caching for predictable tests
 */
export const createTestQueryClient = () =>
  new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        gcTime: 0,
        staleTime: 0,
      },
      mutations: {
        retry: false,
      },
    },
    logger: {
      log: console.log,
      warn: console.warn,
      error: () => {}, // Suppress error logs in tests
    },
  });

interface AllProvidersProps {
  children: ReactNode;
  queryClient?: QueryClient;
}

/**
 * Wrapper component with all necessary providers
 */
export const AllProviders = ({
  children,
  queryClient = createTestQueryClient(),
}: AllProvidersProps) => {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{children}</BrowserRouter>
    </QueryClientProvider>
  );
};

interface CustomRenderOptions extends Omit<RenderOptions, 'wrapper'> {
  queryClient?: QueryClient;
  initialRoute?: string;
}

/**
 * Custom render function that wraps components with providers
 * 
 * @example
 * const { getByText } = renderWithProviders(<MyComponent />);
 * 
 * @example With custom query client
 * const queryClient = createTestQueryClient();
 * const { getByText } = renderWithProviders(<MyComponent />, { queryClient });
 */
export const renderWithProviders = (
  ui: ReactElement,
  options?: CustomRenderOptions
) => {
  const { queryClient, initialRoute, ...renderOptions } = options || {};

  // Set initial route if provided
  if (initialRoute) {
    window.history.pushState({}, 'Test page', initialRoute);
  }

  const Wrapper = ({ children }: { children: ReactNode }) => (
    <AllProviders queryClient={queryClient}>{children}</AllProviders>
  );

  return {
    ...render(ui, { wrapper: Wrapper, ...renderOptions }),
    queryClient: queryClient || createTestQueryClient(),
  };
};

/**
 * Wait for loading states to complete
 * Useful for components that show loading skeletons
 */
export const waitForLoadingToFinish = () =>
  new Promise((resolve) => setTimeout(resolve, 0));

// Re-export everything from React Testing Library
export * from '@testing-library/react';
export { userEvent } from '@testing-library/user-event';

