import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Database.Database import init_db, engine, sync_engine
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from Utils.SlowApi.SlowApi import limiter
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler



### ADMIN DASHBOARD FOR MODELS ###
from sqladmin import Admin, ModelView


# Import models for SQLAdmin
from Models.USER.UserModel import User
from Models.PRODUCT.Dessert.DessertModel import Dessert
from Models.PRODUCT.Doner.DonerModel import Doner
from Models.PRODUCT.Drink.DrinkModel import Drink
from Models.PRODUCT.Kebab.KebabModel import Kebab
from Models.PRODUCT.Salad.SaladModel import Salad
from Models.RESERVATION.TableModel import Table
from Models.RESERVATION.ReservationModel import Reservation
from Models.COMMENT.CommentModel import Comment


# Import Routes
from Routes.USER.UserRoutes import UserRouter
from Routes.RESERVATION.TableRoutes import TableRouter
from Routes.RESERVATION.ReservationRoutes import ReservationRouter
from Routes.PRODUCT.Dessert.DessertRoutes import DessertRouter
from Routes.PRODUCT.Doner.DonerRoutes import DonerRouter
from Routes.PRODUCT.Drink.DrinkRoutes import DrinkRouter
from Routes.PRODUCT.Kebab.KebabRoutes import KebabRouter
from Routes.PRODUCT.Salad.SaladRoutes import SaladRouter
from Routes.PRODUCT.FavouriteProduct.FavouriteProductRoutes import FavouriteProductRouter
from Routes.COMMENT.CommentRoutes import CommentRouter
from Routes.CART.CartRoutes import CartRouter
from Routes.ORDER.OrderRoutes import OrderRouter
from Routes.PAYMENT.PaymentRoutes import PaymentRouter







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
    
    # Optional: Seed admin users on startup (set SEED_ADMIN=true in .env)
    if os.getenv("SEED_ADMIN", "false").lower() == "true":
        print(" Seeding admin users...")
        from Database.Seed.SeedAdminUser import seed_admin_users
        try:
            await seed_admin_users()
            print(" Admin users seeded successfully.")
        except Exception as e:
            print(f" Warning: Admin user seeding failed: {str(e)}")
    
    # Optional: Seed products on startup (set SEED_PRODUCTS=true in .env)
    if os.getenv("SEED_PRODUCTS", "false").lower() == "true":
        print(" Seeding products...")
        from Database.Seed.SeedAllProducts import seed_all_products
        try:
            await seed_all_products()
            print(" Products seeded successfully.")
        except Exception as e:
            print(f" Warning: Product seeding failed: {str(e)}")
    
    # Optional: Seed tables on startup (set SEED_TABLES=true in .env)
    if os.getenv("SEED_TABLES", "false").lower() == "true":
        print(" Seeding tables...")
        from Database.Seed.SeedTables import seed_tables
        try:
            await seed_tables()
            print(" Tables seeded successfully.")
        except Exception as e:
            print(f" Warning: Table seeding failed: {str(e)}")

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

admin = Admin(app, sync_engine)

# SQLAdmin syntax: pass model as parameter in class definition
class UserModelForAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.email, User.role]
    column_searchable_list = [User.username, User.email, User.role]
    column_filters = [User.username, User.email, User.role]
    column_sortable_list = [User.username, User.email, User.role]

class TableModelForAdmin(ModelView,model=Table):
    column_list = [Table.id, Table.table_number, Table.capacity, Table.location, Table.is_available]
    column_searchable_list = [Table.table_number, Table.capacity, Table.location, Table.is_available]
    column_filters = [Table.table_number, Table.capacity, Table.location, Table.is_available]
    column_sortable_list = [Table.table_number, Table.capacity, Table.location, Table.is_available]

class ReservationModelForAdmin(ModelView, model=Reservation):
    column_list = [Reservation.id, Reservation.user_id, Reservation.table_id, Reservation.reservation_time, Reservation.number_of_guests, Reservation.status]
    column_searchable_list = [Reservation.user_id, Reservation.table_id, Reservation.reservation_time, Reservation.number_of_guests, Reservation.status]
    column_filters = [Reservation.user_id, Reservation.table_id, Reservation.reservation_time, Reservation.number_of_guests, Reservation.status]
    column_sortable_list = [Reservation.user_id, Reservation.table_id, Reservation.reservation_time, Reservation.number_of_guests, Reservation.status]

class DessertModelForAdmin(ModelView, model=Dessert):
    column_list = [Dessert.id, Dessert.name, Dessert.description, Dessert.price, Dessert.image_url]
    column_searchable_list = [Dessert.name, Dessert.description, Dessert.price, Dessert.image_url]
    column_filters = [Dessert.name, Dessert.description, Dessert.price, Dessert.image_url]
    column_sortable_list = [Dessert.name, Dessert.description, Dessert.price, Dessert.image_url]

class DonerModelForAdmin(ModelView, model=Doner):
    column_list = [Doner.id, Doner.name, Doner.description, Doner.price, Doner.image_url]
    column_searchable_list = [Doner.name, Doner.description, Doner.price, Doner.image_url]
    column_filters = [Doner.name, Doner.description, Doner.price, Doner.image_url]
    column_sortable_list = [Doner.name, Doner.description, Doner.price, Doner.image_url]

class DrinkModelForAdmin(ModelView, model=Drink):
    column_list = [Drink.id, Drink.name, Drink.description, Drink.price, Drink.image_url]
    column_searchable_list = [Drink.name, Drink.description, Drink.price, Drink.image_url]
    column_filters = [Drink.name, Drink.description, Drink.price, Drink.image_url]
    column_sortable_list = [Drink.name, Drink.description, Drink.price, Drink.image_url]

class KebabModelForAdmin(ModelView, model=Kebab):
    column_list = [Kebab.id, Kebab.name, Kebab.description, Kebab.price, Kebab.image_url]
    column_searchable_list = [Kebab.name, Kebab.description, Kebab.price, Kebab.image_url]
    column_filters = [Kebab.name, Kebab.description, Kebab.price, Kebab.image_url]
    column_sortable_list = [Kebab.name, Kebab.description, Kebab.price, Kebab.image_url]

class SaladModelForAdmin(ModelView, model=Salad):
    column_list = [Salad.id, Salad.name, Salad.description, Salad.price, Salad.image_url]
    column_searchable_list = [Salad.name, Salad.description, Salad.price, Salad.image_url]
    column_filters = [Salad.name, Salad.description, Salad.price, Salad.image_url]
    column_sortable_list = [Salad.name, Salad.description, Salad.price, Salad.image_url]

class CommentModelForAdmin(ModelView, model=Comment):
    column_list = [Comment.id, Comment.user_id, Comment.product_id, Comment.content, Comment.rating]
    column_searchable_list = [Comment.user_id, Comment.product_id, Comment.content, Comment.rating]
    column_filters = [Comment.user_id, Comment.product_id, Comment.content, Comment.rating]
    column_sortable_list = [Comment.user_id, Comment.product_id, Comment.content, Comment.rating]


admin.add_view(UserModelForAdmin)
admin.add_view(TableModelForAdmin)
admin.add_view(ReservationModelForAdmin)
admin.add_view(DessertModelForAdmin)
admin.add_view(DonerModelForAdmin)
admin.add_view(DrinkModelForAdmin)
admin.add_view(KebabModelForAdmin)
admin.add_view(SaladModelForAdmin)
admin.add_view(CommentModelForAdmin)

########## SQL ADMIN CONFIG ##########



### ROUTES ###
app.include_router(UserRouter, prefix="/api")
app.include_router(TableRouter, prefix="/api")
app.include_router(ReservationRouter, prefix="/api")
app.include_router(DessertRouter, prefix="/api")
app.include_router(DonerRouter, prefix="/api")
app.include_router(DrinkRouter, prefix="/api")
app.include_router(KebabRouter, prefix="/api")
app.include_router(SaladRouter, prefix="/api")
app.include_router(FavouriteProductRouter, prefix="/api")
app.include_router(CommentRouter, prefix="/api")
app.include_router(CartRouter, prefix="/api")
app.include_router(OrderRouter, prefix="/api")
app.include_router(PaymentRouter, prefix="/api")
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