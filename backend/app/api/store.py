from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
import uuid
from typing import Any

from app.core.database import get_db
from app.models import ProductWaitlist, AbandonedCart, ProductReview
from app.models.schemas import WaitlistCreate, AbandonedCartCreate, ProductReviewCreate

router = APIRouter(tags=["store-features"])

@router.post("/waitlist", status_code=201)
async def join_waitlist(waitlist_in: WaitlistCreate, db: AsyncSession = Depends(get_db)):
    waitlist_entry = ProductWaitlist(**waitlist_in.model_dump())
    waitlist_entry.id = str(uuid.uuid4())
    db.add(waitlist_entry)
    await db.commit()
    return {"status": "success", "message": "Joined waitlist."}

@router.post("/abandoned-carts", status_code=200)
async def update_abandoned_cart(cart_in: AbandonedCartCreate, db: AsyncSession = Depends(get_db)):
    # Upsert logic based on session_id
    stmt = select(AbandonedCart).where(AbandonedCart.session_id == cart_in.session_id)
    result = await db.execute(stmt)
    existing_cart = result.scalar_one_or_none()
    
    if existing_cart:
        existing_cart.items = cart_in.items
        existing_cart.subtotal = cart_in.subtotal
        if cart_in.customer_email:
            existing_cart.customer_email = cart_in.customer_email
    else:
        new_cart = AbandonedCart(**cart_in.model_dump())
        new_cart.id = str(uuid.uuid4())
        db.add(new_cart)
    
    await db.commit()
    return {"status": "success"}

@router.post("/product-reviews", status_code=201)
async def submit_review(review_in: ProductReviewCreate, db: AsyncSession = Depends(get_db)):
    new_review = ProductReview(**review_in.model_dump())
    new_review.id = str(uuid.uuid4())
    db.add(new_review)
    await db.commit()
    return {"status": "pending_approval", "message": "Review submitted successfully."}


@router.get("/product-reviews")
async def get_reviews(product_id: str = Query(...), db: AsyncSession = Depends(get_db)):
    """Get approved reviews for a product."""
    result = await db.execute(
        select(ProductReview).where(
            ProductReview.product_id == product_id,
            ProductReview.status == "approved",
        ).order_by(ProductReview.created_at.desc())
    )
    return result.scalars().all()


@router.get("/abandoned-carts")
async def get_abandoned_carts(db: AsyncSession = Depends(get_db)):
    """Get abandoned carts for n8n recovery workflows."""
    result = await db.execute(
        text("""
            SELECT id, session_id, customer_email, items, subtotal,
                   EXTRACT(EPOCH FROM (NOW() - updated_at)) / 3600 AS hours_since_abandoned
            FROM abandoned_carts
            WHERE recovered = false
              AND customer_email IS NOT NULL
              AND updated_at < NOW() - INTERVAL '1 hour'
            ORDER BY updated_at DESC
            LIMIT 100
        """)
    )
    return [dict(row) for row in result.mappings()]


@router.get("/waitlist/{product_id}")
async def get_waitlist(product_id: str, db: AsyncSession = Depends(get_db)):
    """Get waitlist subscribers for a product (used by n8n restock workflow)."""
    result = await db.execute(
        select(ProductWaitlist).where(
            ProductWaitlist.product_id == product_id,
            ProductWaitlist.notified == False,  # noqa: E712
        )
    )
    entries = result.scalars().all()
    return [{"customer_email": e.customer_email, "product_id": e.product_id} for e in entries]
