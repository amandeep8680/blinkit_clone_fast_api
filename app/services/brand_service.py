from sqlalchemy.orm import Session

from app.models.brand_model import Brand
from app.schemas.brand_schema import (
    BrandCreate,
    BrandUpdate,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
    ConflictException,
)

from app.exceptions import messages as msg


class BrandService:

    def create_brand(
        self,
        db: Session,
        data: BrandCreate,
    ):
        """
        Create a new brand.
        """

        existing_brand = (
            db.query(Brand)
            .filter(
                (Brand.name == data.name)
                | (Brand.slug == data.slug)
            )
            .first()
        )

        if existing_brand:
            raise ConflictException(
                msg.BRAND_ALREADY_EXISTS
            )

        brand = Brand(
            name=data.name,
            slug=data.slug,
            logo_url=data.logo_url,
            is_active=data.is_active,
        )

        db.add(brand)
        db.commit()
        db.refresh(brand)

        return brand


    def get_brand(
        self,
        db: Session,
        brand_unique_id: str,
    ):
        """
        Get a single brand by unique id.
        """

        brand = (
            db.query(Brand)
            .filter(
                Brand.unique_id
                == brand_unique_id
            )
            .first()
        )

        if not brand:
            raise NotFoundException(
                msg.BRAND_NOT_FOUND
            )

        return brand


    def get_all_brands(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get all brands.
        """

        return (
            db.query(Brand)
            .order_by(
                Brand.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_active_brands(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get only active brands.
        """

        return (
            db.query(Brand)
            .filter(
                Brand.is_active.is_(True)
            )
            .order_by(
                Brand.name.asc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def update_brand(
        self,
        db: Session,
        brand_unique_id: str,
        data: BrandUpdate,
    ):
        """
        Update an existing brand.
        """

        brand = self.get_brand(
            db,
            brand_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_brand = (
                db.query(Brand)
                .filter(
                    Brand.name
                    == update_data["name"],
                    Brand.id != brand.id,
                )
                .first()
            )

            if existing_brand:
                raise ConflictException(
                    msg.BRAND_NAME_ALREADY_EXISTS
                )

        if "slug" in update_data:
            existing_brand = (
                db.query(Brand)
                .filter(
                    Brand.slug
                    == update_data["slug"],
                    Brand.id != brand.id,
                )
                .first()
            )

            if existing_brand:
                raise ConflictException(
                    msg.BRAND_SLUG_ALREADY_EXISTS
                )

        for field, value in update_data.items():
            setattr(
                brand,
                field,
                value,
            )

        db.commit()
        db.refresh(brand)

        return brand


    def activate_brand(
        self,
        db: Session,
        brand_unique_id: str,
    ):
        """
        Activate a brand.
        """

        brand = self.get_brand(
            db,
            brand_unique_id,
        )

        if brand.is_active:
            raise BadRequestException(
                msg.BRAND_ALREADY_ACTIVE
            )

        brand.is_active = True

        db.commit()
        db.refresh(brand)

        return brand


    def deactivate_brand(
        self,
        db: Session,
        brand_unique_id: str,
    ):
        """
        Deactivate a brand.
        """

        brand = self.get_brand(
            db,
            brand_unique_id,
        )

        if not brand.is_active:
            raise BadRequestException(
                msg.BRAND_ALREADY_INACTIVE
            )

        brand.is_active = False

        db.commit()
        db.refresh(brand)

        return brand

    def delete_brand(
        self,
        db: Session,
        brand_unique_id: str,
    ):
        brand = self.get_brand(
            db,
            brand_unique_id,
        )

        if brand.products:
            raise BadRequestException(
                msg.BRAND_HAS_PRODUCTS
            )

        db.delete(brand)
        db.commit()

        return {
            "message": msg.BRAND_DELETED
        }