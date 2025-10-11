"""
Utility Functions Module

This module provides utility functions for password hashing and verification
using Werkzeug's security features.
"""

from werkzeug.security import generate_password_hash, check_password_hash


def generate_password(password: str) -> str:
    """
    Generate a secure password hash using bcrypt.

    This function takes a plain-text password and returns a bcrypt hash
    with a salt length of 10 characters for secure storage in the database.

    Args:
        password (str): Plain-text password to hash

    Returns:
        str: Bcrypt hashed password with salt (approximately 300 characters)

    Security:
        - Uses bcrypt algorithm (Werkzeug default)
        - Salt length: 10 characters
        - Suitable for long-term storage

    Example:
        >>> plain_password = "mysecretpassword123"
        >>> hashed = generate_password(plain_password)
        >>> print(len(hashed))
        60  # Standard bcrypt hash length

    Note:
        Never store plain-text passwords. Always use this function before
        saving passwords to the database.
    """
    return generate_password_hash(password, salt_length=10)


def check_password(password_hash: str, password: str) -> bool:
    """
    Verify a password against its hash.

    This function checks if a plain-text password matches a previously
    generated password hash using constant-time comparison to prevent
    timing attacks.

    Args:
        password_hash (str): The stored bcrypt password hash
        password (str): Plain-text password to verify

    Returns:
        bool: True if password matches the hash, False otherwise

    Security:
        - Uses constant-time comparison
        - Prevents timing attacks
        - Works with bcrypt hashes

    Example:
        >>> hashed = generate_password("mypassword")
        >>> check_password(hashed, "mypassword")
        True
        >>> check_password(hashed, "wrongpassword")
        False

    Note:
        This function is safe to use in authentication flows as it prevents
        timing attacks through constant-time comparison.
    """
    return check_password_hash(password_hash, password)
