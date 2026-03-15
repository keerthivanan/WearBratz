from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.core.database import get_db
from app.models.models import Wishlist, Product
from app.schemas.schemas import WishlistToggle, MessageResponse

router = APIRouter(prefix="/api/wishlist", tags=["wishlist"])


@router.get("/{session_id}")
async def get_wishlist(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Wishlist).where(Wishlist.session_id == session_id)
    )
    items = result.scalars().all()

    out = []
    for item in items:
        prod_result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = prod_result.scalar_one_or_none()
        out.append({
            "id": item.id,
            "product_id": item.product_id,
            "product": {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "category": product.category,
                "emoji": product.emoji,
                "stock": product.stock,
                "tag": product.tag,
                "image_url": product.image_url,
            } if product else None,
            "created_at": item.created_at,
        })
    return out


@router.post("")
async def toggle_wishlist(data: WishlistToggle, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Wishlist).where(
            Wishlist.session_id == data.session_id,
            Wishlist.product_id == data.product_id,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        await db.execute(
            delete(Wishlist).where(
                Wishlist.session_id == data.session_id,
                Wishlist.product_id == data.product_id,
            )
        )
        await db.commit()
        return {"action": "removed", "message": "Removed from wishlist"}
    else:
        item = Wishlist(
            session_id=data.session_id,
            product_id=data.product_id,
            customer_id=data.customer_id,
        )
        db.add(item)
        await db.commit()
        return {"action": "added", "message": "Added to wishlist"}
