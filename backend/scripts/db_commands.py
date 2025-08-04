#!/usr/bin/env python3
"""
Database management commands for development workflow.
This script provides convenient database operations for developers.
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
        return None

def check_database_exists():
    """Check if the database file exists."""
    db_path = Path("chat_app.db")
    return db_path.exists()

def get_database_info():
    """Get information about the current database."""
    if not check_database_exists():
        print("Database does not exist.")
        return
    
    try:
        conn = sqlite3.connect("chat_app.db")
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Database Information:")
        print(f"Database file: chat_app.db")
        print(f"Tables: {len(tables)}")
        
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} records")
        
        conn.close()
        
    except Exception as e:
        print(f"Error getting database info: {e}")

def create_migration(message):
    """Create a new migration."""
    print(f"Creating migration: {message}")
    command = f'alembic revision --autogenerate -m "{message}"'
    output = run_command(command)
    if output:
        print(output)
        return True
    return False

def apply_migrations():
    """Apply all pending migrations."""
    print("Applying migrations...")
    command = "alembic upgrade head"
    output = run_command(command)
    if output:
        print(output)
        return True
    return False

def rollback_migration(steps=1):
    """Rollback migrations by specified steps."""
    print(f"Rolling back {steps} migration(s)...")
    if steps == 1:
        command = "alembic downgrade -1"
    else:
        command = f"alembic downgrade -{steps}"
    
    output = run_command(command)
    if output:
        print(output)
        return True
    return False

def show_migration_status():
    """Show current migration status."""
    print("Migration Status:")
    
    # Show current revision
    command = "alembic current"
    output = run_command(command)
    if output:
        print("Current revision:")
        print(output)
    
    # Show migration history
    command = "alembic history --verbose"
    output = run_command(command)
    if output:
        print("Migration history:")
        print(output)

def reset_database():
    """Reset the database completely."""
    print("Resetting database...")
    
    # Remove database file if it exists
    db_path = Path("chat_app.db")
    if db_path.exists():
        print("Removing existing database file...")
        db_path.unlink()
    
    # Apply all migrations
    if apply_migrations():
        print("Database reset complete!")
        return True
    else:
        print("Failed to reset database.")
        return False

def seed_database():
    """Seed the database with initial data."""
    print("Seeding database...")
    
    # Check if seed script exists
    seed_script = Path("seed_admin.py")
    if seed_script.exists():
        command = "python seed_admin.py"
        output = run_command(command)
        if output:
            print(output)
            print("Database seeded successfully!")
            return True
    else:
        print("Seed script not found. Creating basic admin user...")
        # You could add basic seeding logic here
        return False

def backup_database():
    """Create a backup of the current database."""
    if not check_database_exists():
        print("No database to backup.")
        return False
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"chat_app_backup_{timestamp}.db"
    
    try:
        import shutil
        shutil.copy2("chat_app.db", backup_name)
        print(f"Database backed up to: {backup_name}")
        return True
    except Exception as e:
        print(f"Error creating backup: {e}")
        return False

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Database Management Commands")
        print("Usage: python scripts/db_commands.py <command> [args]")
        print("\nAvailable commands:")
        print("  info                    - Show database information")
        print("  status                  - Show migration status")
        print("  create <message>        - Create a new migration")
        print("  migrate                 - Apply all pending migrations")
        print("  rollback [steps]        - Rollback migrations (default: 1 step)")
        print("  reset                   - Reset database and apply all migrations")
        print("  seed                    - Seed database with initial data")
        print("  backup                  - Create a backup of the database")
        print("\nExamples:")
        print("  python scripts/db_commands.py create 'Add user preferences'")
        print("  python scripts/db_commands.py rollback 2")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "info":
        get_database_info()
    elif command == "status":
        show_migration_status()
    elif command == "create":
        if len(sys.argv) < 3:
            print("Error: create command requires a message")
            sys.exit(1)
        create_migration(sys.argv[2])
    elif command == "migrate":
        apply_migrations()
    elif command == "rollback":
        steps = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        rollback_migration(steps)
    elif command == "reset":
        reset_database()
    elif command == "seed":
        seed_database()
    elif command == "backup":
        backup_database()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()