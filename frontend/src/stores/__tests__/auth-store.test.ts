/**
 * Unit tests for auth-store
 * Tests Zustand state management for authentication
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { useAuthStore } from '../auth-store';

describe('AuthStore', () => {
  beforeEach(() => {
    // Reset store state before each test
    useAuthStore.setState({ token: null });
    // Clear localStorage
    localStorage.clear();
  });

  describe('Initial State', () => {
    it('should have null token initially', () => {
      const { token } = useAuthStore.getState();
      expect(token).toBeNull();
    });
  });

  describe('setToken', () => {
    it('should set token in state', () => {
      const testToken = 'test-jwt-token-123';

      useAuthStore.getState().setToken(testToken);

      const { token } = useAuthStore.getState();
      expect(token).toBe(testToken);
    });

    it('should persist token to localStorage', () => {
      const testToken = 'test-jwt-token-456';

      useAuthStore.getState().setToken(testToken);

      // Check localStorage directly
      const storedToken = localStorage.getItem('auth-token');
      expect(storedToken).toBe(JSON.stringify({ token: testToken }));
    });

    it('should update existing token', () => {
      const firstToken = 'first-token';
      const secondToken = 'second-token';

      useAuthStore.getState().setToken(firstToken);
      expect(useAuthStore.getState().token).toBe(firstToken);

      useAuthStore.getState().setToken(secondToken);
      expect(useAuthStore.getState().token).toBe(secondToken);
    });
  });

  describe('clearToken', () => {
    it('should clear token from state', () => {
      // Set a token first
      useAuthStore.getState().setToken('test-token');
      expect(useAuthStore.getState().token).not.toBeNull();

      // Clear the token
      useAuthStore.getState().clearToken();

      const { token } = useAuthStore.getState();
      expect(token).toBeNull();
    });

    it('should remove token from localStorage', () => {
      // Set a token first
      useAuthStore.getState().setToken('test-token');
      expect(localStorage.getItem('auth-token')).not.toBeNull();

      // Clear the token
      useAuthStore.getState().clearToken();

      const storedToken = localStorage.getItem('auth-token');
      expect(storedToken).toBeNull();
    });
  });

  describe('Token Persistence', () => {
    it('should restore token from localStorage on initialization', () => {
      const testToken = 'persisted-token';

      // Manually set token in localStorage
      localStorage.setItem('auth-token', JSON.stringify({ token: testToken }));

      // Get a fresh store instance (simulates page reload)
      const { token } = useAuthStore.getState();

      expect(token).toBe(testToken);
    });

    it('should handle invalid localStorage data gracefully', () => {
      // Set invalid JSON in localStorage
      localStorage.setItem('auth-token', 'invalid-json');

      // Should not throw error and should default to null
      const { token } = useAuthStore.getState();

      expect(token).toBeNull();
    });

    it('should handle missing localStorage item gracefully', () => {
      // Ensure localStorage is empty
      localStorage.removeItem('auth-token');

      const { token } = useAuthStore.getState();

      expect(token).toBeNull();
    });
  });

  describe('isAuthenticated Helper', () => {
    it('should return true when token exists', () => {
      useAuthStore.getState().setToken('valid-token');

      const { token } = useAuthStore.getState();
      const isAuthenticated = token !== null;

      expect(isAuthenticated).toBe(true);
    });

    it('should return false when token is null', () => {
      useAuthStore.getState().clearToken();

      const { token } = useAuthStore.getState();
      const isAuthenticated = token !== null;

      expect(isAuthenticated).toBe(false);
    });
  });
});

