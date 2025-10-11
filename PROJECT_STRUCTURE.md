# TODO App - Project Structure Documentation

## Overview

This is a full-stack TODO application built with **Flask (Python)** on the backend and **React (TypeScript)** on the frontend. The application allows users to create accounts, authenticate, and manage their tasks with tags and different statuses (PENDING, IN_PROGRESS, COMPLETED).

**Architecture Pattern**: MVC (Model-View-Controller) on backend, Component-based architecture on frontend  
**Communication**: REST API with JWT authentication  
**Database**: SQLite with SQLAlchemy ORM

---

## Project Root Structure

```
todo-app-flask-reactjs/
├── backend/          # Flask REST API server
├── frontend/         # React TypeScript client application
├── preview/          # Application screenshots for documentation
└── README.md         # Main project documentation
```

---

## 🐍 BACKEND Directory (`/backend`)

**Purpose**: Provides REST API endpoints for user authentication, task management, and tag operations. Built with Flask following MVC pattern.

**Technology Stack**: Python 3.13+, Flask, SQLAlchemy, Flask-Smorest, JWT, SQLite

### Backend Top-Level Structure

```
backend/
├── flaskr/              # Main application package (MVC structure)
├── migrations/          # Database migration files (Alembic)
├── application.py       # Flask app entry point
├── config.py           # Application configuration (JWT, CORS, Database)
├── seed.py             # Database seeding script for initial tags
├── data.db             # SQLite database file
├── requirements.txt    # Python dependencies list
├── Pipfile             # Pipenv dependency management
├── pyproject.toml      # Modern Python project configuration
└── venv/              # Python virtual environment
```

---

### Backend Directories Explained

#### 📁 `flaskr/` - Main Application Package

**Purpose**: Contains the entire Flask application following MVC pattern. This is the core of the backend where all business logic, data models, and API routes are defined.

**Subdirectories**:

##### `flaskr/models/` - Data Models (M in MVC)
**Purpose**: Defines database table structures using SQLAlchemy ORM.

**Files**:
- `user_model.py` - User entity (id, username, email, password)
- `task_model.py` - Task entity (id, title, content, status, created_at, user_id, tag_id)
- `tag_model.py` - Tag entity (id, name) for categorizing tasks

**Database Relationships**:
- User ↔ Tasks: One-to-Many (one user has many tasks)
- Tag ↔ Tasks: One-to-Many (one tag can be used by many tasks)

##### `flaskr/controllers/` - Business Logic (C in MVC)
**Purpose**: Handles business logic and data processing. Controllers interact with models and process requests from routes.

**Files**:
- `auth_controller.py` - Authentication logic (sign-in, JWT token creation)
- `user_controller.py` - User CRUD operations (create, read, delete users)
- `task_controller.py` - Task CRUD operations (create, read, update, delete tasks)
- `tag_controller.py` - Tag operations (create, list tags)

##### `flaskr/routes/` - API Endpoints (V in MVC - REST API as View)
**Purpose**: Defines REST API endpoints and maps HTTP requests to controller methods.

**Files**:
- `auth_route.py` - `/api/v1/auth/sign-in` (POST - user login)
- `user_route.py` - `/api/v1/users` (GET, POST, DELETE - user management)
- `task_route.py` - `/api/v1/tasks` (GET, POST, PUT, DELETE - task management)
- `tag_route.py` - `/api/v1/tags` (GET, POST - tag management)

##### `flaskr/schemas/` - Data Validation Schemas
**Purpose**: Defines Marshmallow schemas for request/response validation and serialization.

**Files**:
- `plain_schema.py` - Base schemas for all entities
- `schema.py` - Extended schemas with relationships and custom fields

**Validates**:
- Input data format (email validation, required fields)
- Output data serialization (hiding sensitive data like passwords)
- Data transformations (snake_case ↔ camelCase)

##### `flaskr/` - Core Files
**Files**:
- `__init__.py` - Flask app factory, initializes extensions (DB, CORS, JWT, API)
- `db.py` - Database configuration and SQLAlchemy instance
- `extensions.py` - Flask extension instances (Migrate, Api, CORS, JWTManager)
- `utils.py` - Helper functions (password hashing, password verification)

---

#### 📁 `migrations/` - Database Migrations

**Purpose**: Manages database schema changes over time using Flask-Migrate (Alembic). Allows version control for database structure.

**Key Files**:
- `alembic.ini` - Alembic configuration
- `env.py` - Migration environment setup
- `versions/` - Contains timestamped migration scripts

**Migration History**:
1. `f9749b66f5da` - Added tag model
2. `c07d93b5193d` - Added task model
3. `2d35678c07a5` - Added user model
4. `bcd9334a523e` - Added 1:N relationship (users → tasks)
5. `cac5cf55cffa` - Added 1:N relationship (tags → tasks)
6. `abda7a6fc6af` - Added unique constraints

---

#### 📄 Backend Root Files

- **`application.py`** - Entry point for Flask app, imports and creates the app instance
- **`config.py`** - Configuration classes (JWT secrets, CORS settings, database URI, Swagger UI)
- **`seed.py`** - Seeds database with 20 default tags (Work, Study, Exercise, etc.)
- **`data.db`** - SQLite database file (stores all application data)
- **`requirements.txt`** - Python dependencies for pip installation
- **`Pipfile`** - Pipenv dependency specification
- **`pyproject.toml`** - Modern Python project metadata
- **`venv/`** - Python virtual environment (isolated dependencies)

---

## ⚛️ FRONTEND Directory (`/frontend`)

**Purpose**: Provides the user interface for the TODO application. Built with React, TypeScript, and TailwindCSS.

**Technology Stack**: React 18, TypeScript, Vite, TailwindCSS, Axios, React Query, Zustand, React Router, ShadcnUI

### Frontend Top-Level Structure

```
frontend/
├── src/                 # Source code
├── public/              # Static assets
├── node_modules/        # NPM dependencies
├── index.html          # HTML entry point
├── package.json        # Node.js dependencies and scripts
├── vite.config.ts      # Vite bundler configuration
├── tsconfig.json       # TypeScript configuration
└── tailwind.config.js  # TailwindCSS configuration
```

---

### Frontend Directories Explained

#### 📁 `src/` - Application Source Code

**Purpose**: Contains all React components, business logic, routing, and styling.

##### `src/components/` - Reusable UI Components
**Purpose**: Shared UI components used throughout the application.

**Subdirectory**:
- `components/ui/` - ShadcnUI components (button, card, dialog, form, input, label, select, skeleton, tabs, textarea, alert-dialog)

**Goal**: Provides consistent, accessible, and styled UI primitives for building the interface.

##### `src/routes/` - Page Routing Structure
**Purpose**: Defines application pages and their layouts using React Router.

**Structure**:
```
routes/
├── landing/              # Public pages (unauthenticated)
│   ├── home/
│   │   └── _components/
│   │       ├── sign-in/      # Login form
│   │       └── create-account/ # Registration form
│   └── root.tsx          # Landing layout wrapper
├── dashboard/            # Protected pages (authenticated)
│   ├── _components/
│   │   ├── tasks/        # Task components (card, dialogs, forms)
│   │   └── tags/         # Tag components (badge, section)
│   └── page.tsx          # Main dashboard view
└── routes.tsx            # Router configuration
```

**Goal**: 
- `/` - Landing page with sign-in and create account options
- `/dashboard` - Protected route showing user's tasks and tags

##### `src/services/` - API Communication Layer
**Purpose**: Handles all HTTP requests to the backend REST API.

**Subdirectories**:
- `api/` - Axios HTTP client functions
  - `tasks.ts` - Task API calls (create, update, delete, fetch)
  - `tags.ts` - Tag API calls (fetch all tags)
- `queries/` - React Query hooks for data fetching
  - `tasks.ts` - `useTasksQuery` hook
  - `tags.ts` - `useTagsQuery` hook
- `mutations/` - React Query hooks for data modifications
  - `tasks.ts` - `useCreateTask`, `useUpdateTask`, `useDeleteTask` hooks

**Goal**: Centralized API communication with automatic caching, refetching, and optimistic updates.

##### `src/schemas/` - Form Validation
**Purpose**: Zod schemas for client-side form validation.

**Files**:
- `auth-schema.ts` - Validates sign-in and registration forms
- `task-schema.ts` - Validates task creation and editing forms

**Goal**: Ensures data integrity before sending to backend, provides user-friendly error messages.

##### `src/stores/` - Global State Management
**Purpose**: Zustand stores for managing application-wide state.

**Files**:
- `auth-store.ts` - Manages JWT token, user authentication state, sign-in/sign-out actions

**Goal**: Persistent authentication state across page refreshes using localStorage.

##### `src/types/` - TypeScript Type Definitions
**Purpose**: Defines TypeScript interfaces and types for type safety.

**Files**:
- `types.ts` - Task, Tag, User interfaces

**Goal**: Provides compile-time type checking and better IDE autocomplete.

##### `src/hooks/` - Custom React Hooks
**Purpose**: Reusable React hooks for common functionality.

**Files**:
- `useSEO.ts` - Sets page title dynamically

##### `src/lib/` - Utility Functions
**Purpose**: Helper functions and utilities.

**Files**:
- `utils.ts` - CSS class merging utilities (for TailwindCSS)

##### `src/` - Root Files
- **`main.tsx`** - Application entry point, sets up React Query and Router
- **`index.css`** - Global styles and TailwindCSS imports
- **`vite-env.d.ts`** - Vite TypeScript declarations

---

#### 📁 `public/` - Static Assets

**Purpose**: Contains static files served directly without processing.

**Files**:
- `vite.svg` - Vite logo icon

---

#### 📄 Frontend Root Files

- **`index.html`** - HTML entry point, loads the React app
- **`package.json`** - NPM dependencies, scripts (dev, build, preview)
- **`vite.config.ts`** - Vite configuration (dev server, build settings, path aliases)
- **`tsconfig.json`** - TypeScript compiler configuration
- **`tsconfig.app.json`** - TypeScript config for app source
- **`tsconfig.node.json`** - TypeScript config for Node.js scripts
- **`tailwind.config.js`** - TailwindCSS theme and plugin configuration
- **`postcss.config.js`** - PostCSS configuration for TailwindCSS processing
- **`eslint.config.js`** - ESLint linting rules
- **`components.json`** - ShadcnUI components configuration
- **`node_modules/`** - NPM packages (dependencies)

---

## 📸 PREVIEW Directory (`/preview`)

**Purpose**: Contains screenshot images of the application for documentation purposes.

**Files**: `preview1.png` through `preview8.png` - Application screenshots showing various features.

---

## Data Flow Summary

### 1. **User Authentication Flow**:
```
Frontend (Sign-in form) 
  → POST /api/v1/auth/sign-in 
  → auth_controller.py (validates credentials) 
  → Returns JWT token 
  → Stored in Zustand + localStorage 
  → Used for protected routes
```

### 2. **Task Management Flow**:
```
Frontend (Task form) 
  → POST /api/v1/tasks 
  → task_controller.py (validates, saves to DB) 
  → Returns created task 
  → React Query updates cache 
  → UI updates automatically
```

### 3. **Data Fetching Flow**:
```
Frontend (Dashboard loads) 
  → React Query triggers useTasksQuery 
  → GET /api/v1/tasks/user (with JWT header) 
  → task_controller.py fetches from DB 
  → Returns JSON array 
  → React Query caches data 
  → Components render tasks
```

---

## Running the Application

### Backend:
```bash
cd backend
source venv/bin/activate
flask run  # Runs on http://127.0.0.1:5000
```

### Frontend:
```bash
cd frontend
npm run dev  # Runs on http://localhost:5173
```

---

## Technology Highlights

### Backend:
- **Flask-Smorest**: Automatic API documentation (Swagger UI at `/docs`)
- **Flask-Migrate**: Database version control
- **Flask-JWT-Extended**: Secure JWT authentication
- **SQLAlchemy**: ORM for database operations
- **Marshmallow**: Request/response serialization and validation

### Frontend:
- **React Query**: Server state management with caching
- **Zustand**: Client state management (auth)
- **React Router**: Client-side routing
- **React Hook Form**: Form handling with validation
- **Zod**: Schema validation
- **Axios**: HTTP client
- **ShadcnUI**: Pre-built accessible components
- **TailwindCSS**: Utility-first CSS framework

---

## Database Schema

### Users Table:
- `id` (PK), `username` (unique), `email` (unique), `password` (hashed)

### Tasks Table:
- `id` (PK), `title`, `content`, `status`, `created_at`, `user_id` (FK), `tag_id` (FK)

### Tags Table:
- `id` (PK), `name` (unique)

**Relationships**:
- User → Tasks (1:N) - One user can have many tasks
- Tag → Tasks (1:N) - One tag can be assigned to many tasks

---

*This document was generated to provide a comprehensive understanding of the TODO App project structure.*

