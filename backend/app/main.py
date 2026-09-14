from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.database.database import engine

from app.routes.admin_routes import router as user_router
from app.routes.auth_routes import router as auth_router
from app.routes.branch_routes import router as branch_router
from app.routes.branchmanager_routes import router as branch_manager_router
from app.routes.brand_routes import router as brand_router
from app.routes.category_routes import router as category_router
from app.routes.subcategory_routes import router as subcategory_router
from app.routes.product_routes import router as product_router
from app.routes.product_variant_routes import router as product_variant_router
from app.routes.product_image_routes import router as product_image_router
from app.routes.branch_inventory_routes import router as branch_inventory_router
from app.routes.customer_routes import router as customer_router
from app.routes.cart_routes import router as cart_router
from app.routes.branch_catalog_routes import router as branch_catalog_router
from app.routes.order_routes import (router as order_router,)
from app.routes.cart_event_routes import (router as cart_event_router,)

from app.core.logging_config import setup_logging
from app.middleware.logging_middleware import logging_middleware
from app.middleware.rate_limit_middleware import rate_limit_middleware
from app.middleware.cors import setup_cors


# -----------------------------------
# Application Lifespan
# -----------------------------------

logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        logger.info(
            "Database connected successfully"
        )

    except SQLAlchemyError:
        logger.critical(
            "Database connection failed",
            exc_info=True,
        )

    yield


# -----------------------------------
# Logging configuration
# -----------------------------------
setup_logging()
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s",
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
@app.get("/test-error")
async def test_error():
    result = 10 / 0
    return {"result": result}

# Fixed Window test API
@app.get("/test-fixed")
async def test_fixed():
    return {
        "message": "Fixed window request allowed"
    }


# Sliding Window test API
@app.get("/test-sliding")
async def test_sliding():
    return {
        "message": "Sliding window request allowed"
    }


# Token Bucket test API
@app.get("/test-token")
async def test_token():
    return {
        "message": "Token bucket request allowed"
    }


# Leaky Bucket test API
@app.get("/test-leaky")
async def test_leaky():
    return {
        "message": "Leaky bucket request allowed"
    }

import logging

logger = logging.getLogger("app")


@app.get("/test-info")
async def test_info():
    logger.info("This is INFO log")
    return {"message": "info logged"}


@app.get("/test-warning")
async def test_warning():
    logger.warning("This is WARNING log")
    return {"message": "warning logged"}


@app.get("/test-error")
async def test_error():
    return 10 / 0


@app.get("/test-critical")
async def test_critical():
    logger.critical("This is CRITICAL log")
    return {"message": "critical logged"}
# -----------------------------------
# Logging Middleware
# -----------------------------------

app.middleware("http")(logging_middleware)
app.middleware("http")(
    security_headers_middleware
)

# -----------------------------------
# CORS Middleware
# -----------------------------------

setup_cors(app)


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
app.include_router(branch_catalog_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(cart_event_router)