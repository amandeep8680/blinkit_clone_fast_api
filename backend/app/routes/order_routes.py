from fastapi import (
    APIRouter,
    Depends,
    status,
)

from typing import Annotated
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.auth.authorization import require_roles
from app.constants import roles

from app.schemas.order_schema import (
    OrderCreate,
    OrderResponse,
    OrderDetailResponse,
    OrderStatusUpdate,
    PaymentStatusUpdate,
)

from app.services.order_service import (
    OrderService,
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


order_service = OrderService()


DBSession = Annotated[
    Session,
    Depends(get_db),
]


CurrentCustomer = Annotated[
    object,
    Depends(
        require_roles(
            roles.CUSTOMER
        )
    ),
]


AdminOrManager = Annotated[
    object,
    Depends(
        require_roles(
            roles.SUPER_ADMIN,
            roles.BRANCH_MANAGER,
        )
    ),
]


# =========================================================
# Place Order
# =========================================================
# Creates Order from logged-in customer's active cart.
@router.post(
    "",
    response_model=OrderDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def place_order(
    data: OrderCreate,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return order_service.create_order(
        db=db,
        customer=current_user,
        data=data,
    )


# =========================================================
# Get My Orders
# =========================================================
@router.get(
    "/my",
    response_model=list[OrderResponse],
)
def get_my_orders(
    db: DBSession,
    current_user: CurrentCustomer,
    skip: int = 0,
    limit: int = 100,
):
    return order_service.get_customer_orders(
        db=db,
        customer=current_user,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Get My Order Details
# =========================================================
@router.get(
    "/my/{order_unique_id}",
    response_model=OrderDetailResponse,
)
def get_my_order(
    order_unique_id: str,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return order_service.get_customer_order(
        db=db,
        customer=current_user,
        order_unique_id=order_unique_id,
    )


# =========================================================
# Cancel My Order
# =========================================================
@router.patch(
    "/my/{order_unique_id}/cancel",
    response_model=OrderDetailResponse,
)
def cancel_my_order(
    order_unique_id: str,
    db: DBSession,
    current_user: CurrentCustomer,
):
    return order_service.cancel_order(
        db=db,
        customer=current_user,
        order_unique_id=order_unique_id,
    )


# =========================================================
# Get All Orders
# =========================================================
# Super Admin / Branch Manager
@router.get(
    "",
    response_model=list[OrderResponse],
)
def get_all_orders(
    db: DBSession,
    current_user: AdminOrManager,
    skip: int = 0,
    limit: int = 100,
):
    return order_service.get_all_orders(
        db=db,
        skip=skip,
        limit=limit,
    )


# =========================================================
# Admin / Manager Get Order Detail
# =========================================================
@router.get(
    "/{order_unique_id}",
    response_model=OrderDetailResponse,
)
def get_order(
    order_unique_id: str,
    db: DBSession,
    current_user: AdminOrManager,
):
    return order_service.get_order(
        db=db,
        order_unique_id=order_unique_id,
    )


# =========================================================
# Update Order Status
# =========================================================
@router.patch(
    "/{order_unique_id}/status",
    response_model=OrderDetailResponse,
)
def update_order_status(
    order_unique_id: str,
    data: OrderStatusUpdate,
    db: DBSession,
    current_user: AdminOrManager,
):
    return order_service.update_order_status(
        db=db,
        current_user=current_user,
        order_unique_id=order_unique_id,
        data=data,
    )


# =========================================================
# Update Payment Status
# =========================================================
@router.patch(
    "/{order_unique_id}/payment-status",
    response_model=OrderDetailResponse,
)
def update_payment_status(
    order_unique_id: str,
    data: PaymentStatusUpdate,
    db: DBSession,
    current_user: AdminOrManager,
):
    return order_service.update_payment_status(
        db=db,
        order_unique_id=order_unique_id,
        data=data,
    )