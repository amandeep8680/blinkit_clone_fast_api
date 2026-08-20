# app/realtime/cart_subscription.py

from sqlalchemy.orm import Session

from app.models.cart_model import Cart
from app.core.redis import redis_client

from app.exceptions.custom_exceptions import (
    NotFoundException,
)

from app.exceptions import messages as msg


def get_customer_cart_channels(
    db: Session,
    customer,
) -> list[str]:
    """
    Return Redis inventory channels for all
    items currently present in customer's active cart.
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

        channel = (
            f"inventory:{cart.branch_id}:"
            f"{item.product_variant_id}"
        )

        channels.append(channel)

    return channels



def create_cart_pubsub(
    db: Session,
    customer,
):
    """
    Create Redis Pub/Sub subscriber for
    customer's current cart items.
    """

    channels = get_customer_cart_channels(
        db,
        customer,
    )

    pubsub = redis_client.pubsub()

    if channels:
        pubsub.subscribe(
            *channels
        )

    return pubsub