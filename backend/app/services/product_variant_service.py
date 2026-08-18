from sqlalchemy.orm import Session

from  app.models.product_model import Product
from  app.models.product_variant_model import ProductVariant

from  app.schemas.product_variant_schema import (
    ProductVariantCreate,
    ProductVariantUpdate,
)

from  app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class ProductVariantService:

    def create_variant(
        self,
        db: Session,
        data: ProductVariantCreate,
    ):
        """
        Create a Product Variant under
        an existing Product.
        """

        product = (
            db.query(Product)
            .filter(
                Product.unique_id
                == data.product_unique_id
            )
            .first()
        )

        if not product:
            raise NotFoundException(
                msg.PRODUCT_NOT_FOUND
            )

        existing_variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.sku
                == data.sku
            )
            .first()
        )

        if existing_variant:
            raise ConflictException(
                msg.PRODUCT_VARIANT_SKU_ALREADY_EXISTS
            )

        if data.selling_price > data.mrp:
            raise BadRequestException(
                msg.INVALID_PRODUCT_VARIANT_PRICE
            )

        variant = ProductVariant(
            product_id=product.id,
            sku=data.sku,
            value=data.value,
            unit=data.unit,
            mrp=data.mrp,
            selling_price=data.selling_price,
            is_active=data.is_active,
        )

        db.add(variant)
        db.commit()
        db.refresh(variant)

        return variant


    def get_variant(
        self,
        db: Session,
        variant_unique_id: str,
    ):
        """
        Get Product Variant by unique_id.
        """

        variant = (
            db.query(ProductVariant)
            .filter(
                ProductVariant.unique_id
                == variant_unique_id
            )
            .first()
        )

        if not variant:
            raise NotFoundException(
                msg.PRODUCT_VARIANT_NOT_FOUND
            )

        return variant


    def get_all_variants(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get all Product Variants.
        """

        return (
            db.query(ProductVariant)
            .order_by(
                ProductVariant.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_variants_by_product(
        self,
        db: Session,
        product_unique_id: str,
    ):
        """
        Get all variants for one Product.
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

        return (
            db.query(ProductVariant)
            .filter(
                ProductVariant.product_id
                == product.id
            )
            .order_by(
                ProductVariant.created_at.asc()
            )
            .all()
        )


    def update_variant(
        self,
        db: Session,
        variant_unique_id: str,
        data: ProductVariantUpdate,
    ):
        """
        Partially update Product Variant.
        """

        variant = self.get_variant(
            db,
            variant_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "sku" in update_data:
            existing_variant = (
                db.query(ProductVariant)
                .filter(
                    ProductVariant.sku
                    == update_data["sku"],
                    ProductVariant.id
                    != variant.id,
                )
                .first()
            )

            if existing_variant:
                raise ConflictException(
                    msg.PRODUCT_VARIANT_SKU_ALREADY_EXISTS
                )

        # Calculate final values before validating price.
        new_mrp = update_data.get(
            "mrp",
            variant.mrp,
        )

        new_selling_price = update_data.get(
            "selling_price",
            variant.selling_price,
        )

        if new_selling_price > new_mrp:
            raise BadRequestException(
                msg.INVALID_PRODUCT_VARIANT_PRICE
            )

        for field, value in update_data.items():
            setattr(
                variant,
                field,
                value,
            )

        db.commit()
        db.refresh(variant)

        return variant


    def activate_variant(
        self,
        db: Session,
        variant_unique_id: str,
    ):
        """
        Activate Product Variant.
        """

        variant = self.get_variant(
            db,
            variant_unique_id,
        )

        if variant.is_active:
            raise BadRequestException(
                msg.PRODUCT_VARIANT_ALREADY_ACTIVE
            )

        variant.is_active = True

        db.commit()
        db.refresh(variant)

        return variant


    def deactivate_variant(
        self,
        db: Session,
        variant_unique_id: str,
    ):
        """
        Deactivate Product Variant.
        """

        variant = self.get_variant(
            db,
            variant_unique_id,
        )

        if not variant.is_active:
            raise BadRequestException(
                msg.PRODUCT_VARIANT_ALREADY_INACTIVE
            )

        variant.is_active = False

        db.commit()
        db.refresh(variant)

        return variant


    def delete_variant(
        self,
        db: Session,
        variant_unique_id: str,
    ):
        """
        Permanently delete Product Variant.
        """

        variant = self.get_variant(
            db,
            variant_unique_id,
        )

        db.delete(variant)
        db.commit()

        return {
            "message": msg.PRODUCT_VARIANT_DELETED
        }