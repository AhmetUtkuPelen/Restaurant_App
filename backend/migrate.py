#!/usr/bin/env python3
"""
Database migration utility script for the chat application.
This script provides convenient commands for managing database migrations.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd or os.getcwd(),
            capture_output=True, 
            text=True, 
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def init_alembic():
    """Initialize Alembic (already done, but kept for reference)."""
    print("Alembic is already initialized.")

def create_migration(message="Auto-generated migration"):
    """Create a new migration."""
    print(f"Creating migration: {message}")
    command = f'alembic revision --autogenerate -m "{message}"'
    output = run_command(command)
    print(output)

def upgrade_database(revision="head"):
    """Upgrade database to a specific revision."""
    print(f"Upgrading database to revision: {revision}")
    command = f"alembic upgrade {revision}"
    output = run_command(command)
    print(output)

def downgrade_database(revision):
    """Downgrade database to a specific revision."""
    print(f"Downgrading database to revision: {revision}")
    command = f"alembic downgrade {revision}"
    output = run_command(command)
    print(output)

def show_current_revision():
    """Show current database revision."""
    print("Current database revision:")
    command = "alembic current"
    output = run_command(command)
    print(output)

def show_migration_history():
    """Show migration history."""
    print("Migration history:")
    command = "alembic history --verbose"
    output = run_command(command)
    print(output)

def reset_database():
    """Reset database by removing it and running all migrations."""
    db_file = Path("chat_app.db")
    if db_file.exists():
        print("Removing existing database...")
        db_file.unlink()
    
    print("Running all migrations...")
    upgrade_database()

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python migrate.py <command> [args]")
        print("Commands:")
        print("  init                    - Initialize Alembic (already done)")
        print("  create <message>        - Create a new migration")
        print("  upgrade [revision]      - Upgrade database (default: head)")
        print("  downgrade <revision>    - Downgrade database")
        print("  current                 - Show current revision")
        print("  history                 - Show migration history")
        print("  reset                   - Reset database and run all migrations")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        init_alembic()
    elif command == "create":
        message = sys.argv[2] if len(sys.argv) > 2 else "Auto-generated migration"
        create_migration(message)
    elif command == "upgrade":
        revision = sys.argv[2] if len(sys.argv) > 2 else "head"
        upgrade_database(revision)
    elif command == "downgrade":
        if len(sys.argv) < 3:
            print("Error: downgrade requires a revision argument")
            sys.exit(1)
        downgrade_database(sys.argv[2])
    elif command == "current":
        show_current_revision()
    elif command == "history":
        show_migration_history()
    elif command == "reset":
        reset_database()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()