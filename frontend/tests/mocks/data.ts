/**
 * Mock Data for Testing
 * Provides sample data for API responses
 */

import { Task } from '@/types/types';

// Authentication Mock Data
export const mockAuthResponse = {
  token: 'mock-jwt-token-123456789',
};

// Task Mock Data
export const mockTasks: Task[] = [
  {
    id: 1,
    title: 'Complete project documentation',
    content: 'Write comprehensive documentation for the new feature',
    status: 'PENDING',
    tag_name: 'Work',
    created_at: '2024-10-01T10:00:00Z',
  },
  {
    id: 2,
    title: 'Review pull requests',
    content: 'Review and approve pending PRs from the team',
    status: 'IN_PROGRESS',
    tag_name: 'Work',
    created_at: '2024-10-02T14:30:00Z',
  },
  {
    id: 3,
    title: 'Buy groceries',
    content: 'Milk, eggs, bread, and vegetables',
    status: 'PENDING',
    tag_name: 'Personal',
    created_at: '2024-10-03T09:15:00Z',
  },
  {
    id: 4,
    title: 'Gym workout',
    content: 'Upper body strength training',
    status: 'COMPLETED',
    tag_name: 'Health',
    created_at: '2024-10-04T06:00:00Z',
  },
];

// Tag Mock Data
export const mockTags = [
  {
    id: 1,
    name: 'Work',
    color: '#3b82f6',
  },
  {
    id: 2,
    name: 'Personal',
    color: '#10b981',
  },
  {
    id: 3,
    name: 'Health',
    color: '#f59e0b',
  },
  {
    id: 4,
    name: 'Learning',
    color: '#8b5cf6',
  },
];

// User Mock Data
export const mockUser = {
  id: 1,
  email: 'test@example.com',
  first_name: 'Test',
  last_name: 'User',
  created_at: '2024-01-01T00:00:00Z',
};

// Factory Functions for Dynamic Mock Data
export const createMockTask = (overrides?: Partial<Task>): Task => ({
  id: Math.floor(Math.random() * 1000),
  title: 'Test Task',
  content: 'Test task content',
  status: 'PENDING',
  tag_name: 'Work',
  created_at: new Date().toISOString(),
  ...overrides,
});

export const createMockTasks = (count: number): Task[] => {
  return Array.from({ length: count }, (_, i) =>
    createMockTask({
      id: i + 1,
      title: `Task ${i + 1}`,
    })
  );
};



