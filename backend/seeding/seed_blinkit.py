#!/usr/bin/env python3

"""
Second Branch Blinkit Seeder

Creates:
- Brands
- Categories
- Subcategories
- Products
- Product Variants
- Product Images
- Inventory for SECOND branch

Install:
    pip install requests

Run:
    python seed_blinkit.py \
        --base-url http://127.0.0.1:8000 \
        --email deep@singh.com \
        --password 12345 \
        --branch-id 3b867f90-dd2e-44ec-a5fc-6825ff5521a2
"""

import argparse
import os
import sys
from typing import Any, Dict, Optional

import requests


# ============================================================
# COMMON IMAGE URL
# ============================================================

IMAGE_URL = (
    "https://stimg.cardekho.com/images/"
    "carexteriorimages/630x420/"
    "BMW/M4-CS/"
    "12143/1762778950933/front-left-side-47.jpg?imwidth=420&impolicy=resize"
)


# ============================================================
# DEFAULT INVENTORY STOCK
# ============================================================

DEFAULT_STOCK = 60


# ============================================================
# COMPLETELY NEW SEED DATA
# ============================================================

SEED_DATA = [

    # ========================================================
    # 1. DABUR
    # ========================================================

    {
        "brand": {
            "name": "Dabur",
            "slug": "dabur-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Health & Wellness",
                "slug": "health-wellness-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Honey & Health Foods",
                        "slug": "honey-health-foods-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Dabur Honey",
                                "slug": "dabur-honey-second",
                                "description": "Pure honey for everyday use.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-DABUR-HONEY-250G",
                                        "value": "250",
                                        "unit": "g",
                                        "mrp": 125,
                                        "selling_price": 115,
                                    },
                                    {
                                        "sku": "SECOND-DABUR-HONEY-500G",
                                        "value": "500",
                                        "unit": "g",
                                        "mrp": 240,
                                        "selling_price": 220,
                                    },
                                ],
                            },

                            {
                                "name": "Dabur Chyawanprash",
                                "slug": "dabur-chyawanprash-second",
                                "description": "Traditional Ayurvedic health supplement.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-DABUR-CHYAWAN-500G",
                                        "value": "500",
                                        "unit": "g",
                                        "mrp": 225,
                                        "selling_price": 205,
                                    },
                                    {
                                        "sku": "SECOND-DABUR-CHYAWAN-1KG",
                                        "value": "1",
                                        "unit": "kg",
                                        "mrp": 410,
                                        "selling_price": 379,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 2. KELLOGGS
    # ========================================================

    {
        "brand": {
            "name": "Kellogg's",
            "slug": "kelloggs-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Breakfast Foods",
                "slug": "breakfast-foods-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Cereals",
                        "slug": "cereals-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Kellogg's Corn Flakes",
                                "slug": "kelloggs-corn-flakes-second",
                                "description": "Crispy breakfast corn flakes.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-KELLOGGS-CORN-250G",
                                        "value": "250",
                                        "unit": "g",
                                        "mrp": 135,
                                        "selling_price": 125,
                                    },
                                    {
                                        "sku": "SECOND-KELLOGGS-CORN-475G",
                                        "value": "475",
                                        "unit": "g",
                                        "mrp": 230,
                                        "selling_price": 210,
                                    },
                                ],
                            },

                            {
                                "name": "Kellogg's Chocos",
                                "slug": "kelloggs-chocos-second",
                                "description": "Chocolate flavoured breakfast cereal.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-KELLOGGS-CHOCOS-250G",
                                        "value": "250",
                                        "unit": "g",
                                        "mrp": 150,
                                        "selling_price": 139,
                                    },
                                    {
                                        "sku": "SECOND-KELLOGGS-CHOCOS-385G",
                                        "value": "385",
                                        "unit": "g",
                                        "mrp": 220,
                                        "selling_price": 205,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 3. CADBURY
    # ========================================================

    {
        "brand": {
            "name": "Cadbury",
            "slug": "cadbury-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Chocolates & Sweets",
                "slug": "chocolates-sweets-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Chocolate Bars",
                        "slug": "chocolate-bars-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Cadbury Dairy Milk",
                                "slug": "cadbury-dairy-milk-second",
                                "description": "Classic milk chocolate bar.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-CADBURY-DM-50G",
                                        "value": "50",
                                        "unit": "g",
                                        "mrp": 50,
                                        "selling_price": 48,
                                    },
                                    {
                                        "sku": "SECOND-CADBURY-DM-110G",
                                        "value": "110",
                                        "unit": "g",
                                        "mrp": 100,
                                        "selling_price": 95,
                                    },
                                ],
                            },

                            {
                                "name": "Cadbury Dairy Milk Silk",
                                "slug": "cadbury-silk-second",
                                "description": "Smooth premium milk chocolate.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-CADBURY-SILK-60G",
                                        "value": "60",
                                        "unit": "g",
                                        "mrp": 90,
                                        "selling_price": 85,
                                    },
                                    {
                                        "sku": "SECOND-CADBURY-SILK-150G",
                                        "value": "150",
                                        "unit": "g",
                                        "mrp": 190,
                                        "selling_price": 179,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 4. REAL
    # ========================================================

    {
        "brand": {
            "name": "Real",
            "slug": "real-juice-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Juices & Drinks",
                "slug": "juices-drinks-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Fruit Juices",
                        "slug": "fruit-juices-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Real Mixed Fruit Juice",
                                "slug": "real-mixed-fruit-second",
                                "description": "Mixed fruit juice beverage.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-REAL-MIXED-1L",
                                        "value": "1",
                                        "unit": "L",
                                        "mrp": 130,
                                        "selling_price": 119,
                                    },
                                ],
                            },

                            {
                                "name": "Real Mango Juice",
                                "slug": "real-mango-second",
                                "description": "Mango fruit beverage.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-REAL-MANGO-1L",
                                        "value": "1",
                                        "unit": "L",
                                        "mrp": 125,
                                        "selling_price": 115,
                                    },
                                    {
                                        "sku": "SECOND-REAL-MANGO-200ML",
                                        "value": "200",
                                        "unit": "ml",
                                        "mrp": 30,
                                        "selling_price": 28,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 5. DETTOL
    # ========================================================

    {
        "brand": {
            "name": "Dettol",
            "slug": "dettol-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Home & Hygiene",
                "slug": "home-hygiene-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Hand Wash & Sanitizers",
                        "slug": "handwash-sanitizers-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Dettol Original Liquid Handwash",
                                "slug": "dettol-handwash-second",
                                "description": "Antibacterial liquid hand wash.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-DETTOL-HANDWASH-200ML",
                                        "value": "200",
                                        "unit": "ml",
                                        "mrp": 95,
                                        "selling_price": 89,
                                    },
                                    {
                                        "sku": "SECOND-DETTOL-HANDWASH-750ML",
                                        "value": "750",
                                        "unit": "ml",
                                        "mrp": 250,
                                        "selling_price": 229,
                                    },
                                ],
                            },

                            {
                                "name": "Dettol Instant Hand Sanitizer",
                                "slug": "dettol-sanitizer-second",
                                "description": "Instant hand sanitizer gel.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-DETTOL-SANITIZER-50ML",
                                        "value": "50",
                                        "unit": "ml",
                                        "mrp": 35,
                                        "selling_price": 32,
                                    },
                                    {
                                        "sku": "SECOND-DETTOL-SANITIZER-200ML",
                                        "value": "200",
                                        "unit": "ml",
                                        "mrp": 110,
                                        "selling_price": 99,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 6. NESCAFE
    # ========================================================

    {
        "brand": {
            "name": "Nescafe",
            "slug": "nescafe-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Tea Coffee & More",
                "slug": "tea-coffee-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Coffee",
                        "slug": "coffee-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Nescafe Classic Coffee",
                                "slug": "nescafe-classic-second",
                                "description": "Instant pure coffee.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-NESCAFE-CLASSIC-50G",
                                        "value": "50",
                                        "unit": "g",
                                        "mrp": 180,
                                        "selling_price": 169,
                                    },
                                    {
                                        "sku": "SECOND-NESCAFE-CLASSIC-100G",
                                        "value": "100",
                                        "unit": "g",
                                        "mrp": 350,
                                        "selling_price": 325,
                                    },
                                ],
                            },

                            {
                                "name": "Nescafe Sunrise Coffee",
                                "slug": "nescafe-sunrise-second",
                                "description": "Coffee and chicory instant blend.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-NESCAFE-SUNRISE-50G",
                                        "value": "50",
                                        "unit": "g",
                                        "mrp": 135,
                                        "selling_price": 125,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 7. PAMPERS
    # ========================================================

    {
        "brand": {
            "name": "Pampers",
            "slug": "pampers-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Baby Care",
                "slug": "baby-care-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Baby Diapers",
                        "slug": "baby-diapers-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Pampers Baby Dry Pants",
                                "slug": "pampers-baby-dry-second",
                                "description": "Comfortable baby diaper pants.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-PAMPERS-M-30PCS",
                                        "value": "30",
                                        "unit": "pcs",
                                        "mrp": 499,
                                        "selling_price": 449,
                                    },
                                    {
                                        "sku": "SECOND-PAMPERS-L-30PCS",
                                        "value": "30",
                                        "unit": "pcs",
                                        "mrp": 549,
                                        "selling_price": 489,
                                    },
                                ],
                            },

                            {
                                "name": "Pampers Premium Care Pants",
                                "slug": "pampers-premium-care-second",
                                "description": "Premium baby diaper pants.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-PAMPERS-PREMIUM-M-24PCS",
                                        "value": "24",
                                        "unit": "pcs",
                                        "mrp": 599,
                                        "selling_price": 549,
                                    },
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },


    # ========================================================
    # 8. GODREJ
    # ========================================================

    {
        "brand": {
            "name": "Godrej",
            "slug": "godrej-second-branch",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Household Supplies",
                "slug": "household-supplies-second",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Air Fresheners",
                        "slug": "air-fresheners-second",
                        "image_url": IMAGE_URL,

                        "products": [

                            {
                                "name": "Godrej Aer Spray",
                                "slug": "godrej-aer-spray-second",
                                "description": "Room air freshener spray.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-GODREJ-AER-240ML",
                                        "value": "240",
                                        "unit": "ml",
                                        "mrp": 169,
                                        "selling_price": 155,
                                    },
                                ],
                            },

                            {
                                "name": "Godrej Aer Pocket",
                                "slug": "godrej-aer-pocket-second",
                                "description": "Compact bathroom fragrance.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "SECOND-GODREJ-AER-POCKET-10G",
                                        "value": "10",
                                        "unit": "g",
                                        "mrp": 65,
                                        "selling_price": 59,
                                    }
                                ],
                            },

                        ],
                    }
                ],
            }
        ],
    },

]


# ============================================================
# SEEDER CLASS
# ============================================================

class BlinkitSeeder:

    def __init__(
        self,
        base_url: str,
        email: str,
        password: str,
        branch_id: str,
    ):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.branch_id = branch_id

        self.session = requests.Session()

        self.session.headers.update({
            "Content-Type": "application/json"
        })

        self.brands_by_slug: Dict[str, Dict[str, Any]] = {}
        self.categories_by_slug: Dict[str, Dict[str, Any]] = {}
        self.subcategories_by_slug: Dict[str, Dict[str, Any]] = {}
        self.products_by_slug: Dict[str, Dict[str, Any]] = {}
        self.variants_by_sku: Dict[str, Dict[str, Any]] = {}

        self.created = 0
        self.skipped = 0
        self.failed = 0


    # ========================================================
    # URL
    # ========================================================

    def url(self, path: str) -> str:
        return f"{self.base_url}{path}"


    # ========================================================
    # LOGIN
    # ========================================================

    def login(self) -> None:

        print("\n🔐 Logging in...")

        try:
            response = self.session.post(
                self.url("/auth/login"),
                json={
                    "email": self.email,
                    "password": self.password,
                },
                timeout=20,
            )

        except requests.RequestException as exc:
            print(f"❌ Login network error: {exc}")
            sys.exit(1)


        if not response.ok:

            print(
                f"❌ Login failed: HTTP {response.status_code}"
            )

            print(response.text)

            sys.exit(1)


        body = response.json()

        token = body.get("access_token")


        if not token:

            print(
                "❌ access_token missing from login response"
            )

            print(body)

            sys.exit(1)


        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })


        print("✅ Login successful")


    # ========================================================
    # GENERIC REQUEST
    # ========================================================

    def request(
        self,
        method: str,
        path: str,
        *,
        json_body=None,
        params=None,
        allow_404: bool = False,
    ):

        try:
            response = self.session.request(
                method,
                self.url(path),
                json=json_body,
                params=params,
                timeout=25,
            )

        except requests.RequestException as exc:

            self.failed += 1

            print(
                f"❌ NETWORK {method} {path}: {exc}"
            )

            return None


        # ----------------------------------------------------
        # Expected 404
        # ----------------------------------------------------

        if (
            response.status_code == 404
            and allow_404
        ):
            return None


        # ----------------------------------------------------
        # Authentication / authorization
        # ----------------------------------------------------

        if response.status_code in (401, 403):

            self.failed += 1

            print(
                f"🚫 {method} {path}: "
                f"HTTP {response.status_code}"
            )

            try:
                print(
                    "   ",
                    response.json(),
                )

            except Exception:
                print(
                    "   ",
                    response.text[:500],
                )

            return None


        # ----------------------------------------------------
        # Other errors
        # ----------------------------------------------------

        if not response.ok:

            self.failed += 1

            print(
                f"❌ {method} {path}: "
                f"HTTP {response.status_code}"
            )

            try:
                print(
                    "   ",
                    response.json(),
                )

            except Exception:
                print(
                    "   ",
                    response.text[:500],
                )

            return None


        if (
            response.status_code == 204
            or not response.content
        ):
            return {}


        try:
            return response.json()

        except ValueError:
            return {}


    # ========================================================
    # LOAD EXISTING CATALOG
    # ========================================================

    def preload_existing(self) -> None:

        print("\n📦 Loading existing catalog...")


        brands = (
            self.request(
                "GET",
                "/brands",
                params={
                    "skip": 0,
                    "limit": 1000,
                },
            )
            or []
        )


        categories = (
            self.request(
                "GET",
                "/categories",
                params={
                    "skip": 0,
                    "limit": 1000,
                },
            )
            or []
        )


        subcategories = (
            self.request(
                "GET",
                "/subcategories",
                params={
                    "skip": 0,
                    "limit": 1000,
                },
            )
            or []
        )


        products = (
            self.request(
                "GET",
                "/products",
                params={
                    "skip": 0,
                    "limit": 1000,
                },
            )
            or []
        )


        variants = (
            self.request(
                "GET",
                "/product-variants",
                params={
                    "skip": 0,
                    "limit": 2000,
                },
            )
            or []
        )


        self.brands_by_slug = {
            item.get("slug"): item
            for item in brands
            if item.get("slug")
        }


        self.categories_by_slug = {
            item.get("slug"): item
            for item in categories
            if item.get("slug")
        }


        self.subcategories_by_slug = {
            item.get("slug"): item
            for item in subcategories
            if item.get("slug")
        }


        self.products_by_slug = {
            item.get("slug"): item
            for item in products
            if item.get("slug")
        }


        self.variants_by_sku = {
            item.get("sku"): item
            for item in variants
            if item.get("sku")
        }


        print(
            f"   Existing brands: "
            f"{len(self.brands_by_slug)}"
        )

        print(
            f"   Existing categories: "
            f"{len(self.categories_by_slug)}"
        )

        print(
            f"   Existing subcategories: "
            f"{len(self.subcategories_by_slug)}"
        )

        print(
            f"   Existing products: "
            f"{len(self.products_by_slug)}"
        )

        print(
            f"   Existing variants: "
            f"{len(self.variants_by_sku)}"
        )


    # ========================================================
    # BRAND
    # ========================================================

    def get_or_create_brand(
        self,
        data: Dict[str, Any],
    ):

        slug = data["slug"]


        if slug in self.brands_by_slug:

            self.skipped += 1

            print(
                f"⏭️ Brand already exists: "
                f"{data['name']}"
            )

            return self.brands_by_slug[slug]


        payload = {
            "name": data["name"],
            "slug": data["slug"],
            "logo_url": data.get(
                "logo_url"
            ),
            "is_active": True,
        }


        result = self.request(
            "POST",
            "/brands",
            json_body=payload,
        )


        if result:

            self.created += 1

            self.brands_by_slug[
                slug
            ] = result

            print(
                f"✅ Brand created: "
                f"{data['name']}"
            )


        return result


    # ========================================================
    # CATEGORY
    # ========================================================

    def get_or_create_category(
        self,
        data: Dict[str, Any],
    ):

        slug = data["slug"]


        if slug in self.categories_by_slug:

            self.skipped += 1

            print(
                f"⏭️ Category already exists: "
                f"{data['name']}"
            )

            return self.categories_by_slug[
                slug
            ]


        payload = {
            "name": data["name"],
            "slug": data["slug"],
            "image_url": data.get(
                "image_url"
            ),
            "is_active": True,
        }


        result = self.request(
            "POST",
            "/categories",
            json_body=payload,
        )


        if result:

            self.created += 1

            self.categories_by_slug[
                slug
            ] = result

            print(
                f"✅ Category created: "
                f"{data['name']}"
            )


        return result


    # ========================================================
    # SUBCATEGORY
    # ========================================================

    def get_or_create_subcategory(
        self,
        data: Dict[str, Any],
        category_unique_id: str,
    ):

        slug = data["slug"]


        if slug in self.subcategories_by_slug:

            self.skipped += 1

            print(
                f"⏭️ Subcategory already exists: "
                f"{data['name']}"
            )

            return self.subcategories_by_slug[
                slug
            ]


        payload = {
            "name": data["name"],
            "slug": data["slug"],
            "image_url": data.get(
                "image_url"
            ),
            "is_active": True,
            "category_unique_id":
                category_unique_id,
        }


        result = self.request(
            "POST",
            "/subcategories",
            json_body=payload,
        )


        if result:

            self.created += 1

            self.subcategories_by_slug[
                slug
            ] = result

            print(
                f"✅ Subcategory created: "
                f"{data['name']}"
            )


        return result


    # ========================================================
    # PRODUCT
    # ========================================================

    def get_or_create_product(
        self,
        data: Dict[str, Any],
        brand_unique_id: str,
        subcategory_unique_id: str,
    ):

        slug = data["slug"]


        if slug in self.products_by_slug:

            self.skipped += 1

            print(
                f"⏭️ Product already exists: "
                f"{data['name']}"
            )

            return self.products_by_slug[
                slug
            ]


        payload = {
            "name":
                data["name"],

            "slug":
                data["slug"],

            "description":
                data.get(
                    "description"
                ),

            "is_active":
                True,

            "brand_unique_id":
                brand_unique_id,

            "subcategory_unique_id":
                subcategory_unique_id,
        }


        result = self.request(
            "POST",
            "/products",
            json_body=payload,
        )


        if result:

            self.created += 1

            self.products_by_slug[
                slug
            ] = result

            print(
                f"✅ Product created: "
                f"{data['name']}"
            )


        return result


    # ========================================================
    # PRODUCT VARIANT
    # ========================================================

    def get_or_create_variant(
        self,
        data: Dict[str, Any],
        product_unique_id: str,
    ):

        sku = data["sku"]


        if sku in self.variants_by_sku:

            self.skipped += 1

            print(
                f"   ⏭️ Variant already exists: "
                f"{sku}"
            )

            return self.variants_by_sku[
                sku
            ]


        payload = {
            "sku":
                data["sku"],

            "value":
                str(
                    data["value"]
                ),

            "unit":
                data["unit"],

            "mrp":
                data["mrp"],

            "selling_price":
                data["selling_price"],

            "is_active":
                True,

            "product_unique_id":
                product_unique_id,
        }


        result = self.request(
            "POST",
            "/product-variants",
            json_body=payload,
        )


        if result:

            self.created += 1

            self.variants_by_sku[
                sku
            ] = result

            print(
                f"   ✅ Variant created: "
                f"{sku}"
            )


        return result


    # ========================================================
    # PRODUCT IMAGE
    # ========================================================

    def create_product_image_if_needed(
        self,
        product_unique_id: str,
    ):

        existing_images = (
            self.request(
                "GET",
                (
                    "/product-images/product/"
                    f"{product_unique_id}"
                ),
            )
            or []
        )


        for image in existing_images:

            if (
                image.get("image_url")
                == IMAGE_URL
            ):

                self.skipped += 1

                print(
                    "   ⏭️ Product image "
                    "already exists"
                )

                return


        payload = {
            "image_url":
                IMAGE_URL,

            "sort_order":
                0,

            "is_primary":
                True,

            "product_unique_id":
                product_unique_id,
        }


        result = self.request(
            "POST",
            "/product-images",
            json_body=payload,
        )


        if result:

            self.created += 1

            print(
                "   ✅ Product image created"
            )


    # ========================================================
    # INVENTORY
    # ========================================================

    def create_inventory_if_needed(
        self,
        variant: Dict[str, Any],
    ):

        variant_unique_id = (
            variant.get(
                "unique_id"
            )
        )


        if not variant_unique_id:

            print(
                "❌ Variant unique_id missing"
            )

            return


        inventory_path = (
            f"/inventory/branch/"
            f"{self.branch_id}"
            f"/variant/"
            f"{variant_unique_id}"
        )


        # ----------------------------------------------------
        # Missing inventory normally returns 404.
        # This is expected and should NOT count as failure.
        # ----------------------------------------------------

        existing = self.request(
            "GET",
            inventory_path,
            allow_404=True,
        )


        if existing:

            self.skipped += 1

            print(
                f"      ⏭️ Inventory already exists: "
                f"{variant.get('sku')}"
            )

            return


        payload = {
            "branch_unique_id":
                self.branch_id,

            "product_variant_unique_id":
                variant_unique_id,

            "stock_quantity":
                DEFAULT_STOCK,

            "selling_price_override":
                None,

            "is_available":
                True,
        }


        result = self.request(
            "POST",
            "/inventory",
            json_body=payload,
        )


        if result:

            self.created += 1

            print(
                f"      ✅ Inventory created: "
                f"{variant.get('sku')} "
                f"stock={DEFAULT_STOCK}"
            )


    # ========================================================
    # SEED
    # ========================================================

    def seed(self):

        print()
        print("=" * 65)
        print("🌱 BLINKIT SECOND BRANCH SEEDER")
        print("=" * 65)

        print(
            f"Branch unique_id: "
            f"{self.branch_id}"
        )

        print("=" * 65)


        # Login
        self.login()


        # Load already existing catalog
        self.preload_existing()


        print()
        print("🌱 Starting seed...")
        print()


        # ====================================================
        # LOOP THROUGH ALL BRANDS
        # ====================================================

        for group in SEED_DATA:

            # ------------------------------------------------
            # BRAND
            # ------------------------------------------------

            brand_data = (
                group["brand"]
            )


            brand = (
                self.get_or_create_brand(
                    brand_data
                )
            )


            if not brand:
                continue


            brand_unique_id = (
                brand.get(
                    "unique_id"
                )
            )


            if not brand_unique_id:

                print(
                    f"❌ Brand unique_id missing: "
                    f"{brand_data['name']}"
                )

                continue


            # ------------------------------------------------
            # CATEGORIES
            # ------------------------------------------------

            for category_data in (
                group.get(
                    "categories",
                    [],
                )
            ):

                category = (
                    self.get_or_create_category(
                        category_data
                    )
                )


                if not category:
                    continue


                category_unique_id = (
                    category.get(
                        "unique_id"
                    )
                )


                if not category_unique_id:

                    print(
                        "❌ Category unique_id missing: "
                        f"{category_data['name']}"
                    )

                    continue


                # --------------------------------------------
                # SUBCATEGORIES
                # --------------------------------------------

                for subcategory_data in (
                    category_data.get(
                        "subcategories",
                        [],
                    )
                ):

                    subcategory = (
                        self.get_or_create_subcategory(
                            subcategory_data,
                            category_unique_id,
                        )
                    )


                    if not subcategory:
                        continue


                    subcategory_unique_id = (
                        subcategory.get(
                            "unique_id"
                        )
                    )


                    if not subcategory_unique_id:

                        print(
                            "❌ Subcategory unique_id "
                            "missing: "
                            f"{subcategory_data['name']}"
                        )

                        continue


                    # ----------------------------------------
                    # PRODUCTS
                    # ----------------------------------------

                    for product_data in (
                        subcategory_data.get(
                            "products",
                            [],
                        )
                    ):

                        product = (
                            self.get_or_create_product(
                                product_data,
                                brand_unique_id,
                                subcategory_unique_id,
                            )
                        )


                        if not product:
                            continue


                        product_unique_id = (
                            product.get(
                                "unique_id"
                            )
                        )


                        if not product_unique_id:

                            print(
                                "❌ Product unique_id "
                                "missing: "
                                f"{product_data['name']}"
                            )

                            continue


                        # ------------------------------------
                        # PRODUCT IMAGE
                        # ------------------------------------

                        self.create_product_image_if_needed(
                            product_unique_id
                        )


                        # ------------------------------------
                        # PRODUCT VARIANTS
                        # ------------------------------------

                        for variant_data in (
                            product_data.get(
                                "variants",
                                [],
                            )
                        ):

                            variant = (
                                self.get_or_create_variant(
                                    variant_data,
                                    product_unique_id,
                                )
                            )


                            if not variant:
                                continue


                            # --------------------------------
                            # SECOND BRANCH INVENTORY
                            # --------------------------------

                            self.create_inventory_if_needed(
                                variant
                            )


        # ====================================================
        # SUMMARY
        # ====================================================

        print()
        print("=" * 65)
        print("🎉 SECOND BRANCH SEED FINISHED")
        print("=" * 65)

        print(
            f"✅ Created : "
            f"{self.created}"
        )

        print(
            f"⏭️ Skipped : "
            f"{self.skipped}"
        )

        print(
            f"❌ Failed  : "
            f"{self.failed}"
        )

        print("=" * 65)

        print()
        print(
            f"📍 Inventory branch: "
            f"{self.branch_id}"
        )

        print(
            f"📦 Default stock: "
            f"{DEFAULT_STOCK}"
        )

        print()


# ============================================================
# COMMAND LINE ARGUMENTS
# ============================================================

def parse_args():

    parser = argparse.ArgumentParser(
        description=(
            "Seed completely different catalog "
            "for second Blinkit branch"
        )
    )


    parser.add_argument(
        "--base-url",

        default=os.getenv(
            "BLINKIT_BASE_URL",
            "http://127.0.0.1:8000",
        ),

        help=(
            "FastAPI backend base URL"
        ),
    )


    parser.add_argument(
        "--email",

        default=os.getenv(
            "BLINKIT_ADMIN_EMAIL"
        ),

        help=(
            "Super Admin email"
        ),
    )


    parser.add_argument(
        "--password",

        default=os.getenv(
            "BLINKIT_ADMIN_PASSWORD"
        ),

        help=(
            "Super Admin password"
        ),
    )


    parser.add_argument(
        "--branch-id",

        default=os.getenv(
            "BLINKIT_SECOND_BRANCH_ID"
        ),

        help=(
            "Second branch unique_id"
        ),
    )


    return parser.parse_args()


# ============================================================
# MAIN
# ============================================================

def main():

    args = parse_args()


    # --------------------------------------------------------
    # Required args check
    # --------------------------------------------------------

    if not args.email:

        print(
            "❌ Admin email is required."
        )

        sys.exit(1)


    if not args.password:

        print(
            "❌ Admin password is required."
        )

        sys.exit(1)


    if not args.branch_id:

        print(
            "❌ Second branch unique_id "
            "is required."
        )

        print()

        print("Example:")

        print(
            "python seed_second_branch.py "
            "--base-url http://127.0.0.1:8000 "
            "--email admin@example.com "
            "--password admin123 "
            "--branch-id YOUR_SECOND_BRANCH_UUID"
        )

        sys.exit(1)


    # --------------------------------------------------------
    # Seeder
    # --------------------------------------------------------

    seeder = BlinkitSeeder(
        base_url=args.base_url,
        email=args.email,
        password=args.password,
        branch_id=args.branch_id,
    )


    seeder.seed()


# ============================================================
# START SCRIPT
# ============================================================

if __name__ == "__main__":
    main()