# app/realtime/cart_subscription.py

import json

from sqlalchemy.orm import Session

from app.models.cart_model import Cart
from app.core.redis import redis_client

from app.realtime.inventory_pubsub import (
    get_inventory_channel,
)

from app.exceptions.custom_exceptions import (
    NotFoundException,
)

from app.exceptions import messages as msg


# =========================================================
# Customer Cart Control Channel
# =========================================================

def get_cart_control_channel(
    customer_id: int,
) -> str:
    """
    Internal Redis channel used to tell an already-open
    SSE connection to subscribe/unsubscribe inventory channels.
    """

    return f"cart-subscriptions:{customer_id}"


# =========================================================
# Current Cart Inventory Channels
# =========================================================

def get_customer_cart_channels(
    db: Session,
    customer,
) -> list[str]:
    """
    Return inventory Redis channels for all items
    currently present in customer's active cart.
    """

    cart = (
        db.query(Cart)
        .filter(
            Cart.customer_id == customer.id,
            Cart.is_active.is_(True),
        )
        .first()
    )

    if not cart:
        raise NotFoundException(
            msg.CART_NOT_FOUND
        )

    channels = []

    for item in cart.items:

        channel = get_inventory_channel(
            branch_id=cart.branch_id,
            product_variant_id=(
                item.product_variant_id
            ),
        )

        channels.append(channel)

    return channels


# =========================================================
# Create Customer PubSub
# =========================================================

def create_cart_pubsub(
    db: Session,
    customer,
):
    """
    Create Redis subscriber for:

    1. Current cart inventory channels
    2. Customer's control channel
    """

    inventory_channels = (
        get_customer_cart_channels(
            db,
            customer,
        )
    )

    control_channel = (
        get_cart_control_channel(
            customer.id
        )
    )

    pubsub = redis_client.pubsub()

    # Always subscribe to control channel.
    # Even if cart becomes empty, this stays alive
    # so new cart items can later be subscribed.
    pubsub.subscribe(
        control_channel
    )

    if inventory_channels:
        pubsub.subscribe(
            *inventory_channels
        )

    return pubsub


# =========================================================
# Publish Subscription Changes
# =========================================================

def publish_cart_subscription_change(
    customer_id: int,
    action: str,
    branch_id: int,
    product_variant_id: int,
):
    """
    Tell customer's currently-open SSE subscriber
    to dynamically subscribe/unsubscribe one inventory channel.
    """

    if action not in {
        "subscribe",
        "unsubscribe",
    }:
        raise ValueError(
            "Invalid subscription action"
        )

    control_channel = (
        get_cart_control_channel(
            customer_id
        )
    )

    inventory_channel = (
        get_inventory_channel(
            branch_id=branch_id,
            product_variant_id=(
                product_variant_id
            ),
        )
    )

    payload = {
        "action": action,
        "channel": inventory_channel,
    }

    redis_client.publish(
        control_channel,
        json.dumps(payload),
    )