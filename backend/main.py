import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Database.Database import init_db, engine
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from Utils.SlowApi.SlowApi import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler




from sqladmin import Admin, ModelView







# GET .ENV VARIABLES
load_dotenv()
# GET .ENV VARIABLES


ENVIRONMENT = os.getenv("ENVIRONMENT", "DEVELOPMENT").upper()
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
RELOAD = os.getenv("RELOAD", "False").lower() == "true"
PORT = os.getenv("PORT", 8000)




# -----------------------------
#  Lifespan Context Manager
# -----------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f" Starting Server in {ENVIRONMENT} mode...")
    await init_db()
    print(" Database initialized and ready.")

    # Yield control to FastAPI (the app runs during this time)
    yield

    print(" Shutting down Server...")
    await engine.dispose()
    print(" Database connections closed.")


# -----------------------------
# FastAPI App Config
# -----------------------------
app = FastAPI(
    title="Restaurant Service API",
    description="""
    Handles restaurant backend data.
    Built with * *FastAPI + Async SQLAlchemy + Pydantic **.
    """,
    version="1.0.0",
    lifespan=lifespan,
)



# -----------------------------
# CORS Config
# -----------------------------
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # "https://frontend.yourapp.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Rate limiter (slowapi) setup
# -----------------------------
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
# -----------------------------
# Rate limiter (slowapi) setup
# -----------------------------




########## SQL ADMIN CONFIG ##########

admin = Admin(app, engine)

# SQLAdmin syntax: pass model as parameter in class definition
class UserModelForAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.role]
    column_searchable_list = [User.username, User.email, User.role]
    column_filters = [User.username, User.email, User.role]
    column_sortable_list = [User.username, User.email, User.role]


admin.add_view(UserModelForAdmin)

########## SQL ADMIN CONFIG ##########



### ROUTES ###

### ROUTES ###







# -----------------------------
# Root + Health Endpoints
# -----------------------------
@app.get("/", tags=["Health"])
async def root():
    return {
        "status": "ok",
        "service": "Restaurant_Service",
        "environment": ENVIRONMENT,
        "message": "Running smoothly 🚀",
    }


@app.get("/health", tags=["Monitoring"])
async def health_check():
    return {"status": "healthy"}



# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=PORT,
        debug=DEBUG,
        reload=RELOAD,
    )