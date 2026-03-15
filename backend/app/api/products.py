from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import Optional, List
from app.core.database import get_db
from app.models.models import Product, ProductInventory
from app.schemas.schemas import ProductOut, ProductCreate, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=List[ProductOut])
async def get_products(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    in_stock: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    query = select(Product).where(Product.is_active == True)

    if category and category.lower() != "all":
        query = query.where(Product.category == category)
    if search:
        query = query.where(Product.name.ilike(f"%{search}%"))
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if in_stock:
        query = query.where(Product.stock > 0)

    result = await db.execute(query)
    products = result.scalars().all()

    # Load inventory for each product
    out = []
    for p in products:
        inv_result = await db.execute(
            select(ProductInventory).where(ProductInventory.product_id == p.id)
        )
        p.inventory = inv_result.scalars().all()
        out.append(p)

    return out


@router.get("/{product_id}", response_model=ProductOut)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Product).where(Product.id == product_id, Product.is_active == True)
    )
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    inv_result = await db.execute(
        select(ProductInventory).where(ProductInventory.product_id == product_id)
    )
    product.inventory = inv_result.scalars().all()
    return product


@router.post("", response_model=ProductOut, status_code=201)
async def create_product(data: ProductCreate, db: AsyncSession = Depends(get_db)):
    product = Product(**data.model_dump())
    db.add(product)
    await db.flush()

    # Create inventory entries per size
    size_stock = product.stock // max(len(product.sizes), 1)
    for size in product.sizes:
        inv = ProductInventory(product_id=product.id, size=size, stock=size_stock)
        db.add(inv)

    await db.commit()
    await db.refresh(product)

    inv_result = await db.execute(
        select(ProductInventory).where(ProductInventory.product_id == product.id)
    )
    product.inventory = inv_result.scalars().all()
    return product


@router.patch("/{product_id}", response_model=ProductOut)
async def update_product(product_id: str, data: ProductUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in data.model_dump(exclude_none=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)
    return product
