from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite

# create FastAPI application
app = FastAPI()

# create AdminSite instance
site = AdminSite(settings=Settings(database_url_async='sqlite+aiosqlite:///amisadmin.db'))

# mount AdminSite instance
site.mount_app(app)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app)