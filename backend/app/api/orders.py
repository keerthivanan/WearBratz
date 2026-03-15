from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
import random
import string
import httpx
import os
from app.core.database import get_db
from app.models.models import Order, OrderItem, OrderStatusHistory, Customer, PromoCode
from app.schemas.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/api/orders", tags=["orders"])


def generate_order_number() -> str:
    chars = string.ascii_uppercase + string.digits
    suffix = "".join(random.choices(chars, k=6))
    return f"BD-{suffix}"


@router.get("", response_model=List[OrderOut])
async def get_orders(
    email: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Order)
    if email:
        query = query.where(Order.customer_email == email)
    if status:
        query = query.where(Order.status == status)

    query = query.order_by(Order.created_at.desc())
    result = await db.execute(query)
    orders = result.scalars().all()

    for order in orders:
        items_result = await db.execute(
            select(OrderItem).where(OrderItem.order_id == order.id)
        )
        order.items = items_result.scalars().all()

    return orders


@router.get("/{order_id}", response_model=OrderOut)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        # Try by order_number
        result = await db.execute(select(Order).where(Order.order_number == order_id))
        order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items_result = await db.execute(
        select(OrderItem).where(OrderItem.order_id == order.id)
    )
    order.items = items_result.scalars().all()
    return order


@router.post("", response_model=OrderOut, status_code=201)
async def create_order(data: OrderCreate, db: AsyncSession = Depends(get_db)):
    # Calculate pricing
    subtotal = sum(item.price * item.quantity for item in data.items)
    discount = 0.0
    shipping_cost = 9.99 if subtotal < 150 else 0.0

    # Apply promo code
    if data.promo_code:
        promo_result = await db.execute(
            select(PromoCode).where(
                PromoCode.code == data.promo_code.upper(),
                PromoCode.is_active == True,
            )
        )
        promo = promo_result.scalar_one_or_none()
        if promo and subtotal >= float(promo.min_order):
            if promo.max_uses is None or promo.used_count < promo.max_uses:
                if promo.discount_type == "percentage":
                    discount = subtotal * (float(promo.discount_value) / 100)
                else:
                    discount = float(promo.discount_value)
                promo.used_count += 1

    total = subtotal - discount + shipping_cost

    # Upsert customer
    cust_result = await db.execute(
        select(Customer).where(Customer.email == data.customer_email)
    )
    customer = cust_result.scalar_one_or_none()
    if not customer:
        customer = Customer(
            email=data.customer_email,
            first_name=data.customer_name.split()[0] if data.customer_name else None,
            last_name=" ".join(data.customer_name.split()[1:]) if data.customer_name and len(data.customer_name.split()) > 1 else None,
        )
        db.add(customer)
        await db.flush()

    # Generate unique order number
    for _ in range(5):
        order_number = generate_order_number()
        existing = await db.execute(select(Order).where(Order.order_number == order_number))
        if not existing.scalar_one_or_none():
            break

    order = Order(
        order_number=order_number,
        customer_id=customer.id,
        customer_email=data.customer_email,
        customer_name=data.customer_name,
        status="confirmed",
        subtotal=subtotal,
        discount=discount,
        shipping_cost=shipping_cost,
        total=total,
        promo_code=data.promo_code,
        shipping_address=data.shipping_address.model_dump(),
        notes=data.notes,
    )
    db.add(order)
    await db.flush()

    # Add order items
    order_items = []
    for item in data.items:
        oi = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product_name,
            size=item.size,
            price=item.price,
            quantity=item.quantity,
            subtotal=item.price * item.quantity,
        )
        db.add(oi)
        order_items.append(oi)

    # Status history
    history = OrderStatusHistory(
        order_id=order.id,
        old_status=None,
        new_status="confirmed",
        note="Order placed successfully",
    )
    db.add(history)

    # Update customer stats
    customer.total_orders += 1
    customer.total_spent = float(customer.total_spent) + total

    await db.commit()
    await db.refresh(order)
    order.items = order_items

    # Trigger n8n webhook (non-blocking)
    n8n_url = os.getenv("N8N_WEBHOOK_ORDER_URL")
    if n8n_url:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                await client.post(n8n_url, json={
                    "order_number": order.order_number,
                    "customer_email": order.customer_email,
                    "customer_name": order.customer_name,
                    "total": float(order.total),
                    "items": [{"name": i.product_name, "qty": i.quantity, "price": float(i.price)} for i in order_items],
                    "shipping_address": order.shipping_address,
                })
        except Exception:
            pass  # Don't fail the order if n8n is down

    return order
