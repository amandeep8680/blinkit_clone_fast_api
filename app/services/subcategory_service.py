from sqlalchemy.orm import Session

from app.models.category_model import Category
from app.models.subcategory_model import SubCategory

from app.schemas.subcategory_schema import (
    SubCategoryCreate,
    SubCategoryUpdate,
)

from app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)

from app.exceptions import messages as msg


class SubCategoryService:

    def create_subcategory(
        self,
        db: Session,
        data: SubCategoryCreate,
    ):
        """
        Create a subcategory under an existing category.

        Client provides category_unique_id.
        Internally we store Category.id in category_id.
        """

        category = (
            db.query(Category)
            .filter(
                Category.unique_id
                == data.category_unique_id
            )
            .first()
        )

        if not category:
            raise NotFoundException(
                msg.CATEGORY_NOT_FOUND
            )

        existing_subcategory = (
            db.query(SubCategory)
            .filter(
                (SubCategory.name == data.name)
                | (SubCategory.slug == data.slug)
            )
            .first()
        )

        if existing_subcategory:
            raise ConflictException(
                msg.SUBCATEGORY_ALREADY_EXISTS
            )

        subcategory = SubCategory(
            name=data.name,
            slug=data.slug,
            image_url=data.image_url,
            is_active=data.is_active,
            category_id=category.id,
        )

        db.add(subcategory)
        db.commit()
        db.refresh(subcategory)

        return subcategory


    def get_subcategory(
        self,
        db: Session,
        subcategory_unique_id: str,
    ):
        """
        Get a single subcategory by unique_id.
        """

        subcategory = (
            db.query(SubCategory)
            .filter(
                SubCategory.unique_id
                == subcategory_unique_id
            )
            .first()
        )

        if not subcategory:
            raise NotFoundException(
                msg.SUBCATEGORY_NOT_FOUND
            )

        return subcategory


    def get_all_subcategories(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get all subcategories.
        """

        return (
            db.query(SubCategory)
            .order_by(
                SubCategory.created_at.desc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_active_subcategories(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
    ):
        """
        Get only active subcategories.
        """

        return (
            db.query(SubCategory)
            .filter(
                SubCategory.is_active.is_(True)
            )
            .order_by(
                SubCategory.name.asc()
            )
            .offset(skip)
            .limit(limit)
            .all()
        )


    def get_subcategories_by_category(
        self,
        db: Session,
        category_unique_id: str,
    ):
        """
        Return all subcategories belonging
        to a specific category.
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

        return (
            db.query(SubCategory)
            .filter(
                SubCategory.category_id
                == category.id
            )
            .order_by(
                SubCategory.name.asc()
            )
            .all()
        )


    def update_subcategory(
        self,
        db: Session,
        subcategory_unique_id: str,
        data: SubCategoryUpdate,
    ):
        """
        Partially update a subcategory.
        """

        subcategory = self.get_subcategory(
            db,
            subcategory_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "name" in update_data:
            existing_subcategory = (
                db.query(SubCategory)
                .filter(
                    SubCategory.name
                    == update_data["name"],
                    SubCategory.id
                    != subcategory.id,
                )
                .first()
            )

            if existing_subcategory:
                raise ConflictException(
                    msg.SUBCATEGORY_NAME_ALREADY_EXISTS
                )

        if "slug" in update_data:
            existing_subcategory = (
                db.query(SubCategory)
                .filter(
                    SubCategory.slug
                    == update_data["slug"],
                    SubCategory.id
                    != subcategory.id,
                )
                .first()
            )

            if existing_subcategory:
                raise ConflictException(
                    msg.SUBCATEGORY_SLUG_ALREADY_EXISTS
                )

        for field, value in update_data.items():
            setattr(
                subcategory,
                field,
                value,
            )

        db.commit()
        db.refresh(subcategory)

        return subcategory


    def activate_subcategory(
        self,
        db: Session,
        subcategory_unique_id: str,
    ):
        """
        Activate a subcategory.
        """

        subcategory = self.get_subcategory(
            db,
            subcategory_unique_id,
        )

        if subcategory.is_active:
            raise BadRequestException(
                msg.SUBCATEGORY_ALREADY_ACTIVE
            )

        subcategory.is_active = True

        db.commit()
        db.refresh(subcategory)

        return subcategory


    def deactivate_subcategory(
        self,
        db: Session,
        subcategory_unique_id: str,
    ):
        """
        Deactivate a subcategory.
        """

        subcategory = self.get_subcategory(
            db,
            subcategory_unique_id,
        )

        if not subcategory.is_active:
            raise BadRequestException(
                msg.SUBCATEGORY_ALREADY_INACTIVE
            )

        subcategory.is_active = False

        db.commit()
        db.refresh(subcategory)

        return subcategory


    def delete_subcategory(
        self,
        db: Session,
        subcategory_unique_id: str,
    ):
        """
        Permanently delete a subcategory.
        """

        subcategory = self.get_subcategory(
            db,
            subcategory_unique_id,
        )

        db.delete(subcategory)
        db.commit()

        return {
            "message": msg.SUBCATEGORY_DELETED
        }