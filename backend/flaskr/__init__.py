"""
Flask Application Factory Module

This module provides the application factory pattern for creating and configuring
the Flask application instance with all necessary extensions and blueprints.
"""

import flaskr.models  # Import models to register them with SQLAlchemy

from flask import Flask
from config import DevelopmentConfig
from flaskr.extensions import migrate, api, cors, jwt
from flaskr.db import db

from flaskr.routes.auth_route import bp as auth_route
from flaskr.routes.user_route import bp as user_route
from flaskr.routes.tag_route import bp as tag_route
from flaskr.routes.task_route import bp as task_route


def create_app(test_config=None):
    """
    Create and configure the Flask application instance.

    This function implements the application factory pattern, which allows
    creating multiple instances of the application with different configurations
    (e.g., for testing, development, production).

    Args:
        test_config (object, optional): Configuration object for testing.
            If None, uses DevelopmentConfig. Defaults to None.

    Returns:
        Flask: Configured Flask application instance

    Configuration:
        - Database: SQLAlchemy with SQLite
        - Migrations: Flask-Migrate (Alembic)
        - API: Flask-Smorest for REST API
        - CORS: Configured for frontend origins
        - Auth: JWT-based authentication

    Blueprints:
        - /api/v1/auth: Authentication endpoints (sign-in, sign-up)
        - /api/v1/users: User management endpoints
        - /api/v1/tags: Tag management endpoints
        - /api/v1/tasks: Task management endpoints

    Example:
        >>> # Development mode
        >>> app = create_app()
        >>> app.run(debug=True)

        >>> # Testing mode
        >>> app = create_app(test_config=TestConfig)
        >>> with app.test_client() as client:
        ...     response = client.get('/api/v1/tasks')

    Extensions Initialized:
        1. SQLAlchemy (db) - Database ORM
        2. Flask-Migrate - Database migrations
        3. Flask-Smorest (api) - RESTful API with OpenAPI docs
        4. Flask-CORS - Cross-Origin Resource Sharing
        5. Flask-JWT-Extended - JWT authentication

    Note:
        All models must be imported before db.init_app() to ensure
        they are registered with SQLAlchemy for migrations.
    """
    # Create Flask application instance
    app = Flask(__name__)

    # Load configuration
    if test_config is None:
        # Use development configuration
        app.config.from_object(DevelopmentConfig)
    else:
        # Use provided test configuration
        app.config.from_object(test_config)

    # Initialize extensions
    db.init_app(app)  # Database
    migrate.init_app(app, db)  # Database migrations
    api.init_app(app)  # REST API with OpenAPI docs

    # Configure CORS for frontend access
    cors.init_app(
        app,
        origins=app.config.get('CORS_ORIGINS', '*'),
        allow_headers=app.config.get('CORS_ALLOW_HEADERS'),
        methods=app.config.get('CORS_METHODS')
    )

    # Initialize JWT authentication
    jwt.init_app(app)

    # Register API blueprints with versioned prefix
    api.register_blueprint(auth_route, url_prefix="/api/v1")
    api.register_blueprint(user_route, url_prefix="/api/v1")
    api.register_blueprint(tag_route, url_prefix="/api/v1")
    api.register_blueprint(task_route, url_prefix="/api/v1")

    return app
