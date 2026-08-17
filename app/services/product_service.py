from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.models.brand_model import Brand
from app.models.subcategory_model import SubCategory

from app.schemas.product_schema import (
    ProductCreate,
    ProductUpdate,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from app.exceptions import messages as msg


class ProductService:

    def create_product(
        self,
        db: Session,
        data: ProductCreate,
    ):
        """
        Create a new product.

        Client provides:
        - brand_unique_id
        - subcategory_unique_id

        Internal database IDs are resolved
        before creating the product.
        """

        # Check Brand
        brand = (
            db.query(Brand)
            .filter(
                Brand.unique_id
                == data.brand_unique_id
            )
            .first()
        )

        if not brand:
            raise NotFoundException(
                msg.BRAND_NOT_FOUND
            )

        # Check SubCategory
        subcategory = (
            db.query(SubCategory)
            .filter(
                SubCategory.unique_id
                == data.subcategory_unique_id
            )
            .first()
        )

        if not subcategory:
            raise NotFoundException(
                msg.SUBCATEGORY_NOT_FOUND
            )

        # Check duplicate Product
        existing_product = (
            db.query(Product)
            .filter(
                (Product.name == data.name)
                | (Product.slug == data.slug)
            )
            .first()
        )

        if existing_product:
            raise ConflictException(
                msg.PRODUCT_ALREADY_EXISTS
            )

        product = Product(
            name=data.name,
            slug=data.slug,
            description=data.description,
            brand_id=brand.id,
            subcategory_id=subcategory.id,
            is_active=data.is_active,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product


    def get_product(
        self,
        db: Session,
        product_unique_id: str,
    ):
        """
        Get a single product by unique_id.
        """

        product = (
            db.query(Product)
            .filter(
                Product.unique_id
                == product_unique_id
            )
            .first()
        )

        if not product:
            raise NotFoundException(
                msg.PRODUCT_NOT_FOUND
            )

        return product


    def get_all_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get all products.
        """

        return (
            db.query(Product)
            .order_by(
                Product.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_active_products(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get only active products.
        """

        return (
            db.query(Product)
            .filter(
                Product.is_active.is_(True)
            )
            .order_by(
                Product.name.asc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def update_product(
        self,
        db: Session,
        product_unique_id: str,
        data: ProductUpdate,
    ):
        """
        Partially update Product.
        """

        product = self.get_product(
            db,
            product_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_product = (
                db.query(Product)
                .filter(
                    Product.name
                    == update_data["name"],
                    Product.id != product.id,
                )
                .first()
            )

            if existing_product:
                raise ConflictException(
                    msg.PRODUCT_NAME_ALREADY_EXISTS
                )

        if "slug" in update_data:
            existing_product = (
                db.query(Product)
                .filter(
                    Product.slug
                    == update_data["slug"],
                    Product.id != product.id,
                )
                .first()
            )

            if existing_product:
                raise ConflictException(
                    msg.PRODUCT_SLUG_ALREADY_EXISTS
                )

        for field, value in update_data.items():
            setattr(
                product,
                field,
                value,
            )

        db.commit()
        db.refresh(product)

        return product


    def activate_product(
        self,
        db: Session,
        product_unique_id: str,
    ):
        """
        Activate Product.
        """

        product = self.get_product(
            db,
            product_unique_id,
        )

        if product.is_active:
            raise BadRequestException(
                msg.PRODUCT_ALREADY_ACTIVE
            )

        product.is_active = True

        db.commit()
        db.refresh(product)

        return product


    def deactivate_product(
        self,
        db: Session,
        product_unique_id: str,
    ):
        """
        Deactivate Product.
        """

        product = self.get_product(
            db,
            product_unique_id,
        )

        if not product.is_active:
            raise BadRequestException(
                msg.PRODUCT_ALREADY_INACTIVE
            )

        product.is_active = False

        db.commit()
        db.refresh(product)

        return product


    def delete_product(
        self,
        db: Session,
        product_unique_id: str,
    ):
        """
        Permanently delete Product.

        Product variants and images will also
        be deleted if cascade relationship is configured.
        """

        product = self.get_product(
            db,
            product_unique_id,
        )

        db.delete(product)
        db.commit()

        return {
            "message": msg.PRODUCT_DELETED
        }