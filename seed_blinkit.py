#!/usr/bin/env python3
"""
Blinkit API Seeder

Seeds:
- Brands
- Categories
- Subcategories
- Products
- Product Variants
- Product Images
- Optional branch inventory

Usage:
    pip install requests

    python seed_blinkit.py \
        --base-url http://127.0.0.1:8000 \
        --email admin@example.com \
        --password your_password

Optional inventory for an existing branch:
    python seed_blinkit.py \
        --base-url http://127.0.0.1:8000 \
        --email admin@example.com \
        --password your_password \
        --branch-id YOUR_BRANCH_UNIQUE_ID

You can also use environment variables:
    BLINKIT_BASE_URL
    BLINKIT_ADMIN_EMAIL
    BLINKIT_ADMIN_PASSWORD
    BLINKIT_BRANCH_ID
"""

import argparse
import os
import sys
from typing import Any, Dict, List, Optional

import requests


# ---------------------------------------------------------------------
# Seed Data
# ---------------------------------------------------------------------

SEED_DATA = [
    {
        "brand": {
            "name": "Amul",
            "slug": "amul",
            "logo_url": "https://placehold.co/400x160?text=Amul",
        },
        "categories": [
            {
                "name": "Dairy & Breakfast",
                "slug": "dairy-breakfast",
                "image_url": "https://placehold.co/500x500?text=Dairy",
                "subcategories": [
                    {
                        "name": "Milk",
                        "slug": "milk",
                        "image_url": "https://placehold.co/500x500?text=Milk",
                        "products": [
                            {
                                "name": "Amul Taaza Toned Milk",
                                "slug": "amul-taaza-toned-milk",
                                "description": "Everyday toned milk.",
                                "image_url": "https://placehold.co/600x600?text=Amul+Taaza",
                                "variants": [
                                    {"sku": "AMUL-TAAZA-500ML", "value": "500", "unit": "ml", "mrp": 29, "selling_price": 28},
                                    {"sku": "AMUL-TAAZA-1L", "value": "1", "unit": "L", "mrp": 58, "selling_price": 56},
                                ],
                            },
                            {
                                "name": "Amul Gold Full Cream Milk",
                                "slug": "amul-gold-full-cream-milk",
                                "description": "Rich full cream milk.",
                                "image_url": "https://placehold.co/600x600?text=Amul+Gold",
                                "variants": [
                                    {"sku": "AMUL-GOLD-500ML", "value": "500", "unit": "ml", "mrp": 35, "selling_price": 34},
                                    {"sku": "AMUL-GOLD-1L", "value": "1", "unit": "L", "mrp": 70, "selling_price": 68},
                                ],
                            },
                        ],
                    },
                    {
                        "name": "Butter & Cheese",
                        "slug": "butter-cheese",
                        "image_url": "https://placehold.co/500x500?text=Butter+Cheese",
                        "products": [
                            {
                                "name": "Amul Butter",
                                "slug": "amul-butter",
                                "description": "Classic salted table butter.",
                                "image_url": "https://placehold.co/600x600?text=Amul+Butter",
                                "variants": [
                                    {"sku": "AMUL-BUTTER-100G", "value": "100", "unit": "g", "mrp": 62, "selling_price": 60},
                                    {"sku": "AMUL-BUTTER-500G", "value": "500", "unit": "g", "mrp": 285, "selling_price": 279},
                                ],
                            },
                            {
                                "name": "Amul Cheese Slices",
                                "slug": "amul-cheese-slices",
                                "description": "Processed cheese slices.",
                                "image_url": "https://placehold.co/600x600?text=Cheese+Slices",
                                "variants": [
                                    {"sku": "AMUL-CHEESE-10S", "value": "10", "unit": "slices", "mrp": 145, "selling_price": 139},
                                ],
                            },
                        ],
                    },
                ],
            }
        ],
    },
    {
        "brand": {
            "name": "Tata",
            "slug": "tata",
            "logo_url": "https://placehold.co/400x160?text=Tata",
        },
        "categories": [
            {
                "name": "Atta, Rice & Dal",
                "slug": "atta-rice-dal",
                "image_url": "https://placehold.co/500x500?text=Staples",
                "subcategories": [
                    {
                        "name": "Salt & Sugar",
                        "slug": "salt-sugar",
                        "image_url": "https://placehold.co/500x500?text=Salt+Sugar",
                        "products": [
                            {
                                "name": "Tata Salt",
                                "slug": "tata-salt",
                                "description": "Iodised packaged salt.",
                                "image_url": "https://placehold.co/600x600?text=Tata+Salt",
                                "variants": [
                                    {"sku": "TATA-SALT-1KG", "value": "1", "unit": "kg", "mrp": 30, "selling_price": 28},
                                ],
                            },
                            {
                                "name": "Tata Sampann Unpolished Toor Dal",
                                "slug": "tata-sampann-toor-dal",
                                "description": "Unpolished toor dal.",
                                "image_url": "https://placehold.co/600x600?text=Toor+Dal",
                                "variants": [
                                    {"sku": "TATA-TOOR-1KG", "value": "1", "unit": "kg", "mrp": 220, "selling_price": 199},
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "brand": {
            "name": "Coca-Cola",
            "slug": "coca-cola",
            "logo_url": "https://placehold.co/400x160?text=Coca-Cola",
        },
        "categories": [
            {
                "name": "Cold Drinks & Juices",
                "slug": "cold-drinks-juices",
                "image_url": "https://placehold.co/500x500?text=Drinks",
                "subcategories": [
                    {
                        "name": "Soft Drinks",
                        "slug": "soft-drinks",
                        "image_url": "https://placehold.co/500x500?text=Soft+Drinks",
                        "products": [
                            {
                                "name": "Coca-Cola Soft Drink",
                                "slug": "coca-cola-soft-drink",
                                "description": "Carbonated soft drink.",
                                "image_url": "https://placehold.co/600x600?text=Coca-Cola",
                                "variants": [
                                    {"sku": "COKE-250ML", "value": "250", "unit": "ml", "mrp": 20, "selling_price": 20},
                                    {"sku": "COKE-750ML", "value": "750", "unit": "ml", "mrp": 45, "selling_price": 42},
                                    {"sku": "COKE-2L", "value": "2", "unit": "L", "mrp": 95, "selling_price": 89},
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "brand": {
            "name": "Lay's",
            "slug": "lays",
            "logo_url": "https://placehold.co/400x160?text=Lays",
        },
        "categories": [
            {
                "name": "Munchies",
                "slug": "munchies",
                "image_url": "https://placehold.co/500x500?text=Munchies",
                "subcategories": [
                    {
                        "name": "Chips & Crisps",
                        "slug": "chips-crisps",
                        "image_url": "https://placehold.co/500x500?text=Chips",
                        "products": [
                            {
                                "name": "Lay's India's Magic Masala",
                                "slug": "lays-indias-magic-masala",
                                "description": "Spicy potato chips.",
                                "image_url": "https://placehold.co/600x600?text=Magic+Masala",
                                "variants": [
                                    {"sku": "LAYS-MAGIC-48G", "value": "48", "unit": "g", "mrp": 20, "selling_price": 20},
                                    {"sku": "LAYS-MAGIC-90G", "value": "90", "unit": "g", "mrp": 50, "selling_price": 47},
                                ],
                            },
                            {
                                "name": "Lay's Classic Salted",
                                "slug": "lays-classic-salted",
                                "description": "Classic salted potato chips.",
                                "image_url": "https://placehold.co/600x600?text=Classic+Salted",
                                "variants": [
                                    {"sku": "LAYS-CLASSIC-48G", "value": "48", "unit": "g", "mrp": 20, "selling_price": 20},
                                    {"sku": "LAYS-CLASSIC-90G", "value": "90", "unit": "g", "mrp": 50, "selling_price": 47},
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    },
    {
        "brand": {
            "name": "Surf Excel",
            "slug": "surf-excel",
            "logo_url": "https://placehold.co/400x160?text=Surf+Excel",
        },
        "categories": [
            {
                "name": "Cleaning Essentials",
                "slug": "cleaning-essentials",
                "image_url": "https://placehold.co/500x500?text=Cleaning",
                "subcategories": [
                    {
                        "name": "Laundry",
                        "slug": "laundry",
                        "image_url": "https://placehold.co/500x500?text=Laundry",
                        "products": [
                            {
                                "name": "Surf Excel Matic Front Load",
                                "slug": "surf-excel-matic-front-load",
                                "description": "Detergent powder for front-load washing machines.",
                                "image_url": "https://placehold.co/600x600?text=Surf+Excel",
                                "variants": [
                                    {"sku": "SURF-FRONT-1KG", "value": "1", "unit": "kg", "mrp": 275, "selling_price": 259},
                                    {"sku": "SURF-FRONT-2KG", "value": "2", "unit": "kg", "mrp": 520, "selling_price": 489},
                                ],
                            },
                        ],
                    }
                ],
            }
        ],
    },
]


# ---------------------------------------------------------------------
# API Client
# ---------------------------------------------------------------------

class BlinkitSeeder:
    def __init__(self, base_url: str, email: str, password: str, branch_id: Optional[str] = None):
        self.base_url = base_url.rstrip("/")
        self.email = email
        self.password = password
        self.branch_id = branch_id
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

        self.brands_by_slug: Dict[str, Dict[str, Any]] = {}
        self.categories_by_slug: Dict[str, Dict[str, Any]] = {}
        self.subcategories_by_slug: Dict[str, Dict[str, Any]] = {}
        self.products_by_slug: Dict[str, Dict[str, Any]] = {}
        self.variants_by_sku: Dict[str, Dict[str, Any]] = {}

        self.created = 0
        self.skipped = 0
        self.failed = 0

    def url(self, path: str) -> str:
        return f"{self.base_url}{path}"

    def login(self) -> None:
        print("\n🔐 Logging in...")
        response = self.session.post(
            self.url("/auth/login"),
            json={"email": self.email, "password": self.password},
            timeout=20,
        )

        if not response.ok:
            print(f"❌ Login failed: HTTP {response.status_code}")
            print(response.text)
            sys.exit(1)

        body = response.json()
        token = body.get("access_token")

        if not token:
            print("❌ Login response did not contain access_token")
            print(body)
            sys.exit(1)

        self.session.headers.update({"Authorization": f"Bearer {token}"})
        print("✅ Login successful")

    def request(self, method: str, path: str, *, json_body=None, params=None):
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
            print(f"❌ NETWORK {method} {path}: {exc}")
            return None

        if response.status_code in (401, 403):
            self.failed += 1
            print(f"🚫 {method} {path}: HTTP {response.status_code} - Unauthorized/Admin permission required")
            try:
                print("   ", response.json())
            except Exception:
                print("   ", response.text[:400])
            return None

        if not response.ok:
            self.failed += 1
            print(f"❌ {method} {path}: HTTP {response.status_code}")
            try:
                print("   ", response.json())
            except Exception:
                print("   ", response.text[:500])
            return None

        if response.status_code == 204 or not response.content:
            return {}

        try:
            return response.json()
        except ValueError:
            return {}

    def preload_existing(self) -> None:
        print("\n📦 Loading existing catalog...")

        brands = self.request("GET", "/brands", params={"skip": 0, "limit": 1000}) or []
        categories = self.request("GET", "/categories", params={"skip": 0, "limit": 1000}) or []
        subcategories = self.request("GET", "/subcategories", params={"skip": 0, "limit": 1000}) or []
        products = self.request("GET", "/products", params={"skip": 0, "limit": 1000}) or []
        variants = self.request("GET", "/product-variants", params={"skip": 0, "limit": 2000}) or []

        self.brands_by_slug = {x.get("slug"): x for x in brands if x.get("slug")}
        self.categories_by_slug = {x.get("slug"): x for x in categories if x.get("slug")}
        self.subcategories_by_slug = {x.get("slug"): x for x in subcategories if x.get("slug")}
        self.products_by_slug = {x.get("slug"): x for x in products if x.get("slug")}
        self.variants_by_sku = {x.get("sku"): x for x in variants if x.get("sku")}

        print(
            f"   Existing: {len(self.brands_by_slug)} brands, "
            f"{len(self.categories_by_slug)} categories, "
            f"{len(self.subcategories_by_slug)} subcategories, "
            f"{len(self.products_by_slug)} products, "
            f"{len(self.variants_by_sku)} variants"
        )

    def get_or_create_brand(self, data: Dict[str, Any]):
        slug = data["slug"]
        if slug in self.brands_by_slug:
            self.skipped += 1
            print(f"⏭️  Brand exists: {data['name']}")
            return self.brands_by_slug[slug]

        result = self.request("POST", "/brands", json_body={**data, "is_active": True})
        if result:
            self.created += 1
            self.brands_by_slug[slug] = result
            print(f"✅ Brand created: {data['name']}")
        return result

    def get_or_create_category(self, data: Dict[str, Any]):
        slug = data["slug"]
        if slug in self.categories_by_slug:
            self.skipped += 1
            print(f"⏭️  Category exists: {data['name']}")
            return self.categories_by_slug[slug]

        payload = {
            "name": data["name"],
            "slug": data["slug"],
            "image_url": data.get("image_url"),
            "is_active": True,
        }
        result = self.request("POST", "/categories", json_body=payload)
        if result:
            self.created += 1
            self.categories_by_slug[slug] = result
            print(f"✅ Category created: {data['name']}")
        return result

    def get_or_create_subcategory(self, data: Dict[str, Any], category_id: str):
        slug = data["slug"]
        if slug in self.subcategories_by_slug:
            self.skipped += 1
            print(f"⏭️  Subcategory exists: {data['name']}")
            return self.subcategories_by_slug[slug]

        payload = {
            "name": data["name"],
            "slug": data["slug"],
            "image_url": data.get("image_url"),
            "is_active": True,
            "category_unique_id": category_id,
        }
        result = self.request("POST", "/subcategories", json_body=payload)
        if result:
            self.created += 1
            self.subcategories_by_slug[slug] = result
            print(f"✅ Subcategory created: {data['name']}")
        return result

    def get_or_create_product(self, data: Dict[str, Any], brand_id: str, subcategory_id: str):
        slug = data["slug"]
        if slug in self.products_by_slug:
            self.skipped += 1
            print(f"⏭️  Product exists: {data['name']}")
            return self.products_by_slug[slug]

        payload = {
            "name": data["name"],
            "slug": data["slug"],
            "description": data.get("description"),
            "is_active": True,
            "brand_unique_id": brand_id,
            "subcategory_unique_id": subcategory_id,
        }

        result = self.request("POST", "/products", json_body=payload)
        if result:
            self.created += 1
            self.products_by_slug[slug] = result
            print(f"✅ Product created: {data['name']}")
        return result

    def get_or_create_variant(self, data: Dict[str, Any], product_id: str):
        sku = data["sku"]
        if sku in self.variants_by_sku:
            self.skipped += 1
            print(f"   ⏭️  Variant exists: {sku}")
            return self.variants_by_sku[sku]

        payload = {
            "sku": data["sku"],
            "value": str(data["value"]),
            "unit": data["unit"],
            "mrp": data["mrp"],
            "selling_price": data["selling_price"],
            "is_active": True,
            "product_unique_id": product_id,
        }

        result = self.request("POST", "/product-variants", json_body=payload)
        if result:
            self.created += 1
            self.variants_by_sku[sku] = result
            print(f"   ✅ Variant created: {sku}")
        return result

    def create_image_if_needed(self, product_id: str, image_url: Optional[str]):
        if not image_url:
            return

        existing = self.request("GET", f"/product-images/product/{product_id}") or []
        if any(img.get("image_url") == image_url for img in existing):
            self.skipped += 1
            print("   ⏭️  Product image already exists")
            return

        payload = {
            "image_url": image_url,
            "sort_order": 0,
            "is_primary": True,
            "product_unique_id": product_id,
        }

        result = self.request("POST", "/product-images", json_body=payload)
        if result:
            self.created += 1
            print("   ✅ Product image created")

    def create_inventory_if_needed(self, variant: Dict[str, Any]):
        if not self.branch_id or not variant:
            return

        variant_id = variant.get("unique_id")
        if not variant_id:
            return

        existing = self.request(
            "GET",
            f"/inventory/branch/{self.branch_id}/variant/{variant_id}"
        )

        if existing:
            self.skipped += 1
            print(f"      ⏭️  Inventory already exists for {variant.get('sku', variant_id)}")
            return

        # The GET endpoint may return 404 for missing inventory. request() prints that
        # error, but creation can still be attempted.
        payload = {
            "branch_unique_id": self.branch_id,
            "product_variant_unique_id": variant_id,
            "stock_quantity": 50,
            "selling_price_override": None,
            "is_available": True,
        }

        result = self.request("POST", "/inventory", json_body=payload)
        if result:
            self.created += 1
            print(f"      ✅ Inventory created: stock=50")

    def seed(self):
        self.login()
        self.preload_existing()

        print("\n🌱 Starting seed...\n")

        for group in SEED_DATA:
            brand_data = group["brand"]
            brand = self.get_or_create_brand(brand_data)
            if not brand:
                continue

            brand_id = brand.get("unique_id")
            if not brand_id:
                print(f"❌ Brand response missing unique_id: {brand_data['name']}")
                continue

            for category_data in group.get("categories", []):
                category = self.get_or_create_category(category_data)
                if not category:
                    continue

                category_id = category.get("unique_id")
                if not category_id:
                    print(f"❌ Category response missing unique_id: {category_data['name']}")
                    continue

                for subcategory_data in category_data.get("subcategories", []):
                    subcategory = self.get_or_create_subcategory(subcategory_data, category_id)
                    if not subcategory:
                        continue

                    subcategory_id = subcategory.get("unique_id")
                    if not subcategory_id:
                        print(f"❌ Subcategory response missing unique_id: {subcategory_data['name']}")
                        continue

                    for product_data in subcategory_data.get("products", []):
                        product = self.get_or_create_product(
                            product_data,
                            brand_id,
                            subcategory_id,
                        )
                        if not product:
                            continue

                        product_id = product.get("unique_id")
                        if not product_id:
                            print(f"❌ Product response missing unique_id: {product_data['name']}")
                            continue

                        self.create_image_if_needed(product_id, product_data.get("image_url"))

                        for variant_data in product_data.get("variants", []):
                            variant = self.get_or_create_variant(variant_data, product_id)

                            if self.branch_id and variant:
                                self.create_inventory_if_needed(variant)

        print("\n" + "=" * 60)
        print("🎉 Seed finished")
        print(f"✅ Created : {self.created}")
        print(f"⏭️  Skipped : {self.skipped}")
        print(f"❌ Failed  : {self.failed}")
        print("=" * 60)

        if not self.branch_id:
            print("\nℹ️  Inventory was not seeded because --branch-id was not supplied.")
            print("   Pass an existing branch unique_id to also create stock records.")


def parse_args():
    parser = argparse.ArgumentParser(description="Seed Blinkit API catalog data")
    parser.add_argument(
        "--base-url",
        default=os.getenv("BLINKIT_BASE_URL", "http://127.0.0.1:8000"),
        help="Backend API base URL",
    )
    parser.add_argument(
        "--email",
        default=os.getenv("BLINKIT_ADMIN_EMAIL"),
        help="Admin email",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("BLINKIT_ADMIN_PASSWORD"),
        help="Admin password",
    )
    parser.add_argument(
        "--branch-id",
        default=os.getenv("BLINKIT_BRANCH_ID"),
        help="Optional existing branch unique_id for inventory seeding",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if not args.email or not args.password:
        print("❌ Admin email/password required.")
        print()
        print("Example:")
        print(
            "python seed_blinkit.py "
            "--base-url http://127.0.0.1:8000 "
            "--email admin@example.com "
            "--password your_password"
        )
        sys.exit(1)

    seeder = BlinkitSeeder(
        base_url=args.base_url,
        email=args.email,
        password=args.password,
        branch_id=args.branch_id,
    )
    seeder.seed()


if __name__ == "__main__":
    main()