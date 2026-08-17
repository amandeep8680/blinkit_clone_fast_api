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
from app.routes.brand_routes import router as brand_router
from app.routes.category_routes import router as category_router
from app.routes.subcategory_routes import router as subcategory_router
from app.routes.product_routes import (router as product_router,)
from app.routes.product_variant_routes import (router as product_variant_router,)
from app.routes.product_image_routes import (router as product_image_router,)
from app.routes.branch_inventory_routes import (router as branch_inventory_router ,)
from app.routes.customer_routes import router as customer_router


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
app.include_router(brand_router)
app.include_router(category_router)
app.include_router(subcategory_router)
app.include_router(product_router)
app.include_router(product_variant_router)
app.include_router(product_image_router)
app.include_router(branch_inventory_router)
app.include_router(customer_router)



