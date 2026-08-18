# Blinkit Customer UI

A responsive customer storefront wired to the supplied Blinkit FastAPI OpenAPI contract.

## Included flows
- Customer registration: `POST /customers/register`
- Login: `POST /auth/login`
- Refresh token: `POST /auth/refresh`
- Branch selection: `GET /branches/`
- Live branch catalog: `GET /branch-catalog/{branch_unique_id}`
- Cart create/get: `POST /cart`, `GET /cart`
- Add item: `POST /cart/items`
- Change quantity: `PATCH /cart/items/{product_variant_unique_id}`
- Remove item: `DELETE /cart/items/{product_variant_unique_id}`
- Clear cart: `DELETE /cart/clear`
- Customer profile/details when customer unique ID is known
- Add and view customer addresses

## Important
The supplied OpenAPI contract has no order/checkout endpoint. The checkout button therefore explains that checkout is not wired instead of inventing an API.

The customer-address routes require `customer_unique_id`. Registration returns it, so newly registered users work automatically. For existing logins, the UI tries to infer an ID from common JWT claims; if your JWT uses a different claim, paste the customer unique ID under Account → API settings, or add a `/customers/me` endpoint later.

## Run
```bash
cd blinkit-customer-ui
python -m http.server 5600
```

Open:
`http://localhost:5600`

Default backend:
`http://127.0.0.1:8000`

## CORS
Add `http://localhost:5600` and `http://127.0.0.1:5600` to the FastAPI CORS allowlist.
