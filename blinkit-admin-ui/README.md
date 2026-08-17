# BlinkOps Admin & Manager UI

Static frontend generated from the supplied **Blinkit API OpenAPI 3.1** document.

## Run

Because `openapi.json` is fetched by the browser, serve this folder over HTTP rather than opening `index.html` directly.

```bash
cd blinkit-admin-ui
python -m http.server 5500
```

Open `http://localhost:5500` and enter your backend base URL (for example `http://127.0.0.1:8000`) on the login screen.

## Included

- Admin / Branch Manager login using `POST /auth/login`
- Refresh-token retry using `POST /auth/refresh`
- 401 / 403 unauthorized handling for protected APIs
- Branch CRUD
- Branch Manager CRUD
- Brand CRUD + activation/deactivation
- Category + nested Subcategory CRUD
- Product CRUD
- Product Variant CRUD
- Product Image create/list/edit/delete workflow
- Branch Inventory list/create + stock increase/decrease
- Customer CRUD controls
- Branch Catalog preview by branch
- Super Admin profile/update/delete
- OpenAPI-powered API Console covering every operation in the supplied spec, including customer address and cart endpoints

## Important role note

The supplied OpenAPI file declares Bearer authentication but does **not** document which endpoints are Admin-only versus Manager-accessible. Therefore the frontend does not invent authorization rules. It uses the backend as the authority: any `401`/`403` becomes an Unauthorized Access experience. If the JWT contains a `role` claim, the UI also labels Admin-only-looking sections, but backend authorization remains definitive.

## CORS

If frontend and backend run on different origins, your FastAPI backend must allow the frontend origin through CORS.
