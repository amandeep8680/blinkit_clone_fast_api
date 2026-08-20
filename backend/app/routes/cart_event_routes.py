# app/routes/cart_event_routes.py

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
    get_cart_control_channel,
)


router = APIRouter(
    prefix="/cart",
    tags=["Cart Events"],
)


# =========================================================
# SSE Stream
# =========================================================

def cart_event_stream(
    pubsub,
    customer,
):
    """
    Listen to both:

    - inventory update channels
    - customer's subscription control channel
    """

    control_channel = (
        get_cart_control_channel(
            customer.id
        )
    )

    try:

        for message in pubsub.listen():

            if message["type"] != "message":
                continue

            channel = message["channel"]
            data = message["data"]

            # ---------------------------------------------
            # Internal subscription control message
            # ---------------------------------------------

            if channel == control_channel:

                command = json.loads(data)

                action = command.get(
                    "action"
                )

                inventory_channel = (
                    command.get("channel")
                )

                if action == "subscribe":

                    pubsub.subscribe(
                        inventory_channel
                    )

                elif action == "unsubscribe":

                    pubsub.unsubscribe(
                        inventory_channel
                    )

                # Control messages are INTERNAL.
                # Do not send them to frontend.
                continue

            # ---------------------------------------------
            # Actual inventory event
            # ---------------------------------------------

            yield (
                f"data: {data}\n\n"
            )

    finally:

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

    # Important:
    # Create/validate pubsub BEFORE StreamingResponse starts.
    pubsub = create_cart_pubsub(
        db,
        current_user,
    )

    return StreamingResponse(
        cart_event_stream(
            pubsub,
            current_user,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )