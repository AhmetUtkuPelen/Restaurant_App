from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import jwt
from datetime import datetime, timedelta
import os

from Models.USER.UserModel import User
from Database.Database import AsyncSessionLocal
from Utils.Enums.Enums import UserRole


class AdminAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        """Handle admin login"""
        try:
            form = await request.form()
            username = form.get("username")
            password = form.get("password")

            print(f"[DEBUG] Login attempt - Username: {username}")

            # Validate credentials
            async with AsyncSessionLocal() as db:
                stmt = select(User).where(User.username == username)
                result = await db.execute(stmt)
                user = result.scalar_one_or_none()

                if not user:
                    print(f"[DEBUG] User not found: {username}")
                    return False

                print(f"[DEBUG] User found: {user.username}, Role: {user.role}")

                # Verify password using bcrypt directly
                import bcrypt
                
                # Convert password to bytes if it's a string
                password_bytes = password.encode('utf-8') if isinstance(password, str) else password
                hashed_password_bytes = user.hashed_password.encode('utf-8') if isinstance(user.hashed_password, str) else user.hashed_password
                
                password_match = bcrypt.checkpw(password_bytes, hashed_password_bytes)
                print(f"[DEBUG] Password match: {password_match}")
                
                if not password_match:
                    print(f"[DEBUG] Password verification failed")
                    return False

                # Check if user is admin or staff
                if user.role not in [UserRole.ADMIN, UserRole.STAFF]:
                    print(f"[DEBUG] User role not authorized: {user.role}")
                    return False

                print(f"[DEBUG] User authorized, creating session token")

                # Create JWT token for session
                secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
                token_data = {
                    "sub": str(user.id),
                    "username": user.username,
                    "role": user.role.value,
                    "exp": datetime.utcnow() + timedelta(hours=24)
                }
                token = jwt.encode(token_data, secret_key, algorithm="HS256")

                # Store token in session
                request.session["token"] = token
                request.session["user_id"] = user.id
                request.session["username"] = user.username
                
                # Force session to be marked as modified
                request.session.update(request.session)
                
                print(f"[DEBUG] Session updated with token")
                print(f"[DEBUG] Session after update: {dict(request.session)}")
                print(f"[DEBUG] Login successful for user: {username}")
                return True
                
        except Exception as e:
            print(f"[DEBUG] Login error: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    async def logout(self, request: Request) -> bool:
        """Handle admin logout"""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Optional[RedirectResponse]:
        """Check if user is authenticated for each request"""
        print(f"[DEBUG] Authenticate called for path: {request.url.path}")
        print(f"[DEBUG] Full URL: {request.url}")
        
        # Only authenticate admin routes
        if not request.url.path.startswith("/admin"):
            print(f"[DEBUG] Not an admin route ({request.url.path}), skipping authentication")
            return None
        
        # Skip authentication for login page
        if request.url.path == "/admin/login":
            print(f"[DEBUG] Skipping auth for login page")
            return None
        
        print(f"[DEBUG] Session data: {dict(request.session)}")
        token = request.session.get("token")

        if not token:
            print(f"[DEBUG] No token found in session")
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        print(f"[DEBUG] Token found in session")

        try:
            secret_key = os.getenv("JWT_SECRET_KEY", "your-secret-key")
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            print(f"[DEBUG] Token decoded successfully, user: {payload.get('username')}")
            
            # Verify user still exists and has admin/staff role
            async with AsyncSessionLocal() as db:
                stmt = select(User).where(User.id == int(payload["sub"]))
                result = await db.execute(stmt)
                user = result.scalar_one_or_none()

                if not user or user.role not in [UserRole.ADMIN, UserRole.STAFF]:
                    print(f"[DEBUG] User not found or not authorized")
                    return RedirectResponse(request.url_for("admin:login"), status_code=302)

                print(f"[DEBUG] User authenticated: {user.username}")

        except jwt.ExpiredSignatureError:
            print(f"[DEBUG] Token expired")
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        except jwt.InvalidTokenError as e:
            print(f"[DEBUG] Invalid token: {str(e)}")
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        except Exception as e:
            print(f"[DEBUG] Authentication error: {str(e)}")
            import traceback
            traceback.print_exc()
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        # User is authenticated
        print(f"[DEBUG] Authentication successful")
        return None
