# Database Migrations

This directory contains the Alembic migration system for the chat application database.

## Overview

Alembic is used to manage database schema changes in a version-controlled manner. This allows us to:
- Track database schema changes over time
- Apply changes consistently across different environments
- Rollback changes if needed
- Collaborate on database changes with other developers

## Directory Structure

```
alembic/
├── versions/           # Migration files
├── env.py             # Migration environment configuration
├── script.py.mako     # Template for new migration files
└── README.md          # This file
```

## Quick Start

### Using the Database Commands Script (Recommended)

The easiest way to work with migrations is using the database commands script:

```bash
# Show database information
python scripts/db_commands.py info

# Show migration status
python scripts/db_commands.py status

# Create a new migration
python scripts/db_commands.py create "Add user preferences table"

# Apply all pending migrations
python scripts/db_commands.py migrate

# Rollback last migration
python scripts/db_commands.py rollback

# Rollback multiple migrations
python scripts/db_commands.py rollback 3

# Reset database (removes and recreates)
python scripts/db_commands.py reset

# Create database backup
python scripts/db_commands.py backup
```

### Using Alembic Directly

You can also use Alembic commands directly:

```bash
# Create a new migration
alembic revision --autogenerate -m "Add user preferences table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history --verbose
```

### Using the Migration Utility Script

There's also a migration utility script for more advanced operations:

```bash
# Create a migration
python migrate.py create "Add new feature"

# Upgrade database
python migrate.py upgrade

# Show current revision
python migrate.py current

# Show history
python migrate.py history

# Reset database
python migrate.py reset
```

## Development Workflow

### 1. Making Schema Changes

When you need to change the database schema:

1. **Modify the models** in `Models/database_models.py`
2. **Create a migration**:
   ```bash
   python scripts/db_commands.py create "Describe your changes"
   ```
3. **Review the generated migration** in `alembic/versions/`
4. **Apply the migration**:
   ```bash
   python scripts/db_commands.py migrate
   ```

### 2. Working with Existing Databases

If you have an existing database and want to bring it under migration control:

1. **Backup your database**:
   ```bash
   python scripts/db_commands.py backup
   ```
2. **Reset to use migrations**:
   ```bash
   python scripts/db_commands.py reset
   ```

### 3. Collaboration

When working with other developers:

1. **Pull latest changes** from version control
2. **Check migration status**:
   ```bash
   python scripts/db_commands.py status
   ```
3. **Apply any new migrations**:
   ```bash
   python scripts/db_commands.py migrate
   ```

## Migration Best Practices

### 1. Migration Naming

Use descriptive names for your migrations:
- ✅ "Add user email verification fields"
- ✅ "Create audit log table"
- ✅ "Add indexes for message queries"
- ❌ "Update database"
- ❌ "Fix stuff"

### 2. Review Generated Migrations

Always review the auto-generated migration before applying:
- Check that all intended changes are included
- Verify that foreign key relationships are correct
- Ensure indexes are created where needed
- Add any custom data migration logic if needed

### 3. Test Migrations

Before applying migrations to production:
- Test on a copy of production data
- Verify that the migration can be rolled back
- Check that the application works with the new schema

### 4. Backup Before Major Changes

Always backup your database before applying migrations, especially in production:
```bash
python scripts/db_commands.py backup
```

## Common Operations

### Adding a New Table

1. Add the model class to `Models/database_models.py`
2. Import the model in `alembic/env.py` (if not already imported)
3. Create migration:
   ```bash
   python scripts/db_commands.py create "Add new_table"
   ```

### Adding a Column

1. Add the column to the existing model in `Models/database_models.py`
2. Create migration:
   ```bash
   python scripts/db_commands.py create "Add column_name to table_name"
   ```

### Adding an Index

1. Add the index to the model (using `index=True` or `Index()`)
2. Create migration:
   ```bash
   python scripts/db_commands.py create "Add index on table_name.column_name"
   ```

### Data Migrations

For migrations that need to modify existing data:

1. Create an empty migration:
   ```bash
   alembic revision -m "Migrate user data"
   ```
2. Edit the migration file to add custom logic in the `upgrade()` function
3. Add corresponding rollback logic in the `downgrade()` function

## Troubleshooting

### Migration Conflicts

If you encounter migration conflicts (multiple heads):
```bash
alembic merge heads -m "Merge migrations"
```

### Corrupted Migration State

If the migration state becomes corrupted:
1. Backup your data
2. Reset the database:
   ```bash
   python scripts/db_commands.py reset
   ```

### SQLite Limitations

When using SQLite, some operations require special handling:
- Column renames and type changes may require table recreation
- The migration environment is configured with `render_as_batch=True` for SQLite compatibility

## Environment Configuration

The migration environment is configured in `env.py`:
- Database URL is loaded from `config.py`
- All models are imported to ensure they're registered
- SQLite-specific settings are enabled
- Batch operations are enabled for SQLite compatibility

## Production Considerations

### Before Deploying

1. **Test migrations** on a production-like dataset
2. **Estimate migration time** for large tables
3. **Plan for downtime** if needed
4. **Prepare rollback plan**

### During Deployment

1. **Backup production database**
2. **Apply migrations** during maintenance window
3. **Verify application functionality**
4. **Monitor for issues**

### After Deployment

1. **Verify data integrity**
2. **Monitor application performance**
3. **Keep migration logs** for troubleshooting

## Files and Scripts

- `alembic.ini` - Alembic configuration
- `env.py` - Migration environment setup
- `script.py.mako` - Template for new migrations
- `versions/` - Directory containing migration files
- `../migrate.py` - Migration utility script
- `../scripts/db_commands.py` - Database management commands