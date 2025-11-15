# Database Seeding

## Admin User Seeding

This directory contains scripts to seed initial data into the database.

### Seeding Admin Users

There are **two ways** to seed admin users:

#### Method 1: Run the Seeding Script Directly

```bash
# From the backend directory
python -m Database.Seed.SeedAdminUser
```

This will create 3 admin users if they don't already exist.

#### Method 2: Automatic Seeding on Server Startup

Add this to your `.env` file:

```env
SEED_ADMIN=true
```

Then start your server normally:

```bash
uvicorn main:app --reload
```

The admin users will be automatically seeded when the server starts.

**Note:** After the first run, set `SEED_ADMIN=false` or remove it from `.env` to prevent checking on every startup.

### Default Admin Credentials

After seeding, you can login with these credentials:

#### 1. Main Admin
- **Username:** `admin`
- **Password:** `Admin123!@#`
- **Email:** `admin@restaurant.com`

#### 2. Secondary Admin
- **Username:** `admin2`
- **Password:** `Admin123!@#`
- **Email:** `admin2@restaurant.com`

#### 3. Super Admin
- **Username:** `superadmin`
- **Password:** `SuperAdmin123!@#`
- **Email:** `superadmin@restaurant.com`

### ⚠️ IMPORTANT SECURITY NOTES

1. **Change these passwords immediately after first login!**
2. These are default credentials for development only
3. Never use these passwords in production
4. The seeding script will skip users that already exist

### How It Works

The seeding script:
1. Checks if each admin user already exists (by username and email)
2. If the user doesn't exist, creates them with the default credentials
3. Hashes passwords securely using bcrypt
4. Automatically creates a cart for each admin user (via the User model event listener)
5. Logs the results (created/skipped counts)

### Customizing Admin Users

To customize the admin users, edit the `admin_users` list in `SeedAdminUser.py`:

```python
admin_users = [
    {
        "username": "your_username",
        "email": "your_email@example.com",
        "password": "YourSecurePassword123!",
        "role": UserRole.ADMIN,
        "phone": "+905551234567",
        "address": "Your Address",
        "image_url": "https://your-image-url.com/avatar.jpg"
    },
    # Add more admin users...
]
```

### Troubleshooting

**Issue:** "User already exists" message
- **Solution:** This is normal. The script skips existing users to prevent duplicates.

**Issue:** "Email already exists" message
- **Solution:** Change the email in the seeding script or delete the existing user first.

**Issue:** Import errors
- **Solution:** Make sure you're running from the backend directory and all dependencies are installed.

**Issue:** Database connection errors
- **Solution:** Check your `.env` file has the correct `DATABASE_URL` configured.
