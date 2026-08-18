from sqlalchemy.orm import Session

from  app.models.product_model import Product
from  app.models.product_image_model import ProductImage

from  app.schemas.product_image_schema import (
    ProductImageCreate,
    ProductImageUpdate,
)

from  app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class ProductImageService:

    def create_image(
        self,
        db: Session,
        data: ProductImageCreate,
    ):
        """
        Add an image to an existing Product.
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

        # If new image is marked primary,
        # remove primary status from current image.
        if data.is_primary:
            current_primary = (
                db.query(ProductImage)
                .filter(
                    ProductImage.product_id
                    == product.id,
                    ProductImage.is_primary.is_(True),
                )
                .first()
            )

            if current_primary:
                current_primary.is_primary = False

        image = ProductImage(
            product_id=product.id,
            image_url=data.image_url,
            sort_order=data.sort_order,
            is_primary=data.is_primary,
        )

        db.add(image)
        db.commit()
        db.refresh(image)

        return image


    def get_image(
        self,
        db: Session,
        image_unique_id: str,
    ):
        """
        Get Product Image by unique_id.
        """

        image = (
            db.query(ProductImage)
            .filter(
                ProductImage.unique_id
                == image_unique_id
            )
            .first()
        )

        if not image:
            raise NotFoundException(
                msg.PRODUCT_IMAGE_NOT_FOUND
            )

        return image


    def get_images_by_product(
        self,
        db: Session,
        product_unique_id: str,
    ):
        """
        Get all images belonging to one Product.
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
            db.query(ProductImage)
            .filter(
                ProductImage.product_id
                == product.id
            )
            .order_by(
                ProductImage.sort_order.asc()
            )
            .all()
        )


    def update_image(
        self,
        db: Session,
        image_unique_id: str,
        data: ProductImageUpdate,
    ):
        """
        Update Product Image.
        """

        image = self.get_image(
            db,
            image_unique_id,
        )

        update_data = data.model_dump(
            exclude_unset=True
        )

        # If this image becomes primary,
        # clear existing primary image.
        if update_data.get("is_primary") is True:
            current_primary = (
                db.query(ProductImage)
                .filter(
                    ProductImage.product_id
                    == image.product_id,
                    ProductImage.is_primary.is_(True),
                    ProductImage.id != image.id,
                )
                .first()
            )

            if current_primary:
                current_primary.is_primary = False

        for field, value in update_data.items():
            setattr(
                image,
                field,
                value,
            )

        db.commit()
        db.refresh(image)

        return image


    def delete_image(
        self,
        db: Session,
        image_unique_id: str,
    ):
        """
        Permanently delete Product Image.
        """

        image = self.get_image(
            db,
            image_unique_id,
        )

        db.delete(image)
        db.commit()

        return {
            "message": msg.PRODUCT_IMAGE_DELETED
        }