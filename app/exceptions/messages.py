# app/exceptions/messages.py

# =========================
# Authentication Messages
# =========================

INVALID_CREDENTIALS = "Invalid email or password."
UNAUTHORIZED = "Authentication required."
INVALID_TOKEN = "Invalid authentication token."
TOKEN_EXPIRED = "Authentication token has expired."


# =========================
# Authorization Messages
# =========================

FORBIDDEN = "You do not have permission to perform this action."


# =========================
# Super Admin Messages
# =========================

ALREADY_EXISTS = " Admin already exists."
ADMIN_NOT_FOUND = "Admin not found."
ADMIN_INACTIVE = "Admin account is inactive."


# =========================
# Branch Manager Messages
# =========================

BRANCH_MANAGER_ALREADY_EXISTS = "Branch Manager already exists."
BRANCH_MANAGER_NOT_FOUND = "Branch Manager not found."
BRANCH_MANAGER_INACTIVE = "Branch Manager account is inactive."


# =========================
# Branch Messages
# =========================

BRANCH_ALREADY_EXISTS = "Branch already exists."
BRANCH_NOT_FOUND = "Branch not found."


# =========================
# General Messages
# =========================

INTERNAL_SERVER_ERROR = "Something went wrong."



# =========================
# JWT Token Messages
# =========================

TOKEN_EXPIRED = "Authentication token has expired."
INVALID_TOKEN = "Invalid authentication token."


# =========================
# Branch Related Messages
# =========================

BRANCH_ALREADY_EXISTS = "Branch already exists."
BRANCH_NOT_FOUND = "Branch not found."

# =========================
# Brand Messages
# =========================

BRAND_ALREADY_EXISTS = "Brand already exists."
BRAND_NAME_ALREADY_EXISTS = "Brand with this name already exists."
BRAND_SLUG_ALREADY_EXISTS = "Brand with this slug already exists."
BRAND_NOT_FOUND = "Brand not found."
BRAND_ALREADY_ACTIVE = "Brand is already active."
BRAND_ALREADY_INACTIVE = "Brand is already inactive."
BRAND_DELETED = "Brand deleted successfully."

# =========================
# Category Messages
# =========================

CATEGORY_ALREADY_EXISTS = "Category already exists."
CATEGORY_NAME_ALREADY_EXISTS = "Category with this name already exists."
CATEGORY_SLUG_ALREADY_EXISTS = "Category with this slug already exists."
CATEGORY_NOT_FOUND = "Category not found."
CATEGORY_ALREADY_ACTIVE = "Category is already active."
CATEGORY_ALREADY_INACTIVE = "Category is already inactive."
CATEGORY_DELETED = "Category deleted successfully."


# =========================
# SubCategory Messages
# =========================

SUBCATEGORY_ALREADY_EXISTS = "SubCategory already exists."
SUBCATEGORY_NAME_ALREADY_EXISTS = "SubCategory with this name already exists."
SUBCATEGORY_SLUG_ALREADY_EXISTS = "SubCategory with this slug already exists."
SUBCATEGORY_NOT_FOUND = "SubCategory not found."
SUBCATEGORY_ALREADY_ACTIVE = "SubCategory is already active."
SUBCATEGORY_ALREADY_INACTIVE = "SubCategory is already inactive."
SUBCATEGORY_DELETED = "SubCategory deleted successfully."


# =========================
# Product Messages
# =========================

PRODUCT_ALREADY_EXISTS = "Product already exists."
PRODUCT_NAME_ALREADY_EXISTS = "Product with this name already exists."
PRODUCT_SLUG_ALREADY_EXISTS = "Product with this slug already exists."
PRODUCT_NOT_FOUND = "Product not found."
PRODUCT_ALREADY_ACTIVE = "Product is already active."
PRODUCT_ALREADY_INACTIVE = "Product is already inactive."
PRODUCT_DELETED = "Product deleted successfully."


# =========================
# Product Variant Messages
# =========================

PRODUCT_VARIANT_ALREADY_EXISTS = "Product variant already exists."
PRODUCT_VARIANT_NOT_FOUND = "Product variant not found."
PRODUCT_VARIANT_SKU_ALREADY_EXISTS = "Product variant with this SKU already exists."
PRODUCT_VARIANT_ALREADY_ACTIVE = "Product variant is already active."
PRODUCT_VARIANT_ALREADY_INACTIVE = "Product variant is already inactive."
PRODUCT_VARIANT_DELETED = "Product variant deleted successfully."
INVALID_PRODUCT_VARIANT_PRICE = "Selling price cannot be greater than MRP."


# =========================
# Product Image Messages
# =========================

PRODUCT_IMAGE_NOT_FOUND = "Product image not found."
PRODUCT_IMAGE_DELETED = "Product image deleted successfully."
PRODUCT_PRIMARY_IMAGE_ALREADY_EXISTS = "A primary image already exists for this product."