from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, text
from typing import List, Optional
import uuid

from app.core.database import get_db
from app.models import Product, InventoryLog
from app.models.schemas import ProductCreate, ProductUpdate, ProductResponse, RecommendationRequest, InventoryUpdateRequest

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
async def list_products(
    category: Optional[str] = Query(None),
    status: Optional[str] = Query("active"),
    search: Optional[str] = Query(None),
    sort: Optional[str] = Query("created_at"),  # price_asc, price_desc, name, created_at
    limit: int = Query(50, le=200),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db)
):
    """List products with optional filtering, search and sorting."""
    stmt = select(Product)

    if status:
        stmt = stmt.where(Product.status == status)
    if category:
        stmt = stmt.where(Product.category == category)
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(or_(
            Product.title.ilike(search_term),
            Product.description.ilike(search_term),
            Product.category.ilike(search_term),
        ))

    # Sorting
    if sort == "price_asc":
        stmt = stmt.order_by(Product.price.asc())
    elif sort == "price_desc":
        stmt = stmt.order_by(Product.price.desc())
    elif sort == "name":
        stmt = stmt.order_by(Product.title.asc())
    elif sort == "popular":
        stmt = stmt.order_by(Product.wishlist_count.desc())
    else:
        stmt = stmt.order_by(Product.created_at.desc())

    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all unique product categories."""
    result = await db.execute(
        text("SELECT DISTINCT category, COUNT(*) as count FROM products WHERE status = 'active' GROUP BY category ORDER BY count DESC")
    )
    return [{"category": row[0], "count": row[1]} for row in result if row[0]]


@router.get("/handle/{handle}", response_model=ProductResponse)
async def get_product_by_handle(handle: str, db: AsyncSession = Depends(get_db)):
    """Get product by URL handle. Also increments view count."""
    result = await db.execute(select(Product).where(Product.handle == handle))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    # Increment view count
    product.view_count = (product.view_count or 0) + 1
    await db.commit()
    await db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/recommendations", response_model=List[ProductResponse])
async def get_recommendations(req: RecommendationRequest, db: AsyncSession = Depends(get_db)):
    """Get product recommendations based on category."""
    stmt = select(Product).where(
        Product.id != req.currentProductId,
        Product.status == "active"
    )
    if req.category:
        stmt = stmt.where(Product.category == req.category)
    stmt = stmt.order_by(Product.wishlist_count.desc()).limit(4)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product_in: ProductCreate, db: AsyncSession = Depends(get_db)):
    """Create product — designed to be hit by n8n AI Product Creation workflow."""
    new_product = Product(**product_in.model_dump())
    new_product.id = str(uuid.uuid4())
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


@router.patch("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, update: ProductUpdate, db: AsyncSession = Depends(get_db)):
    """Update product fields."""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for field, value in update.model_dump(exclude_none=True).items():
        setattr(product, field, value)
    await db.commit()
    await db.refresh(product)
    return product


@router.post("/{product_id}/inventory")
async def update_inventory(product_id: str, update: InventoryUpdateRequest, db: AsyncSession = Depends(get_db)):
    """Update product inventory — restock, adjustment, return."""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.inventory_quantity = max(0, (product.inventory_quantity or 0) + update.quantity_change)

    # Log the change
    log = InventoryLog(
        id=str(uuid.uuid4()),
        product_id=product_id,
        quantity_change=update.quantity_change,
        reason=update.reason,
        notes=update.notes,
        created_by="manual",
    )
    db.add(log)
    await db.commit()
    await db.refresh(product)
    return {"product_id": product_id, "new_quantity": product.inventory_quantity, "change": update.quantity_change}
