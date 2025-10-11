"""
Unit tests for flaskr.utils module

Tests password hashing and verification utilities.
"""

import pytest
from flaskr.utils import generate_password, check_password


@pytest.mark.unit
@pytest.mark.auth
class TestPasswordUtils:
    """Test password generation and verification utilities."""
    
    def test_generate_password_returns_hash(self):
        """Test that generate_password returns a non-empty hash string."""
        password = "test_password123"
        hashed = generate_password(password)
        
        assert hashed is not None
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        # Bcrypt hashes start with $2b$ or $2a$ or $2y$
        assert hashed.startswith('$2')
    
    def test_generate_password_different_hashes(self):
        """Test that same password generates different hashes (salt randomness)."""
        password = "test_password123"
        hash1 = generate_password(password)
        hash2 = generate_password(password)
        
        # Same password should generate different hashes due to random salt
        assert hash1 != hash2
    
    def test_check_password_with_correct_password(self):
        """Test that check_password returns True for correct password."""
        password = "correct_password"
        hashed = generate_password(password)
        
        result = check_password(hashed, password)
        
        assert result is True
    
    def test_check_password_with_incorrect_password(self):
        """Test that check_password returns False for incorrect password."""
        password = "correct_password"
        wrong_password = "wrong_password"
        hashed = generate_password(password)
        
        result = check_password(hashed, wrong_password)
        
        assert result is False
    
    def test_check_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "TestPassword"
        hashed = generate_password(password)
        
        assert check_password(hashed, password) is True
        assert check_password(hashed, "testpassword") is False
        assert check_password(hashed, "TESTPASSWORD") is False
    
    @pytest.mark.parametrize("password", [
        "short",
        "averagelenpass",
        "very_long_password_with_special_chars!@#$%^&*()",
        "password with spaces",
        "пароль",  # Unicode characters
        "12345678",  # Numbers only
    ])
    def test_generate_and_check_various_passwords(self, password):
        """Test password generation and verification with various inputs."""
        hashed = generate_password(password)
        
        assert check_password(hashed, password) is True
        assert check_password(hashed, password + "x") is False
    
    def test_check_password_with_empty_password(self):
        """Test behavior with empty password."""
        hashed = generate_password("nonempty")
        
        # Empty password should not match
        result = check_password(hashed, "")
        assert result is False
    
    def test_generate_password_with_empty_string(self):
        """Test that empty password can be hashed (edge case)."""
        # While not recommended in production, the function should handle it
        hashed = generate_password("")
        
        assert hashed is not None
        assert isinstance(hashed, str)
        assert check_password(hashed, "") is True



