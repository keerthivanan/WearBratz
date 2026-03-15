from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import httpx
import os
from app.core.database import get_db
from app.models.models import EmailSubscriber
from app.schemas.schemas import SubscribeRequest, SubscribeResponse

router = APIRouter(prefix="/api/subscribe", tags=["subscribe"])


@router.post("", response_model=SubscribeResponse)
async def subscribe(data: SubscribeRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(EmailSubscriber).where(EmailSubscriber.email == data.email)
    )
    existing = result.scalar_one_or_none()

    if existing:
        if not existing.is_active:
            existing.is_active = True
            await db.commit()
            return SubscribeResponse(success=True, message="Welcome back! You've been re-subscribed.")
        return SubscribeResponse(success=True, message="You're already subscribed!")

    subscriber = EmailSubscriber(email=data.email, source=data.source)
    db.add(subscriber)
    await db.commit()

    # Trigger n8n welcome email workflow (non-blocking)
    n8n_url = os.getenv("N8N_WEBHOOK_SUBSCRIBE_URL")
    if n8n_url:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(n8n_url, json={"email": data.email, "source": data.source})
        except Exception:
            pass

    return SubscribeResponse(success=True, message="Welcome to the Bratz circle! Check your email for a special gift.")
