from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from app.core.database import get_db
from app.models.models import PromoCode
from app.schemas.schemas import PromoCodeCheck, PromoCodeResult

router = APIRouter(prefix="/api/promos", tags=["promos"])


@router.post("/check", response_model=PromoCodeResult)
async def check_promo(data: PromoCodeCheck, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PromoCode).where(
            PromoCode.code == data.code.upper(),
            PromoCode.is_active == True,
        )
    )
    promo = result.scalar_one_or_none()

    if not promo:
        return PromoCodeResult(valid=False, message="Invalid promo code.")

    if promo.expires_at and promo.expires_at < datetime.utcnow():
        return PromoCodeResult(valid=False, message="This promo code has expired.")

    if promo.max_uses and promo.used_count >= promo.max_uses:
        return PromoCodeResult(valid=False, message="This promo code has reached its usage limit.")

    if data.order_total < float(promo.min_order):
        return PromoCodeResult(
            valid=False,
            message=f"This code requires a minimum order of ${promo.min_order:.2f}.",
        )

    return PromoCodeResult(
        valid=True,
        discount_type=promo.discount_type,
        discount_value=float(promo.discount_value),
        message=f"Code applied! {int(promo.discount_value)}{'%' if promo.discount_type == 'percentage' else '$'} off your order.",
    )
