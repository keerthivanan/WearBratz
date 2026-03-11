from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
import uuid
import httpx
import os
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models import Order, Customer, InventoryLog
from app.models.schemas import OrderCreate, OrderResponse, OrderUpdateStatus

router = APIRouter(prefix="/orders", tags=["orders"])

N8N_ORDER_WEBHOOK = os.getenv("N8N_WEBHOOK_ORDER_URL", "")

def generate_order_number():
    ts = datetime.now().strftime("%y%m%d")
    uid = str(uuid.uuid4()).split("-")[0].upper()
    return f"BD-{ts}-{uid}"


@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(order_in: OrderCreate, db: AsyncSession = Depends(get_db)):
    """Place a new order. Triggers n8n for confirmation email."""
    
    # Find or create customer
    customer = None
    if order_in.customer_id:
        # Logged-in user: look up directly by ID
        result = await db.execute(select(Customer).where(Customer.id == order_in.customer_id))
        customer = result.scalar_one_or_none()
    elif order_in.customer_email:
        result = await db.execute(select(Customer).where(Customer.email == order_in.customer_email))
        customer = result.scalar_one_or_none()
        if not customer:
            customer = Customer(
                id=str(uuid.uuid4()),
                email=order_in.customer_email,
                first_name=order_in.customer_name.split()[0] if order_in.customer_name else None,
                last_name=" ".join(order_in.customer_name.split()[1:]) if order_in.customer_name and len(order_in.customer_name.split()) > 1 else None,
            )
            db.add(customer)
            await db.flush()

    # Build line_items as JSON-serializable list
    line_items = [item.model_dump() for item in order_in.line_items]

    new_order = Order(
        id=str(uuid.uuid4()),
        order_number=generate_order_number(),
        customer_id=customer.id if customer else None,
        subtotal=order_in.subtotal,
        tax=order_in.tax,
        shipping=order_in.shipping,
        discount=order_in.discount,
        total=order_in.total,
        financial_status="pending",
        fulfillment_status="unfulfilled",
        line_items=line_items,
        shipping_address=order_in.shipping_address,
        billing_address=order_in.billing_address,
        notes=order_in.notes,
        stripe_payment_intent_id=order_in.stripe_payment_intent_id,
    )
    db.add(new_order)

    # Update customer stats
    if customer:
        customer.total_orders = (customer.total_orders or 0) + 1
        customer.total_spent = (customer.total_spent or 0.0) + order_in.total

    # Log inventory changes
    for item in order_in.line_items:
        log = InventoryLog(
            id=str(uuid.uuid4()),
            product_id=item.product_id,
            quantity_change=-item.quantity,
            reason="sale",
            order_id=new_order.id,
        )
        db.add(log)

    await db.commit()
    await db.refresh(new_order)

    # Trigger n8n workflow 01 in background (non-blocking)
    if N8N_ORDER_WEBHOOK:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(N8N_ORDER_WEBHOOK, json={
                    "order": {
                        "id": new_order.id,
                        "order_number": new_order.order_number,
                        "customer_email": order_in.customer_email,
                        "customer_name": order_in.customer_name,
                        "total": new_order.total,
                        "subtotal": new_order.subtotal,
                        "discount": new_order.discount,
                        "shipping_cost": new_order.shipping,
                        "created_at": new_order.created_at.isoformat() if new_order.created_at else None,
                    },
                    "items": line_items,
                })
        except Exception as e:
            print(f"n8n order webhook failed (non-critical): {e}")

    return new_order


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    email: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db)
):
    """List orders — filter by customer email or status."""
    stmt = select(Order).order_by(Order.created_at.desc()).limit(limit)
    if email:
        result_cust = await db.execute(select(Customer).where(Customer.email == email))
        customer = result_cust.scalar_one_or_none()
        if customer:
            stmt = stmt.where(Order.customer_id == customer.id)
        else:
            return []
    if status:
        stmt = stmt.where(Order.financial_status == status)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(order_id: str, update: OrderUpdateStatus, db: AsyncSession = Depends(get_db)):
    """Update order status (financial / fulfillment / tracking)."""
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if update.financial_status:
        order.financial_status = update.financial_status
    if update.fulfillment_status:
        order.fulfillment_status = update.fulfillment_status
        if update.fulfillment_status == "fulfilled":
            order.fulfilled_at = datetime.utcnow()
    if update.tracking_number:
        order.tracking_number = update.tracking_number
    if update.tracking_url:
        order.tracking_url = update.tracking_url
    if update.notes:
        order.notes = update.notes

    await db.commit()
    await db.refresh(order)
    return order
