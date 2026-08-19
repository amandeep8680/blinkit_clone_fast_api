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

# =========================
# Branch Inventory Messages
# =========================

INVENTORY_ALREADY_EXISTS = "Inventory item already exists for this branch and product variant."
INVENTORY_NOT_FOUND = "Inventory item not found."
INVENTORY_ALREADY_ACTIVE = "Inventory item is already available."
INVENTORY_ALREADY_INACTIVE = "Inventory item is already unavailable."
INVENTORY_DELETED = "Inventory item deleted successfully."
INVALID_STOCK_QUANTITY = "Stock quantity cannot be negative."
INSUFFICIENT_STOCK = "Insufficient stock available."



# =========================
# Customer Messages
# =========================

CUSTOMER_ALREADY_EXISTS = "Customer already exists."
CUSTOMER_EMAIL_ALREADY_EXISTS = "Customer with this email already exists."
CUSTOMER_PHONE_ALREADY_EXISTS = "Customer with this phone number already exists."
CUSTOMER_NOT_FOUND = "Customer not found."
CUSTOMER_ALREADY_ACTIVE = "Customer account is already active."
CUSTOMER_ALREADY_INACTIVE = "Customer account is already inactive."
CUSTOMER_DELETED = "Customer deleted successfully."


# =========================
# Customer Address Messages
# =========================

CUSTOMER_ADDRESS_NOT_FOUND = "Customer address not found."
CUSTOMER_ADDRESS_LABEL_ALREADY_EXISTS = "Address with this label already exists."
CUSTOMER_ADDRESS_DELETED = "Customer address deleted successfully."
CUSTOMER_ADDRESS_ALREADY_ACTIVE = "Customer address is already active."
CUSTOMER_ADDRESS_ALREADY_INACTIVE = "Customer address is already inactive."






# =========================
# Cart Messages
# =========================

CART_ALREADY_EXISTS = "Customer already has an active cart."
CART_NOT_FOUND = "Active cart not found."
CART_CREATED = "Cart created successfully."
CART_CLEARED = "Cart cleared successfully."


# =========================
# Cart Item Messages
# =========================

CART_ITEM_NOT_FOUND = "Cart item not found."
CART_ITEM_DELETED = "Cart item removed successfully."
INVALID_CART_QUANTITY = "Cart quantity must be greater than zero."
CART_QUANTITY_EXCEEDS_STOCK = "Requested quantity exceeds available stock."
PRODUCT_NOT_AVAILABLE = "Product is not available in this branch."
PRODUCT_VARIANT_INACTIVE = "Product variant is inactive."
BRANCH_INACTIVE = "Branch is inactive."



# =========================
# Branch Catalog Messages
# =========================

BRANCH_INACTIVE = (
    "Selected branch is currently inactive."
)



BRAND_HAS_PRODUCTS = (
    "Brand cannot be deleted because products are linked to it."
)


# =========================
# Cart Related Messages
# =========================

CART_CREATED = "Cart created successfully"
CART_CLEARED = "Cart cleared successfully"
CART_DELETED = "Cart deleted successfully"

# =========================
# Order Messages
# =========================

ORDER_NOT_FOUND = "Order not found."
ORDER_CREATED = "Order placed successfully."
ORDER_CANCELLED = "Order cancelled successfully."

ORDER_EMPTY_CART = "Cannot place an order with an empty cart."

ORDER_ALREADY_CANCELLED = "Order is already cancelled."
ORDER_ALREADY_DELIVERED = "Delivered order cannot be modified."
ORDER_CANNOT_CANCEL = "This order can no longer be cancelled."

INVALID_ORDER_STATUS = "Invalid order status."
INVALID_ORDER_STATUS_TRANSITION = "Invalid order status transition."

ORDER_BRANCH_INACTIVE = "Order branch is currently inactive."

ORDER_ITEM_OUT_OF_STOCK = "One or more cart items are out of stock."
ORDER_ITEM_NOT_AVAILABLE = "One or more cart items are unavailable."

ORDER_ADDRESS_NOT_FOUND = "Selected customer address was not found."


# =========================
# Payment Messages
# =========================

INVALID_PAYMENT_METHOD = "Invalid payment method."
INVALID_PAYMENT_STATUS = "Invalid payment status."
PAYMENT_STATUS_UPDATED = "Payment status updated successfully."