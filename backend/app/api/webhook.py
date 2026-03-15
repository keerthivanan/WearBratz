from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import Order, OrderStatusHistory
from app.schemas.schemas import WebhookPayload

router = APIRouter(prefix="/api/webhook", tags=["webhook"])


@router.post("")
async def handle_webhook(payload: WebhookPayload, db: AsyncSession = Depends(get_db)):
    """Receive callbacks from n8n workflows to update order status."""
    event = payload.event
    data = payload.data

    if event == "order.shipped":
        order_id = data.get("order_id") or data.get("order_number")
        tracking_number = data.get("tracking_number")

        result = await db.execute(
            select(Order).where(
                (Order.id == order_id) | (Order.order_number == order_id)
            )
        )
        order = result.scalar_one_or_none()
        if order:
            old_status = order.status
            order.status = "shipped"
            order.tracking_number = tracking_number
            history = OrderStatusHistory(
                order_id=order.id,
                old_status=old_status,
                new_status="shipped",
                note=f"Tracking: {tracking_number}",
            )
            db.add(history)
            await db.commit()

    elif event == "order.delivered":
        order_id = data.get("order_id") or data.get("order_number")
        result = await db.execute(
            select(Order).where(
                (Order.id == order_id) | (Order.order_number == order_id)
            )
        )
        order = result.scalar_one_or_none()
        if order:
            old_status = order.status
            order.status = "delivered"
            history = OrderStatusHistory(
                order_id=order.id,
                old_status=old_status,
                new_status="delivered",
            )
            db.add(history)
            await db.commit()

    return {"received": True, "event": event}
