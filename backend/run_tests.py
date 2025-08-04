#!/usr/bin/env python3
"""
Test runner script for the chat application backend

This script runs the comprehensive test suite including unit tests,
integration tests, and security tests with proper configuration.
"""

import sys
import subprocess
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print("STDOUT:")
        print(result.stdout)
    
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    
    if result.returncode != 0:
        print(f"❌ {description} failed with return code {result.returncode}")
        return False
    else:
        print(f"✅ {description} completed successfully")
        return True

def main():
    """Main test runner function."""
    print("🚀 Starting Chat Application Test Suite")
    print(f"Working directory: {os.getcwd()}")
    
    # Change to backend directory if not already there
    if not os.path.exists("pytest.ini"):
        backend_path = Path(__file__).parent
        os.chdir(backend_path)
        print(f"Changed to backend directory: {os.getcwd()}")
    
    # Check if pytest is available
    try:
        import pytest
        print(f"✅ pytest version: {pytest.__version__}")
    except ImportError:
        print("❌ pytest not found. Please install requirements:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    
    # Test commands to run
    test_commands = [
        {
            "command": "python -m pytest tests/ -v --tb=short",
            "description": "Basic Test Run"
        },
        {
            "command": "python -m pytest tests/test_auth_service.py -v",
            "description": "Authentication Service Tests"
        },
        {
            "command": "python -m pytest tests/test_password_service.py -v",
            "description": "Password Service Tests"
        },
        {
            "command": "python -m pytest tests/test_validation_service.py -v",
            "description": "Validation Service Tests"
        },
        {
            "command": "python -m pytest tests/test_api_integration.py -v",
            "description": "API Integration Tests"
        },
        {
            "command": "python -m pytest tests/test_security.py -v -m security",
            "description": "Security Tests"
        },
        {
            "command": "python -m pytest tests/ -v --cov=. --cov-report=term-missing --cov-report=html:htmlcov",
            "description": "Coverage Report"
        },
        {
            "command": "python -m pytest tests/ -v -m 'not slow'",
            "description": "Fast Tests Only"
        }
    ]
    
    # Run tests based on command line arguments
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == "unit":
            # Run only unit tests
            commands = [cmd for cmd in test_commands if "service" in cmd["description"].lower()]
        elif test_type == "integration":
            # Run only integration tests
            commands = [cmd for cmd in test_commands if "integration" in cmd["description"].lower()]
        elif test_type == "security":
            # Run only security tests
            commands = [cmd for cmd in test_commands if "security" in cmd["description"].lower()]
        elif test_type == "coverage":
            # Run coverage report
            commands = [cmd for cmd in test_commands if "coverage" in cmd["description"].lower()]
        elif test_type == "fast":
            # Run fast tests only
            commands = [cmd for cmd in test_commands if "fast" in cmd["description"].lower()]
        elif test_type == "all":
            # Run all tests
            commands = test_commands
        else:
            print(f"❌ Unknown test type: {test_type}")
            print("Available options: unit, integration, security, coverage, fast, all")
            sys.exit(1)
    else:
        # Default: run basic tests
        commands = [test_commands[0]]  # Basic test run
    
    # Run selected test commands
    success_count = 0
    total_count = len(commands)
    
    for cmd_info in commands:
        if run_command(cmd_info["command"], cmd_info["description"]):
            success_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    print(f"✅ Successful: {success_count}/{total_count}")
    print(f"❌ Failed: {total_count - success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()