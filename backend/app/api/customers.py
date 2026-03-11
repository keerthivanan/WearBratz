from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from typing import List, Optional

from app.core.database import get_db
from app.models import Customer
from app.models.schemas import CustomerCreate, CustomerUpdate, CustomerResponse

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerResponse, status_code=201)
async def create_or_update_customer(customer_in: CustomerCreate, db: AsyncSession = Depends(get_db)):
    """Create a new customer or return existing one by email."""
    result = await db.execute(select(Customer).where(Customer.email == customer_in.email))
    existing = result.scalar_one_or_none()

    if existing:
        # Update fields if provided
        if customer_in.first_name:
            existing.first_name = customer_in.first_name
        if customer_in.last_name:
            existing.last_name = customer_in.last_name
        if customer_in.phone:
            existing.phone = customer_in.phone
        existing.email_marketing_consent = customer_in.email_marketing_consent
        await db.commit()
        await db.refresh(existing)
        return existing

    new_customer = Customer(
        id=str(uuid.uuid4()),
        email=customer_in.email,
        first_name=customer_in.first_name,
        last_name=customer_in.last_name,
        phone=customer_in.phone,
        email_marketing_consent=customer_in.email_marketing_consent,
    )
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer


@router.get("/", response_model=List[CustomerResponse])
async def list_customers(
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Customer).order_by(Customer.created_at.desc()).limit(limit))
    return result.scalars().all()


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.get("/by-email/{email}", response_model=CustomerResponse)
async def get_customer_by_email(email: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.email == email))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", response_model=CustomerResponse)
async def update_customer(customer_id: str, update: CustomerUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    for field, value in update.model_dump(exclude_none=True).items():
        setattr(customer, field, value)

    await db.commit()
    await db.refresh(customer)
    return customer
