from sqlalchemy.orm import Session

from app.models.customer_model import (
    Customer,
    CustomerAddress,
)

from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerUpdate,
    CustomerAddressCreate,
    CustomerAddressUpdate,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from app.exceptions import messages as msg

from app.core.security import hash_password


class CustomerService:

    # =====================================================
    # Create Customer
    # =====================================================

   
    def create_customer(
        self,
        db: Session,
        customer: CustomerCreate,
    ):
        """
        Create a new customer account.
        """

        existing_email = (
            db.query(Customer)
            .filter(Customer.email == customer.email)
            .first()
        )

        if existing_email:
            raise ConflictException(
                msg.CUSTOMER_EMAIL_ALREADY_EXISTS
            )

        existing_phone = (
            db.query(Customer)
            .filter(Customer.phone == customer.phone)
            .first()
        )

        if existing_phone:
            raise ConflictException(
                msg.CUSTOMER_PHONE_ALREADY_EXISTS
            )

        new_customer = Customer(
            name=customer.name,
            email=customer.email,
            phone=customer.phone,
            password_hash=hash_password(
                customer.password
            ),
            role="customer",
        )

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

        return new_customer



    # =====================================================
    # Get Customer
    # =====================================================

    

    def get_customer(
        self,
        db: Session,
        customer_unique_id: str,
    ):
        customer = (
            db.query(Customer)
            .filter(
                Customer.unique_id
                == customer_unique_id
            )
            .first()
        )

        if not customer:
            raise NotFoundException(
                msg.CUSTOMER_NOT_FOUND
            )

        return customer


    # =====================================================
    # Get All Customers
    # =====================================================

    def get_all_customers(self, db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(Customer)
            .order_by(Customer.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )


    # =====================================================
    # Update Customer
    # =====================================================

    def update_customer(
        self,
        db: Session,
        customer_unique_id: str,
        data: CustomerUpdate,
    ):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:
            existing_email = (
                db.query(Customer)
                .filter(
                    Customer.email
                    == update_data["email"],
                    Customer.id != customer.id,
                )
                .first()
            )

            if existing_email:
                raise ConflictException(
                    msg.CUSTOMER_EMAIL_ALREADY_EXISTS
                )

        if "phone" in update_data:
            existing_phone = (
                db.query(Customer)
                .filter(
                    Customer.phone
                    == update_data["phone"],
                    Customer.id != customer.id,
                )
                .first()
            )

            if existing_phone:
                raise ConflictException(
                    msg.CUSTOMER_PHONE_ALREADY_EXISTS
                )

        for field, value in update_data.items():
            setattr(
                customer,
                field,
                value,
            )

        db.commit()
        db.refresh(customer)

        return customer

    # =====================================================
    # Activate Customer
    # =====================================================

    def activate_customer(self, db: Session, customer_unique_id: str):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        if customer.is_active:
            raise BadRequestException(
                msg.CUSTOMER_ALREADY_ACTIVE
            )

        customer.is_active = True

        db.commit()
        db.refresh(customer)

        return customer


    # =====================================================
    # Deactivate Customer
    # =====================================================

    def deactivate_customer(self, db: Session, customer_unique_id: str):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        if not customer.is_active:
            raise BadRequestException(
                msg.CUSTOMER_ALREADY_INACTIVE
            )

        customer.is_active = False

        db.commit()
        db.refresh(customer)

        return customer


    # =====================================================
    # Delete Customer
    # =====================================================

    def delete_customer(self, db: Session, customer_unique_id: str):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        db.delete(customer)
        db.commit()

        return {
            "message": msg.CUSTOMER_DELETED
        }


    # =====================================================
    # Create Customer Address
    # =====================================================

    def create_address(
        self,
        db: Session,
        customer_unique_id: str,
        data: CustomerAddressCreate,
    ):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        existing_label = (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.customer_id == customer.id,
                CustomerAddress.label == data.label,
            )
            .first()
        )

        if existing_label:
            raise ConflictException(
                msg.CUSTOMER_ADDRESS_LABEL_ALREADY_EXISTS
            )

        # If this address is going to be default,
        # remove default from previous address.
        if data.is_default:
            (
                db.query(CustomerAddress)
                .filter(
                    CustomerAddress.customer_id == customer.id,
                    CustomerAddress.is_default.is_(True),
                )
                .update(
                    {"is_default": False},
                    synchronize_session=False,
                )
            )

        address = CustomerAddress(
            customer_id=customer.id,
            label=data.label,
            address_line=data.address_line,
            landmark=data.landmark,
            city=data.city,
            state=data.state,
            pincode=data.pincode,
            is_default=data.is_default,
        )

        db.add(address)
        db.commit()
        db.refresh(address)

        return address


    # =====================================================
    # Get Customer Address
    # =====================================================

    def get_address(
        self,
        db: Session,
        customer_unique_id: str,
        address_unique_id: str,
    ):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        address = (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.unique_id == address_unique_id,
                CustomerAddress.customer_id == customer.id,
            )
            .first()
        )

        if not address:
            raise NotFoundException(
                msg.CUSTOMER_ADDRESS_NOT_FOUND
            )

        return address


    # =====================================================
    # Get All Customer Addresses
    # =====================================================

    def get_customer_addresses(self, db: Session, customer_unique_id: str):
        customer = self.get_customer(
            db,
            customer_unique_id,
        )

        return (
            db.query(CustomerAddress)
            .filter(
                CustomerAddress.customer_id == customer.id
            )
            .order_by(
                CustomerAddress.is_default.desc(),
                CustomerAddress.created_at.desc(),
            )
            .all()
        )


    # =====================================================
    # Update Address
    # =====================================================

    def update_address(
        self,
        db: Session,
        customer_unique_id: str,
        address_unique_id: str,
        data: CustomerAddressUpdate,
    ):
        address = self.get_address(
            db,
            customer_unique_id,
            address_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "label" in update_data:
            existing_label = (
                db.query(CustomerAddress)
                .filter(
                    CustomerAddress.customer_id == address.customer_id,
                    CustomerAddress.label == update_data["label"],
                    CustomerAddress.id != address.id,
                )
                .first()
            )

            if existing_label:
                raise ConflictException(
                    msg.CUSTOMER_ADDRESS_LABEL_ALREADY_EXISTS
                )

        # New default address selected.
        if update_data.get("is_default") is True:
            (
                db.query(CustomerAddress)
                .filter(
                    CustomerAddress.customer_id == address.customer_id,
                    CustomerAddress.id != address.id,
                    CustomerAddress.is_default.is_(True),
                )
                .update(
                    {"is_default": False},
                    synchronize_session=False,
                )
            )

        for field, value in update_data.items():
            setattr(address, field, value)

        db.commit()
        db.refresh(address)

        return address


    # =====================================================
    # Activate Address
    # =====================================================

    def activate_address(
        self,
        db: Session,
        customer_unique_id: str,
        address_unique_id: str,
    ):
        address = self.get_address(
            db,
            customer_unique_id,
            address_unique_id,
        )

        if address.is_active:
            raise BadRequestException(
                msg.CUSTOMER_ADDRESS_ALREADY_ACTIVE
            )

        address.is_active = True

        db.commit()
        db.refresh(address)

        return address


    # =====================================================
    # Deactivate Address
    # =====================================================

    def deactivate_address(
        self,
        db: Session,
        customer_unique_id: str,
        address_unique_id: str,
    ):
        address = self.get_address(
            db,
            customer_unique_id,
            address_unique_id,
        )

        if not address.is_active:
            raise BadRequestException(
                msg.CUSTOMER_ADDRESS_ALREADY_INACTIVE
            )

        address.is_active = False

        db.commit()
        db.refresh(address)

        return address


    # =====================================================
    # Delete Address
    # =====================================================

    def delete_address(
        self,
        db: Session,
        customer_unique_id: str,
        address_unique_id: str,
    ):
        address = self.get_address(
            db,
            customer_unique_id,
            address_unique_id,
        )

        db.delete(address)
        db.commit()

        return {
            "message": msg.CUSTOMER_ADDRESS_DELETED
        }