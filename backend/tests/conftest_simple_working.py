"""
Simple conftest for testing
"""

import pytest

@pytest.fixture
def simple_fixture():
    """Simple test fixture."""
    return "test_value"