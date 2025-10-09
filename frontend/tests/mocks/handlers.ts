/**
 * Mock Service Worker (MSW) Request Handlers
 * Defines API mocks for testing
 */

import { http, HttpResponse } from 'msw';
import { mockTasks, mockTags, mockAuthResponse } from './data';

const API_BASE_URL = 'http://localhost:5000/api/v1';

export const handlers = [
  // ============ Authentication Endpoints ============
  
  http.post(`${API_BASE_URL}/auth/sign-up`, async ({ request }) => {
    const body = await request.json() as any;
    
    // Simulate validation
    if (!body.email || !body.password) {
      return HttpResponse.json(
        { message: 'Email and password are required' },
        { status: 400 }
      );
    }
    
    // Simulate duplicate email
    if (body.email === 'existing@example.com') {
      return HttpResponse.json(
        { message: 'Email already exists' },
        { status: 409 }
      );
    }
    
    return HttpResponse.json(mockAuthResponse, { status: 201 });
  }),
  
  http.post(`${API_BASE_URL}/auth/sign-in`, async ({ request }) => {
    const body = await request.json() as any;
    
    // Simulate incorrect credentials
    if (body.email !== 'test@example.com' || body.password !== 'password123') {
      return HttpResponse.json(
        { message: 'Incorrect credentials' },
        { status: 401 }
      );
    }
    
    return HttpResponse.json(mockAuthResponse, { status: 200 });
  }),
  
  // ============ Task Endpoints ============
  
  http.get(`${API_BASE_URL}/tasks/user`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return HttpResponse.json(
        { message: 'Missing or invalid authorization header' },
        { status: 401 }
      );
    }
    
    return HttpResponse.json(mockTasks, { status: 200 });
  }),
  
  http.post(`${API_BASE_URL}/tasks`, async ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader) {
      return HttpResponse.json(
        { message: 'Missing authorization header' },
        { status: 401 }
      );
    }
    
    const body = await request.json() as any;
    
    // Simulate validation
    if (!body.title || !body.content || !body.tag_id) {
      return HttpResponse.json(
        { message: 'Title, content, and tag_id are required' },
        { status: 400 }
      );
    }
    
    return new HttpResponse(null, { status: 201 });
  }),
  
  http.put(`${API_BASE_URL}/tasks/:id`, async ({ request, params }) => {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader) {
      return HttpResponse.json(
        { message: 'Missing authorization header' },
        { status: 401 }
      );
    }
    
    const { id } = params;
    const body = await request.json() as any;
    
    // Simulate task not found
    if (id === '999') {
      return HttpResponse.json(
        { message: 'Task not found' },
        { status: 404 }
      );
    }
    
    // Simulate validation
    if (!body.title || !body.content || !body.status) {
      return HttpResponse.json(
        { message: 'Title, content, and status are required' },
        { status: 400 }
      );
    }
    
    return new HttpResponse(null, { status: 200 });
  }),
  
  http.delete(`${API_BASE_URL}/tasks/:id`, ({ request, params }) => {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader) {
      return HttpResponse.json(
        { message: 'Missing authorization header' },
        { status: 401 }
      );
    }
    
    const { id } = params;
    
    // Simulate task not found
    if (id === '999') {
      return HttpResponse.json(
        { message: 'Task not found' },
        { status: 404 }
      );
    }
    
    return new HttpResponse(null, { status: 204 });
  }),
  
  // ============ Tag Endpoints ============
  
  http.get(`${API_BASE_URL}/tags/user`, ({ request }) => {
    const authHeader = request.headers.get('Authorization');
    
    if (!authHeader) {
      return HttpResponse.json(
        { message: 'Missing authorization header' },
        { status: 401 }
      );
    }
    
    return HttpResponse.json(mockTags, { status: 200 });
  }),
];

