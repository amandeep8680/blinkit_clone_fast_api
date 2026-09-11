from sqlalchemy.orm import Session
from app.core.cache import delete_cache_pattern
from app.core.cache_keys import (
    ACTIVE_CATEGORIES_CACHE_PATTERN,
)
from  app.models.category_model import Category
from  app.schemas.category_schema import (
    CategoryCreate,
    CategoryUpdate,
)

from  app.exceptions.custom_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
)
from fastapi.encoders import jsonable_encoder
from  app.exceptions import messages as msg

from app.core.cache import get_cache, set_cache ,get_or_set_cache
from app.core.cache_keys import active_categories_cache_key

def delete_cache():
    delete_cache_pattern(
    ACTIVE_CATEGORIES_CACHE_PATTERN
)

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
        delete_cache()

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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # #  Direct simple redis 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    # def get_active_categories(
    #     self,
    #     db: Session,
    #     skip: int = 0,
    #     limit: int = 100,
    # ):
    #     """
    #     Get only active categories.
    #     """


    #     # Make cache keys
    #     cache_key =  active_categories_cache_key(
    #         skip=skip,
    #         limit=limit,
    #         )

    #     # check redis
    #     cached_data = get_cache(cache_key)

    #     if cached_data is not None:
    #         print(f"✅ CACHE HIT | key={cache_key}")
    #         return cached_data
        
    #     print(f"❌ CACHE MISS | key={cache_key}")
    #     # if cache miss 
    #     categories =  (
    #         db.query(Category)
    #         .filter(
    #             Category.is_active.is_(True)
    #         )
    #         .order_by(
    #             Category.name.asc()
    #         )
    #         .offset(skip)
    #         .limit(limit)
    #         .all()
    #     )

    #     # convert sqlalchemyibjec tin to JSON serializable
    #     data = jsonable_encoder(categories)

    #     # store in redis
    #     set_cache(
    #         key=cache_key,
    #         data = data , 
    #         ttl = 60
    #     )

    #     return data



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# # #  Reusable redis cache 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def get_active_categories(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
            ):

        cache_key = active_categories_cache_key(
            skip=skip,
            limit=limit,
        )

        def fetch_categories():
            categories = (
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

            return jsonable_encoder(categories)

        return get_or_set_cache(
            key=cache_key,
            fetch_function=fetch_categories,
            ttl=60,
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
        delete_cache_pattern(
            ACTIVE_CATEGORIES_CACHE_PATTERN
        )

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
        delete_cache_pattern(
            ACTIVE_CATEGORIES_CACHE_PATTERN
        )

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
        delete_cache_pattern(
            ACTIVE_CATEGORIES_CACHE_PATTERN
        )

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
        delete_cache_pattern(
                    ACTIVE_CATEGORIES_CACHE_PATTERN
                )
        return {
            "message": msg.CATEGORY_DELETED
        }