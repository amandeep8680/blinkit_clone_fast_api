from sqlalchemy.orm import (
    Session,
    joinedload,
)

from  app.models.branches_model import Branch
from  app.models.branch_inventory_model import (
    BranchInventory,
)

from  app.models.product_variant_model import (
    ProductVariant,
)

from  app.models.product_model import Product

from  app.exceptions.custom_exceptions import (
    BadRequestException,
    NotFoundException,
)

from  app.exceptions import messages as msg


class BranchCatalogService:

    def get_branch_catalog(
        self,
        db: Session,
        branch_unique_id: str,
    ):
        """
        Return all active and available products
        for the selected branch.
        """

        # -----------------------------------
        # Find Branch
        # -----------------------------------

        branch = (
            db.query(Branch)
            .filter(
                Branch.unique_id == branch_unique_id
            )
            .first()
        )

        if not branch:
            raise NotFoundException(
                msg.BRANCH_NOT_FOUND
            )

        if not branch.is_active:
            raise BadRequestException(
                msg.BRANCH_INACTIVE
            )

        # -----------------------------------
        # Find Branch Inventory
        # -----------------------------------

        inventory_items = (
            db.query(BranchInventory)
            .join(
                ProductVariant,
                BranchInventory.product_variant_id
                == ProductVariant.id,
            )
            .join(
                Product,
                ProductVariant.product_id
                == Product.id,
            )
            .options(
                joinedload(
                    BranchInventory.product_variant
                )
                .joinedload(
                    ProductVariant.product
                )
                .joinedload(
                    Product.brand
                ),

                joinedload(
                    BranchInventory.product_variant
                )
                .joinedload(
                    ProductVariant.product
                )
                .joinedload(
                    Product.subcategory
                ),

                joinedload(
                    BranchInventory.product_variant
                )
                .joinedload(
                    ProductVariant.product
                )
                .joinedload(
                    Product.images
                ),
            )
            .filter(
                BranchInventory.branch_id
                == branch.id,

                BranchInventory.is_available
                .is_(True),

                BranchInventory.stock_quantity > 0,

                ProductVariant.is_active
                .is_(True),

                Product.is_active
                .is_(True),
            )
            .all()
        )

        # -----------------------------------
        # Group Variants By Product
        # -----------------------------------

        products = {}

        for inventory in inventory_items:

            variant = inventory.product_variant
            product = variant.product

            # Use branch specific price if available.
            selling_price = (
                inventory.selling_price_override
                if inventory.selling_price_override is not None
                else variant.selling_price
            )

            # -----------------------------------
            # Add Product
            # -----------------------------------

            if product.id not in products:

                products[product.id] = {
                    "unique_id": product.unique_id,
                    "name": product.name,
                    "slug": product.slug,
                    "description": product.description,

                    "brand": {
                        "unique_id": product.brand.unique_id,
                        "name": product.brand.name,
                        "slug": product.brand.slug,
                        "logo_url": product.brand.logo_url,
                    },

                    "subcategory": {
                        "unique_id": product.subcategory.unique_id,
                        "name": product.subcategory.name,
                        "slug": product.subcategory.slug,
                    },

                    "images": [
                        {
                            "image_url": image.image_url,
                            "sort_order": image.sort_order,
                            "is_primary": image.is_primary,
                        }
                        for image in product.images
                    ],

                    "variants": [],
                }

            # -----------------------------------
            # Add Available Variant
            # -----------------------------------

            products[product.id]["variants"].append(
                {
                    "unique_id": variant.unique_id,
                    "sku": variant.sku,
                    "value": variant.value,
                    "unit": variant.unit,
                    "mrp": variant.mrp,
                    "selling_price": selling_price,
                    "is_available": True,
                }
            )

        return list(
            products.values()
        )