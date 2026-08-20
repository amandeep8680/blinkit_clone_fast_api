# app/routes/cart_event_routes.py

# curl -N \
# -H "Authorization: Bearer TOKEN" \
# http://127.0.0.1:8000/cart/events
import json

from fastapi import (
    APIRouter,
    Depends,
)

from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.auth.authorization import require_roles
from app.constants import roles

from app.realtime.cart_subscription import (
    create_cart_pubsub,
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart Events"],
)


# =========================================================
# SSE Stream
# =========================================================

def cart_event_stream(
    db: Session,
    customer,
):
    """
    Listen to Redis inventory channels for
    customer's cart and stream events to frontend.
    """

    pubsub = create_cart_pubsub(
        db,
        customer,
    )

    try:
        for message in pubsub.listen():

            # Redis also sends subscribe/unsubscribe messages.
            # We only want actual published inventory messages.
            if message["type"] != "message":
                continue

            data = message["data"]

            # SSE format:
            #
            # data: {...}
            #
            # Blank line is required after every SSE event.
            yield (
                f"data: {data}\n\n"
            )

    finally:
        # Customer closes cart screen / connection disconnects.
        pubsub.close()


# =========================================================
# Cart Inventory Events
# =========================================================

@router.get(
    "/events",
)
def cart_events(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            roles.CUSTOMER
        )
    ),
):
    """
    Open SSE connection for logged-in customer's cart.
    """

    return StreamingResponse(
        cart_event_stream(
            db,
            current_user,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )