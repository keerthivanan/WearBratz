from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.core.database import get_db
from app.models.models import Cart
from app.schemas.schemas import CartSave, CartOut, MessageResponse

router = APIRouter(prefix="/api/cart", tags=["cart"])


@router.get("/{session_id}", response_model=CartOut)
async def get_cart(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).where(Cart.session_id == session_id))
    cart = result.scalar_one_or_none()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart


@router.post("", response_model=CartOut)
async def save_cart(data: CartSave, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Cart).where(Cart.session_id == data.session_id))
    cart = result.scalar_one_or_none()

    items_list = [item.model_dump() for item in data.items]

    if cart:
        cart.items = items_list
        if data.customer_id:
            cart.customer_id = data.customer_id
    else:
        cart = Cart(
            session_id=data.session_id,
            customer_id=data.customer_id,
            items=items_list,
        )
        db.add(cart)

    await db.commit()
    await db.refresh(cart)
    return cart


@router.delete("/{session_id}", response_model=MessageResponse)
async def clear_cart(session_id: str, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Cart).where(Cart.session_id == session_id))
    await db.commit()
    return {"message": "Cart cleared", "success": True}
