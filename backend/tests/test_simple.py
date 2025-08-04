"""
Simple test to check fixture loading
"""

def test_simple_fixture(simple_fixture):
    """Test that simple fixture works."""
    assert simple_fixture == "test_value"