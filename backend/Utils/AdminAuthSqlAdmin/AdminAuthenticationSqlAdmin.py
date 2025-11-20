from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from sqlalchemy import select
from Database.Database import AsyncSessionLocal
from Models.USER.UserModel import User
from Utils.Auth.HashPassword import verify_password
from Utils.Enums.Enums import UserRole
from Utils.Auth.JWT import create_access_token


#### SQLADMIN ADMIN DASHBOARD AUTHENTICATION ####
class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        async with AsyncSessionLocal() as session:
            stmt = select(User).where(User.username == username)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

        # Validate User, Password, and Role
        if not user:
            return False
            
        if not verify_password(password, user.hashed_password):
            return False
            
        #### Only allow ADMINs ####
        if user.role != UserRole.ADMIN:
            return False

        # Create a session token (using JWT from Utils folder)
        access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
        request.session.update({"token": access_token})
        
        return True


    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True


    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        return True