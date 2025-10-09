/**
 * E2E Tests for Authentication Flow
 * Tests user sign up, sign in, and logout functionality
 */

import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to home page before each test
    await page.goto('/');
  });

  test('should display landing page with auth tabs', async ({ page }) => {
    // Check for sign in and create account tabs
    await expect(page.getByRole('tab', { name: /sign in/i })).toBeVisible();
    await expect(page.getByRole('tab', { name: /create account/i })).toBeVisible();
  });

  test('should show validation errors for empty sign in form', async ({ page }) => {
    // Click sign in button without filling form
    await page.getByRole('button', { name: /sign in/i }).click();

    // Should show validation errors
    await expect(page.getByText(/email is required/i)).toBeVisible();
    await expect(page.getByText(/password is required/i)).toBeVisible();
  });

  test('should show error for invalid credentials', async ({ page }) => {
    // Fill in invalid credentials
    await page.getByPlaceholder(/email/i).fill('invalid@example.com');
    await page.getByPlaceholder(/password/i).fill('wrongpassword');
    
    // Submit form
    await page.getByRole('button', { name: /sign in/i }).click();

    // Should show error message
    await expect(page.getByText(/incorrect credentials/i)).toBeVisible();
  });

  test('should successfully sign in with valid credentials', async ({ page }) => {
    // Fill in valid credentials (assuming test user exists)
    await page.getByPlaceholder(/email/i).fill('test@example.com');
    await page.getByPlaceholder(/password/i).fill('password123');
    
    // Submit form
    await page.getByRole('button', { name: /sign in/i }).click();

    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Should show dashboard content
    await expect(page.getByText(/my tasks/i)).toBeVisible();
  });

  test('should switch to create account tab', async ({ page }) => {
    // Click create account tab
    await page.getByRole('tab', { name: /create account/i }).click();

    // Should show create account form
    await expect(page.getByPlaceholder(/first name/i)).toBeVisible();
    await expect(page.getByPlaceholder(/last name/i)).toBeVisible();
    await expect(page.getByPlaceholder(/email/i)).toBeVisible();
    await expect(page.getByPlaceholder(/password/i)).toBeVisible();
  });

  test('should show validation errors for empty sign up form', async ({ page }) => {
    // Switch to create account
    await page.getByRole('tab', { name: /create account/i }).click();
    
    // Click create account button without filling form
    await page.getByRole('button', { name: /create account/i }).click();

    // Should show validation errors for all required fields
    await expect(page.getByText(/first name is required/i)).toBeVisible();
    await expect(page.getByText(/last name is required/i)).toBeVisible();
    await expect(page.getByText(/email is required/i)).toBeVisible();
    await expect(page.getByText(/password is required/i)).toBeVisible();
  });

  test('should successfully create account and redirect to dashboard', async ({ page }) => {
    // Generate unique email for test
    const uniqueEmail = `test${Date.now()}@example.com`;

    // Switch to create account
    await page.getByRole('tab', { name: /create account/i }).click();
    
    // Fill in form
    await page.getByPlaceholder(/first name/i).fill('Test');
    await page.getByPlaceholder(/last name/i).fill('User');
    await page.getByPlaceholder(/email/i).fill(uniqueEmail);
    await page.getByPlaceholder(/password/i).fill('password123');
    
    // Submit form
    await page.getByRole('button', { name: /create account/i }).click();

    // Should redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    
    // Should show dashboard content
    await expect(page.getByText(/my tasks/i)).toBeVisible();
  });

  test('should show error when creating account with existing email', async ({ page }) => {
    // Switch to create account
    await page.getByRole('tab', { name: /create account/i }).click();
    
    // Fill in form with existing email
    await page.getByPlaceholder(/first name/i).fill('Test');
    await page.getByPlaceholder(/last name/i).fill('User');
    await page.getByPlaceholder(/email/i).fill('existing@example.com');
    await page.getByPlaceholder(/password/i).fill('password123');
    
    // Submit form
    await page.getByRole('button', { name: /create account/i }).click();

    // Should show error message
    await expect(page.getByText(/email already exists/i)).toBeVisible();
  });

  test('should logout and redirect to home', async ({ page }) => {
    // First, sign in
    await page.getByPlaceholder(/email/i).fill('test@example.com');
    await page.getByPlaceholder(/password/i).fill('password123');
    await page.getByRole('button', { name: /sign in/i }).click();
    
    // Wait for redirect to dashboard
    await expect(page).toHaveURL('/dashboard');

    // Click logout button
    await page.getByRole('button', { name: /logout/i }).click();

    // Should redirect to home
    await expect(page).toHaveURL('/');
    
    // Should show sign in form again
    await expect(page.getByRole('tab', { name: /sign in/i })).toBeVisible();
  });

  test('should persist authentication after page reload', async ({ page }) => {
    // Sign in
    await page.getByPlaceholder(/email/i).fill('test@example.com');
    await page.getByPlaceholder(/password/i).fill('password123');
    await page.getByRole('button', { name: /sign in/i }).click();
    
    // Wait for redirect to dashboard
    await expect(page).toHaveURL('/dashboard');

    // Reload page
    await page.reload();

    // Should still be on dashboard (token persisted)
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText(/my tasks/i)).toBeVisible();
  });

  test('should redirect to login when accessing protected route without auth', async ({ page }) => {
    // Try to access dashboard without authentication
    await page.goto('/dashboard');

    // Should redirect to home/login
    await expect(page).toHaveURL('/');
    
    // Should show sign in form
    await expect(page.getByRole('tab', { name: /sign in/i })).toBeVisible();
  });
});

