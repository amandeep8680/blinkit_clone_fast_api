from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import engine
from app.routes.admin_routes import router as user_router
from app.middleware.logging_middleware import (logging_middleware)
from app.routes.auth_routes import router as auth_router
from app.routes.branch_routes import router as branch_router
from app.routes.branchmanager_routes import (router as branch_manager_router)


# -----------------------------------
# Application Lifespan
# -----------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Runs when the application starts and shuts down.
    Currently used to test database connectivity.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("✅ Database connected successfully!")

    except SQLAlchemyError as e:
        print(f"❌ Database connection failed: {e}")

    yield


# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)
# -----------------------------------
# FastAPI Application
# -----------------------------------

app = FastAPI(
    title="Blinkit API",
    version="1.0.0",
    description="Backend APIs for Blinkit Clone",
    lifespan=lifespan,
)


# -----------------------------------
# Register Logging-Middleware
# -----------------------------------
app.middleware("http")(logging_middleware)


# -----------------------------------
# Routers
# -----------------------------------
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(branch_router)
app.include_router(branch_manager_router)

