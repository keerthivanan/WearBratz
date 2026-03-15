from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from app.core.database import get_db
from app.models.models import Customer
from app.schemas.schemas import CustomerCreate, CustomerOut

router = APIRouter(prefix="/api/customers", tags=["customers"])


@router.get("", response_model=List[CustomerOut])
async def get_customers(
    email: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Customer)
    if email:
        query = query.where(Customer.email == email)
    result = await db.execute(query.order_by(Customer.created_at.desc()))
    return result.scalars().all()


@router.get("/{customer_id}", response_model=CustomerOut)
async def get_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("", response_model=CustomerOut)
async def upsert_customer(data: CustomerCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.email == data.email))
    customer = result.scalar_one_or_none()

    if customer:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(customer, field, value)
    else:
        customer = Customer(**data.model_dump())
        db.add(customer)

    await db.commit()
    await db.refresh(customer)
    return customer
