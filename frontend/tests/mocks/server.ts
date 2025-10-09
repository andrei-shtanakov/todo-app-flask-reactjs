/**
 * Mock Service Worker (MSW) Server Setup
 * Intercepts API requests during testing
 */

import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Create MSW server with default handlers
export const server = setupServer(...handlers);

