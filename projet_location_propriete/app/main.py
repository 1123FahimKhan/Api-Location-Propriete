from fastapi import FastAPI

from app.config.env import settings
from app.routers.routers_resetdb import router as resetdb
from app.routers.routers_locations import router as locations_router
from app.routers.routers_proprietaire import router as proprietaire_router
from app.routers.routers_client import router as client_router
from app.routers.routers_admin import router as admin
from app.routers.router_user import router as users

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION
)

app.include_router(users)
app.include_router(locations_router)
app.include_router(admin)
app.include_router(resetdb)
app.include_router(proprietaire_router)
app.include_router(client_router)
