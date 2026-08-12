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