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
        --password 123456 \
        --branch-id 11bfd7ca-9a53-4fa9-b92c-8d128e20075e
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
    # 1. FARMROOT
    # ========================================================

    {
        "brand": {
            "name": "FarmRoot",
            "slug": "farmroot-fresh-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Fresh Pantry",
                "slug": "fresh-pantry-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Natural Spreads",
                        "slug": "natural-spreads-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "FarmRoot Wildflower Honey",
                                "slug": "farmroot-wildflower-honey-2026",
                                "description": "Smooth floral honey sourced for everyday breakfast and beverages.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-FARMROOT-HONEY-300G",
                                        "value": "300",
                                        "unit": "g",
                                        "mrp": 159,
                                        "selling_price": 139,
                                    },
                                    {
                                        "sku": "NEW-FARMROOT-HONEY-650G",
                                        "value": "650",
                                        "unit": "g",
                                        "mrp": 299,
                                        "selling_price": 269,
                                    },
                                ],
                            },

                            {
                                "name": "FarmRoot Peanut Cocoa Spread",
                                "slug": "farmroot-peanut-cocoa-spread-2026",
                                "description": "Creamy peanut and cocoa spread for toast, snacks and quick desserts.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-FARMROOT-COCOA-200G",
                                        "value": "200",
                                        "unit": "g",
                                        "mrp": 149,
                                        "selling_price": 129,
                                    },
                                    {
                                        "sku": "NEW-FARMROOT-COCOA-400G",
                                        "value": "400",
                                        "unit": "g",
                                        "mrp": 269,
                                        "selling_price": 239,
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
    # 2. MORNING MATE
    # ========================================================

    {
        "brand": {
            "name": "Morning Mate",
            "slug": "morning-mate-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Breakfast Essentials",
                "slug": "breakfast-essentials-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Cereals & Granola",
                        "slug": "cereals-granola-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "Morning Mate Crunchy Corn Cereal",
                                "slug": "morning-mate-corn-cereal-2026",
                                "description": "Light and crispy corn cereal for a quick morning bowl.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-MORNING-CORN-300G",
                                        "value": "300",
                                        "unit": "g",
                                        "mrp": 145,
                                        "selling_price": 129,
                                    },
                                    {
                                        "sku": "NEW-MORNING-CORN-500G",
                                        "value": "500",
                                        "unit": "g",
                                        "mrp": 229,
                                        "selling_price": 205,
                                    },
                                ],
                            },

                            {
                                "name": "Morning Mate Choco Millet Bites",
                                "slug": "morning-mate-choco-millet-2026",
                                "description": "Chocolate-flavoured crunchy millet bites made for breakfast or snacking.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-MORNING-CHOCO-250G",
                                        "value": "250",
                                        "unit": "g",
                                        "mrp": 165,
                                        "selling_price": 149,
                                    },
                                    {
                                        "sku": "NEW-MORNING-CHOCO-450G",
                                        "value": "450",
                                        "unit": "g",
                                        "mrp": 259,
                                        "selling_price": 229,
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
    # 3. COCOCRAFT
    # ========================================================

    {
        "brand": {
            "name": "CocoCraft",
            "slug": "cococraft-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Sweet Treats",
                "slug": "sweet-treats-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Chocolate & Confectionery",
                        "slug": "chocolate-confectionery-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "CocoCraft Creamy Milk Chocolate",
                                "slug": "cococraft-creamy-milk-2026",
                                "description": "Classic creamy milk chocolate with a smooth melt and balanced sweetness.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-COCOCRAFT-MILK-55G",
                                        "value": "55",
                                        "unit": "g",
                                        "mrp": 60,
                                        "selling_price": 54,
                                    },
                                    {
                                        "sku": "NEW-COCOCRAFT-MILK-120G",
                                        "value": "120",
                                        "unit": "g",
                                        "mrp": 125,
                                        "selling_price": 112,
                                    },
                                ],
                            },

                            {
                                "name": "CocoCraft Hazelnut Silk Bar",
                                "slug": "cococraft-hazelnut-silk-2026",
                                "description": "Rich milk chocolate bar with a silky hazelnut-style flavour.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-COCOCRAFT-HAZEL-70G",
                                        "value": "70",
                                        "unit": "g",
                                        "mrp": 99,
                                        "selling_price": 89,
                                    },
                                    {
                                        "sku": "NEW-COCOCRAFT-HAZEL-150G",
                                        "value": "150",
                                        "unit": "g",
                                        "mrp": 199,
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
    # 4. FRUITWAVE
    # ========================================================

    {
        "brand": {
            "name": "FruitWave",
            "slug": "fruitwave-drinks-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Beverages",
                "slug": "beverages-refreshers-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Fruit Drinks",
                        "slug": "fruit-drinks-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "FruitWave Tropical Blend",
                                "slug": "fruitwave-tropical-blend-2026",
                                "description": "Refreshing tropical fruit drink with mango, pineapple and citrus notes.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-FRUITWAVE-TROPICAL-1L",
                                        "value": "1",
                                        "unit": "L",
                                        "mrp": 139,
                                        "selling_price": 125,
                                    },
                                    {
                                        "sku": "NEW-FRUITWAVE-TROPICAL-250ML",
                                        "value": "250",
                                        "unit": "ml",
                                        "mrp": 40,
                                        "selling_price": 36,
                                    },
                                ],
                            },

                            {
                                "name": "FruitWave Pink Guava Drink",
                                "slug": "fruitwave-pink-guava-2026",
                                "description": "Sweet and tangy pink guava beverage served best chilled.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-FRUITWAVE-GUAVA-1L",
                                        "value": "1",
                                        "unit": "L",
                                        "mrp": 129,
                                        "selling_price": 116,
                                    },
                                    {
                                        "sku": "NEW-FRUITWAVE-GUAVA-250ML",
                                        "value": "250",
                                        "unit": "ml",
                                        "mrp": 38,
                                        "selling_price": 34,
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
    # 5. PUREGUARD
    # ========================================================

    {
        "brand": {
            "name": "PureGuard",
            "slug": "pureguard-hygiene-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Personal Hygiene",
                "slug": "personal-hygiene-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Hand Care",
                        "slug": "hand-care-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "PureGuard Aloe Hand Wash",
                                "slug": "pureguard-aloe-handwash-2026",
                                "description": "Gentle liquid hand wash with a fresh aloe-inspired fragrance.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-PUREGUARD-WASH-250ML",
                                        "value": "250",
                                        "unit": "ml",
                                        "mrp": 109,
                                        "selling_price": 99,
                                    },
                                    {
                                        "sku": "NEW-PUREGUARD-WASH-750ML",
                                        "value": "750",
                                        "unit": "ml",
                                        "mrp": 279,
                                        "selling_price": 249,
                                    },
                                ],
                            },

                            {
                                "name": "PureGuard Fresh Hand Sanitizer",
                                "slug": "pureguard-fresh-sanitizer-2026",
                                "description": "Quick-dry hand sanitizer gel for travel, work and daily use.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-PUREGUARD-SAN-100ML",
                                        "value": "100",
                                        "unit": "ml",
                                        "mrp": 59,
                                        "selling_price": 52,
                                    },
                                    {
                                        "sku": "NEW-PUREGUARD-SAN-250ML",
                                        "value": "250",
                                        "unit": "ml",
                                        "mrp": 129,
                                        "selling_price": 115,
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
    # 6. BEANBAY
    # ========================================================

    {
        "brand": {
            "name": "BeanBay",
            "slug": "beanbay-coffee-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Tea Coffee & Drinks",
                "slug": "tea-coffee-drinks-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Instant Coffee",
                        "slug": "instant-coffee-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "BeanBay Classic Instant Coffee",
                                "slug": "beanbay-classic-instant-2026",
                                "description": "Bold instant coffee with a roasted aroma and smooth finish.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-BEANBAY-CLASSIC-50G",
                                        "value": "50",
                                        "unit": "g",
                                        "mrp": 189,
                                        "selling_price": 172,
                                    },
                                    {
                                        "sku": "NEW-BEANBAY-CLASSIC-100G",
                                        "value": "100",
                                        "unit": "g",
                                        "mrp": 359,
                                        "selling_price": 329,
                                    },
                                ],
                            },

                            {
                                "name": "BeanBay Morning Roast Coffee",
                                "slug": "beanbay-morning-roast-2026",
                                "description": "Balanced instant coffee blend designed for a bright morning cup.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-BEANBAY-MORNING-75G",
                                        "value": "75",
                                        "unit": "g",
                                        "mrp": 229,
                                        "selling_price": 209,
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
    # 7. TINYBLOOM
    # ========================================================

    {
        "brand": {
            "name": "TinyBloom",
            "slug": "tinybloom-baby-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Baby Essentials",
                "slug": "baby-essentials-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Diapers & Baby Pants",
                        "slug": "diapers-baby-pants-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "TinyBloom SoftFit Diaper Pants",
                                "slug": "tinybloom-softfit-pants-2026",
                                "description": "Soft and flexible diaper pants designed for everyday comfort.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-TINYBLOOM-M-32PCS",
                                        "value": "32",
                                        "unit": "pcs",
                                        "mrp": 479,
                                        "selling_price": 429,
                                    },
                                    {
                                        "sku": "NEW-TINYBLOOM-L-30PCS",
                                        "value": "30",
                                        "unit": "pcs",
                                        "mrp": 529,
                                        "selling_price": 475,
                                    },
                                ],
                            },

                            {
                                "name": "TinyBloom NightComfort Diaper Pants",
                                "slug": "tinybloom-nightcomfort-2026",
                                "description": "High-absorbency diaper pants for longer overnight comfort.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-TINYBLOOM-NIGHT-L-24PCS",
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
    # 8. HOMEBREEZE
    # ========================================================

    {
        "brand": {
            "name": "HomeBreeze",
            "slug": "homebreeze-2026",
            "logo_url": IMAGE_URL,
        },

        "categories": [
            {
                "name": "Home Care",
                "slug": "home-care-2026",
                "image_url": IMAGE_URL,

                "subcategories": [
                    {
                        "name": "Room Fresheners",
                        "slug": "room-fresheners-2026",
                        "image_url": IMAGE_URL,

                        "products": [
                            {
                                "name": "HomeBreeze Citrus Room Spray",
                                "slug": "homebreeze-citrus-spray-2026",
                                "description": "Bright citrus room freshener spray for bedrooms and living spaces.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-HOMEBREEZE-CITRUS-240ML",
                                        "value": "240",
                                        "unit": "ml",
                                        "mrp": 179,
                                        "selling_price": 159,
                                    },
                                ],
                            },

                            {
                                "name": "HomeBreeze Lavender Gel Freshener",
                                "slug": "homebreeze-lavender-gel-2026",
                                "description": "Compact lavender-scented gel freshener for bathrooms and cupboards.",
                                "image_url": IMAGE_URL,

                                "variants": [
                                    {
                                        "sku": "NEW-HOMEBREEZE-LAVENDER-60G",
                                        "value": "60",
                                        "unit": "g",
                                        "mrp": 89,
                                        "selling_price": 79,
                                    },
                                    {
                                        "sku": "NEW-HOMEBREEZE-LAVENDER-120G",
                                        "value": "120",
                                        "unit": "g",
                                        "mrp": 149,
                                        "selling_price": 135,
                                    },
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