from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)


unique_id = "88993719-b285-46f1-bcf8-f60be9d6cbea"
role = "super_admin"


access_token = create_access_token(
    unique_id=unique_id,
    role=role
)

refresh_token = create_refresh_token(
    unique_id=unique_id,
    role=role
)


print("\nACCESS TOKEN:")
print(access_token)


print("\nDECODED ACCESS TOKEN:")
print(
    decode_token(access_token)
)


print("\nDECODED REFRESH TOKEN:")
print(
    decode_token(refresh_token)
)