RATE_LIMIT_POLICIES = {

    "test_fixed": {
        "algorithm": "fixed_window",
        "limit": 3,
        "window_seconds": 10,
        "routes": [
            ("GET", "/test-fixed"),
        ],
    },

    "test_sliding": {
        "algorithm": "sliding_window",
        "limit": 3,
        "window_seconds": 10,
        "routes": [
            ("GET", "/test-sliding"),
        ],
    },

    "test_token": {
        "algorithm": "token_bucket",
        "capacity": 3,
        "refill_rate": 0.2,
        "routes": [
            ("GET", "/test-token"),
        ],
    },

    "test_leaky": {
        "algorithm": "leaky_bucket",
        "capacity": 3,
        "leak_rate": 0.2,
        "routes": [
            ("GET", "/test-leaky"),
        ],
    },
}


# RATE_LIMIT_POLICIES = {

#     # =====================================================
#     # SLIDING WINDOW - AUTH
#     # =====================================================

#     "auth_sensitive": {
#         "algorithm": "sliding_window",
#         "limit": 5,
#         "window_seconds": 60,

#         "routes": [
#             ("POST", "/auth/login"),
#             ("POST", "/customers/register"),
#         ],
#     },


#     # =====================================================
#     # SLIDING WINDOW - CRITICAL ACTIONS
#     # =====================================================

#     "critical_actions": {
#         "algorithm": "sliding_window",
#         "limit": 5,
#         "window_seconds": 300,

#         "routes": [
#             ("POST", "/orders"),
#             (
#                 "PATCH",
#                 "/orders/my/{order_unique_id}/cancel",
#             ),
#             (
#                 "DELETE",
#                 "/customers/{customer_unique_id}",
#             ),
#         ],
#     },


#     # =====================================================
#     # TOKEN BUCKET - HIGH TRAFFIC
#     # =====================================================

#     "public_browsing": {
#         "algorithm": "token_bucket",
#         "capacity": 100,
#         "refill_rate": 20,

#         "routes": [
#             ("GET", "/products"),
#             ("GET", "/products/active"),
#             ("GET", "/categories"),
#             ("GET", "/categories/active"),
#             ("GET", "/brands"),
#             ("GET", "/brands/active"),
#             (
#                 "GET",
#                 "/branch-catalog/{branch_unique_id}",
#             ),
#         ],
#     },


#     # =====================================================
#     # TOKEN BUCKET - NORMAL USER
#     # =====================================================

#     "user_actions": {
#         "algorithm": "token_bucket",
#         "capacity": 30,
#         "refill_rate": 5,

#         "routes": [
#             ("GET", "/cart"),
#             ("POST", "/cart"),
#             ("POST", "/cart/items"),
#             (
#                 "PATCH",
#                 "/cart/items/{product_variant_unique_id}",
#             ),
#             (
#                 "DELETE",
#                 "/cart/items/{product_variant_unique_id}",
#             ),
#             ("GET", "/orders/my"),
#             (
#                 "GET",
#                 "/orders/my/{order_unique_id}",
#             ),
#         ],
#     },


#     # =====================================================
#     # LEAKY BUCKET - ADMIN WRITES
#     # =====================================================

#     "admin_write": {
#         "algorithm": "leaky_bucket",
#         "capacity": 15,
#         "leak_rate": 3,

#         "routes": [
#             ("POST", "/products"),
#             (
#                 "PATCH",
#                 "/products/{product_unique_id}",
#             ),
#             ("POST", "/categories"),
#             (
#                 "PATCH",
#                 "/categories/{category_unique_id}",
#             ),
#             ("POST", "/brands"),
#             (
#                 "PATCH",
#                 "/brands/{brand_unique_id}",
#             ),
#         ],
#     },


#     # =====================================================
#     # LEAKY BUCKET - INVENTORY
#     # =====================================================

#     "inventory_write": {
#         "algorithm": "leaky_bucket",
#         "capacity": 20,
#         "leak_rate": 5,

#         "routes": [
#             ("POST", "/inventory"),

#             (
#                 "PATCH",
#                 "/inventory/branch/{branch_unique_id}/variant/"
#                 "{product_variant_unique_id}",
#             ),

#             (
#                 "PATCH",
#                 "/inventory/branch/{branch_unique_id}/variant/"
#                 "{product_variant_unique_id}/increase-stock",
#             ),

#             (
#                 "PATCH",
#                 "/inventory/branch/{branch_unique_id}/variant/"
#                 "{product_variant_unique_id}/decrease-stock",
#             ),
#         ],
#     },


#     # =====================================================
#     # FIXED WINDOW - SIMPLE ADMIN ACTIONS
#     # =====================================================

#     "simple_admin": {
#         "algorithm": "fixed_window",
#         "limit": 10,
#         "window_seconds": 60,

#         "routes": [
#             (
#                 "PATCH",
#                 "/products/{product_unique_id}/activate",
#             ),
#             (
#                 "PATCH",
#                 "/products/{product_unique_id}/deactivate",
#             ),
#             (
#                 "PATCH",
#                 "/categories/{category_unique_id}/activate",
#             ),
#             (
#                 "PATCH",
#                 "/categories/{category_unique_id}/deactivate",
#             ),
#             (
#                 "PATCH",
#                 "/brands/{brand_unique_id}/activate",
#             ),
#             (
#                 "PATCH",
#                 "/brands/{brand_unique_id}/deactivate",
#             ),
#         ],
#     },
# }