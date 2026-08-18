from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Annotated
from  app.database.database import get_db
from  app.auth.authorization import require_roles

from  app.constants.roles import (
    SUPER_ADMIN,
    CUSTOMER,
)

from  app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
    CustomerWithAddressesResponse,
    CustomerAddressCreate,
    CustomerAddressUpdate,
    CustomerAddressResponse,
)

from  app.services.customer_service import CustomerService


customer_service = CustomerService()
# Database dependency
DBSession = Annotated[
    Session,
    Depends(get_db),
]

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)




# =========================================================
# Register Customer
# =========================================================
# Public route.
# Customer does not need JWT before registration.
@router.post(
    "/register",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_customer_route(
    data: CustomerCreate,
    db: DBSession,
):
    return customer_service.create_customer(
        db,
        data,
    )


# =========================================================
# Get All Customers
# =========================================================
# Super Admin only.
@router.get(
    "",
    response_model=list[CustomerResponse],
)
def get_all_customers_route(
    db: DBSession,
    skip: int = 0,
    limit: int = 100,
    
    current_user=Depends(
        require_roles(SUPER_ADMIN)
    ),
):
    return customer_service.get_all_customers(
        db,
        skip,
        limit,
    )


# =========================================================
# Get Customer With Addresses
# =========================================================
@router.get(
    "/{customer_unique_id}/details",
    response_model=CustomerWithAddressesResponse,
)
def get_customer_with_address_route(
    customer_unique_id: str,
    db: DBSession,
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.get_customer(
        db,
        customer_unique_id,
    )


# =========================================================
# Get Single Customer
# =========================================================
@router.get(
    "/{customer_unique_id}",
    response_model=CustomerResponse,
)
def get_customer_route(
    customer_unique_id: str,
    db: DBSession,
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.get_customer(
        db,
        customer_unique_id,
    )


# =========================================================
# Update Customer
# =========================================================
@router.patch(
    "/{customer_unique_id}",
    response_model=CustomerResponse,
)
def update_customer_route(
    customer_unique_id: str,
    data: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.update_customer(
        db,
        customer_unique_id,
        data,
    )


# =========================================================
# Activate Customer
# =========================================================
# Usually admin operation.
@router.patch(
    "/{customer_unique_id}/activate",
    response_model=CustomerResponse,
)
def activate_customer_route(
    customer_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN)
    ),
):
    return customer_service.activate_customer(
        db,
        customer_unique_id,
    )


# =========================================================
# Deactivate Customer
# =========================================================
@router.patch(
    "/{customer_unique_id}/deactivate",
    response_model=CustomerResponse,
)
def deactivate_customer_route(
    customer_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN)
    ),
):
    return customer_service.deactivate_customer(
        db,
        customer_unique_id,
    )


# =========================================================
# Delete Customer
# =========================================================
@router.delete(
    "/{customer_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_customer_route(
    customer_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN)
    ),
):
    return customer_service.delete_customer(
        db,
        customer_unique_id,
    )


# =========================================================
# Add Customer Address
# =========================================================
@router.post(
    "/{customer_unique_id}/addresses",
    response_model=CustomerAddressResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_address_route(
    customer_unique_id: str,
    data: CustomerAddressCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.create_address(
        db,
        customer_unique_id,
        data,
    )


# =========================================================
# Get Customer Addresses
# =========================================================
@router.get(
    "/{customer_unique_id}/addresses",
    response_model=list[CustomerAddressResponse],
)
def get_customer_addresses_route(
    customer_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.get_customer_addresses(
        db,
        customer_unique_id,
    )


# =========================================================
# Get Single Address
# =========================================================
@router.get(
    "/{customer_unique_id}/addresses/{address_unique_id}",
    response_model=CustomerAddressResponse,
)
def get_address_route(
    customer_unique_id: str,
    address_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.get_address(
        db,
        customer_unique_id,
        address_unique_id,
    )


# =========================================================
# Update Address
# =========================================================
@router.patch(
    "/{customer_unique_id}/addresses/{address_unique_id}",
    response_model=CustomerAddressResponse,
)
def update_address_route(
    customer_unique_id: str,
    address_unique_id: str,
    data: CustomerAddressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.update_address(
        db,
        customer_unique_id,
        address_unique_id,
        data,
    )


# =========================================================
# Activate Address
# =========================================================
@router.patch(
    "/{customer_unique_id}/addresses/{address_unique_id}/activate",
    response_model=CustomerAddressResponse,
)
def activate_address_route(
    customer_unique_id: str,
    address_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.activate_address(
        db,
        customer_unique_id,
        address_unique_id,
    )


# =========================================================
# Deactivate Address
# =========================================================
@router.patch(
    "/{customer_unique_id}/addresses/{address_unique_id}/deactivate",
    response_model=CustomerAddressResponse,
)
def deactivate_address_route(
    customer_unique_id: str,
    address_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.deactivate_address(
        db,
        customer_unique_id,
        address_unique_id,
    )


# =========================================================
# Delete Address
# =========================================================
@router.delete(
    "/{customer_unique_id}/addresses/{address_unique_id}",
    status_code=status.HTTP_200_OK,
)
def delete_address_route(
    customer_unique_id: str,
    address_unique_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(SUPER_ADMIN, CUSTOMER)
    ),
):
    return customer_service.delete_address(
        db,
        customer_unique_id,
        address_unique_id,
    )