from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from app.exceptions import messages as msg


class CategoryService:

    def create_category(
        self,
        db: Session,
        data: CategoryCreate,
    ):
        """
        Create a new category.
        """

        existing_category = (
            db.query(Category)
            .filter(
                (Category.name == data.name)
                | (Category.slug == data.slug)
            )
            .first()
        )

        if existing_category:
            raise ConflictException(
                msg.CATEGORY_ALREADY_EXISTS
            )

        category = Category(
            name=data.name,
            slug=data.slug,
            image_url=data.image_url,
            is_active=data.is_active,
        )

        db.add(category)
        db.commit()
        db.refresh(category)

        return category


    def get_category(
        self,
        db: Session,
        category_unique_id: str,
    ):
        """
        Get a category using its public unique_id.
        """

        category = (
            db.query(Category)
            .filter(
                Category.unique_id
                == category_unique_id
            )
            .first()
        )

        if not category:
            raise NotFoundException(
                msg.CATEGORY_NOT_FOUND
            )

        return category


    def get_all_categories(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get all categories including
        active and inactive categories.
        """

        return (
            db.query(Category)
            .order_by(
                Category.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_active_categories(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get only active categories.
        """

        return (
            db.query(Category)
            .filter(
                Category.is_active.is_(True)
            )
            .order_by(
                Category.name.asc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def update_category(
        self,
        db: Session,
        category_unique_id: str,
        data: CategoryUpdate,
    ):
        """
        Partially update a category.
        """

        category = self.get_category(
            db,
            category_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_category = (
                db.query(Category)
                .filter(
                    Category.name
                    == update_data["name"],
                    Category.id != category.id,
                )
                .first()
            )

            if existing_category:
                raise ConflictException(
                    msg.CATEGORY_NAME_ALREADY_EXISTS
                )

        if "slug" in update_data:
            existing_category = (
                db.query(Category)
                .filter(
                    Category.slug
                    == update_data["slug"],
                    Category.id != category.id,
                )
                .first()
            )

            if existing_category:
                raise ConflictException(
                    msg.CATEGORY_SLUG_ALREADY_EXISTS
                )

        for field, value in update_data.items():
            setattr(
                category,
                field,
                value,
            )

        db.commit()
        db.refresh(category)

        return category


    def activate_category(
        self,
        db: Session,
        category_unique_id: str,
    ):
        """
        Activate a category.
        """

        category = self.get_category(
            db,
            category_unique_id,
        )

        if category.is_active:
            raise BadRequestException(
                msg.CATEGORY_ALREADY_ACTIVE
            )

        category.is_active = True

        db.commit()
        db.refresh(category)

        return category


    def deactivate_category(
        self,
        db: Session,
        category_unique_id: str,
    ):
        """
        Deactivate a category.
        """

        category = self.get_category(
            db,
            category_unique_id,
        )

        if not category.is_active:
            raise BadRequestException(
                msg.CATEGORY_ALREADY_INACTIVE
            )

        category.is_active = False

        db.commit()
        db.refresh(category)

        return category


    def delete_category(
        self,
        db: Session,
        category_unique_id: str,
    ):
        """
        Permanently delete a category.

        Because Category -> SubCategory relationship
        uses cascade='all, delete-orphan',
        related subcategories may also be deleted.
        """

        category = self.get_category(
            db,
            category_unique_id,
        )

        db.delete(category)
        db.commit()

        return {
            "message": msg.CATEGORY_DELETED
        }