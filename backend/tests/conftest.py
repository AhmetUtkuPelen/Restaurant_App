"""
Minimal pytest configuration for Chat API tests
"""

import pytest
from unittest.mock import Mock, patch

@pytest.fixture
def mock_redis():
    """Mock Redis client for testing."""
    with patch('Services.AuthService.AuthService._get_redis_client') as mock_redis:
        mock_client = Mock()
        mock_client.ping.return_value = True
        mock_client.setex.return_value = True
        mock_client.set.return_value = True
        mock_client.exists.return_value = False
        mock_redis.return_value = mock_client
        yield mock_client