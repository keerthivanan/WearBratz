from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import uuid
import httpx
import os

from app.core.database import get_db
from app.models.schemas import PromoCodeValidate, PromoCodeResponse, SubscriberCreate

router = APIRouter(tags=["store"])

N8N_SUBSCRIBE_WEBHOOK = os.getenv("N8N_WEBHOOK_SUBSCRIBE_URL", "")


# ================================================================
# PROMO CODES
# ================================================================

@router.post("/promo/validate", response_model=PromoCodeResponse)
async def validate_promo_code(body: PromoCodeValidate, db: AsyncSession = Depends(get_db)):
    """Validate a promo code and calculate the discount amount."""
    result = await db.execute(
        text("""SELECT * FROM promo_codes 
                WHERE UPPER(code) = UPPER(:code) 
                AND is_active = true
                AND (expires_at IS NULL OR expires_at > NOW())
                AND (max_uses IS NULL OR used_count < max_uses)"""),
        {"code": body.code}
    )
    promo = result.mappings().first()

    if not promo:
        return PromoCodeResponse(valid=False, message="Invalid or expired promo code.")

    promo = dict(promo)

    if body.order_subtotal < (promo.get("min_order") or 0):
        return PromoCodeResponse(
            valid=False,
            message=f"Minimum order of ${promo['min_order']:.2f} required for this code."
        )

    if promo["discount_type"] == "percentage":
        discount_amount = round(body.order_subtotal * (promo["discount_value"] / 100), 2)
    else:  # fixed
        discount_amount = min(promo["discount_value"], body.order_subtotal)

    return PromoCodeResponse(
        valid=True,
        code=promo["code"],
        discount_type=promo["discount_type"],
        discount_value=promo["discount_value"],
        discount_amount=discount_amount,
        message=f"Code applied! You saved ${discount_amount:.2f}."
    )


# ================================================================
# EMAIL SUBSCRIBERS
# ================================================================

@router.post("/subscribe", status_code=201)
async def subscribe_to_newsletter(subscriber: SubscriberCreate, db: AsyncSession = Depends(get_db)):
    """Subscribe to newsletter. Triggers n8n welcome email workflow."""
    
    # Check if already subscribed
    result = await db.execute(
        text("SELECT id, is_active FROM email_subscribers WHERE email = :email"),
        {"email": subscriber.email}
    )
    existing = result.mappings().first()

    if existing:
        if existing["is_active"]:
            return {"status": "already_subscribed", "message": "You're already on the list!"}
        else:
            # Re-activate
            await db.execute(
                text("UPDATE email_subscribers SET is_active = true WHERE email = :email"),
                {"email": subscriber.email}
            )
    else:
        await db.execute(
            text("INSERT INTO email_subscribers (id, email, source, is_active, created_at) VALUES (:id, :email, :source, true, NOW())"),
            {"id": str(uuid.uuid4()), "email": subscriber.email, "source": subscriber.source}
        )

    await db.commit()

    # Trigger n8n workflow 04 (welcome email)
    if N8N_SUBSCRIBE_WEBHOOK:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(N8N_SUBSCRIBE_WEBHOOK, json={
                    "email": subscriber.email,
                    "event": "new_subscriber",
                })
        except Exception as e:
            print(f"n8n subscribe webhook failed (non-critical): {e}")

    return {"status": "subscribed", "message": "Welcome to the fam! Check your inbox for your 10% discount code 💅"}


@router.get("/subscribe/count")
async def get_subscriber_count(db: AsyncSession = Depends(get_db)):
    """Get total active subscriber count."""
    result = await db.execute(
        text("SELECT COUNT(*) FROM email_subscribers WHERE is_active = true")
    )
    count = result.scalar()
    return {"total_subscribers": count}
