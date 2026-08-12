from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
)


unique_id = "88993719-b285-46f1-bcf8-f60be9d6cbea"


access_token = create_access_token(
    unique_id
)

refresh_token = create_refresh_token(
    unique_id
)


print("ACCESS:")
print(access_token)

print("REFRESH:")
print(refresh_token)


print("DECODED ACCESS:")
print(
    decode_token(access_token)
)