# app/realtime/inventory_pubsub.py

import json

from app.core.redis import redis_client


def get_inventory_channel(
    branch_id: int,
    product_variant_id: int,
) -> str:
    """
    Build Redis channel name for one
    Branch + ProductVariant combination.
    """

    return (
        f"inventory:{branch_id}:"
        f"{product_variant_id}"
    )


def publish_inventory_update(
    branch_id: int,
    product_variant_id: int,
    stock_quantity: int,
    is_available: bool,
):
    """
    Publish latest inventory state to Redis.
    """

    channel = get_inventory_channel(
        branch_id,
        product_variant_id,
    )

    payload = {
        "branch_id": branch_id,
        "product_variant_id": (
            product_variant_id
        ),
        "stock_quantity": stock_quantity,
        "is_available": is_available,
    }

    redis_client.publish(
        channel,
        json.dumps(payload),
    )