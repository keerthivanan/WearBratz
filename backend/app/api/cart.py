from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import uuid
import json
from typing import List

from app.core.database import get_db
from app.models.schemas import CartUpsert, CartResponse, WishlistToggle, WishlistResponse

router = APIRouter(tags=["cart-wishlist"])

# We use raw SQL tables (carts, wishlists) — define lightweight models here
from sqlalchemy import Table, Column, String, DateTime, MetaData
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy import text


# ================================================================
# CART ENDPOINTS
# ================================================================

@router.get("/cart/{session_id}")
async def get_cart(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get cart by session ID."""
    result = await db.execute(
        text("SELECT * FROM carts WHERE session_id = :sid"),
        {"sid": session_id}
    )
    row = result.mappings().first()
    if not row:
        return {"session_id": session_id, "items": [], "subtotal": 0}
    return dict(row)


@router.post("/cart")
async def save_cart(cart_in: CartUpsert, db: AsyncSession = Depends(get_db)):
    """Save or update cart for a session."""
    items_json = [item.model_dump() for item in cart_in.items]
    subtotal = sum(i["price"] * i["quantity"] for i in items_json)

    # Check if cart exists
    result = await db.execute(
        text("SELECT id FROM carts WHERE session_id = :sid"),
        {"sid": cart_in.session_id}
    )
    existing = result.first()

    items_str = json.dumps(items_json)

    if existing:
        await db.execute(
            text("UPDATE carts SET items = :items::jsonb, updated_at = NOW() WHERE session_id = :sid"),
            {"items": items_str, "sid": cart_in.session_id}
        )
    else:
        await db.execute(
            text("""INSERT INTO carts (id, session_id, customer_id, items, created_at, updated_at)
                    VALUES (:id, :sid, :cid, :items::jsonb, NOW(), NOW())"""),
            {
                "id": str(uuid.uuid4()),
                "sid": cart_in.session_id,
                "cid": cart_in.customer_id,
                "items": items_str,
            }
        )
    await db.commit()
    return {"status": "saved", "session_id": cart_in.session_id, "item_count": len(items_json), "subtotal": subtotal}


@router.delete("/cart/{session_id}")
async def clear_cart(session_id: str, db: AsyncSession = Depends(get_db)):
    """Clear entire cart for a session."""
    await db.execute(
        text("DELETE FROM carts WHERE session_id = :sid"),
        {"sid": session_id}
    )
    await db.commit()
    return {"status": "cleared", "session_id": session_id}


# ================================================================
# WISHLIST ENDPOINTS
# ================================================================

@router.get("/wishlist/{session_id}")
async def get_wishlist(session_id: str, db: AsyncSession = Depends(get_db)):
    """Get wishlist product IDs for a session."""
    result = await db.execute(
        text("SELECT product_id, created_at FROM wishlists WHERE session_id = :sid"),
        {"sid": session_id}
    )
    rows = result.mappings().all()
    return {"session_id": session_id, "product_ids": [dict(r)["product_id"] for r in rows]}


@router.post("/wishlist/toggle")
async def toggle_wishlist(toggle: WishlistToggle, db: AsyncSession = Depends(get_db)):
    """Toggle a product in the wishlist (add if not present, remove if exists)."""
    result = await db.execute(
        text("SELECT id FROM wishlists WHERE session_id = :sid AND product_id = :pid"),
        {"sid": toggle.session_id, "pid": toggle.product_id}
    )
    existing = result.first()

    if existing:
        # Remove from wishlist
        await db.execute(
            text("DELETE FROM wishlists WHERE session_id = :sid AND product_id = :pid"),
            {"sid": toggle.session_id, "pid": toggle.product_id}
        )
        # Decrement wishlist count
        await db.execute(
            text("UPDATE products SET wishlist_count = GREATEST(0, wishlist_count - 1) WHERE id = :pid"),
            {"pid": toggle.product_id}
        )
        await db.commit()
        return {"action": "removed", "product_id": toggle.product_id}
    else:
        # Add to wishlist
        await db.execute(
            text("""INSERT INTO wishlists (id, session_id, customer_id, product_id, created_at)
                    VALUES (:id, :sid, :cid, :pid, NOW())
                    ON CONFLICT (session_id, product_id) DO NOTHING"""),
            {
                "id": str(uuid.uuid4()),
                "sid": toggle.session_id,
                "cid": toggle.customer_id,
                "pid": toggle.product_id,
            }
        )
        # Increment wishlist count
        await db.execute(
            text("UPDATE products SET wishlist_count = wishlist_count + 1 WHERE id = :pid"),
            {"pid": toggle.product_id}
        )
        await db.commit()
        return {"action": "added", "product_id": toggle.product_id}
