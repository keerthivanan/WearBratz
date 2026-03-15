import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    String, Text, Numeric, Integer, Boolean, DateTime,
    ForeignKey, UniqueConstraint, CheckConstraint, Index,
    ARRAY
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    original_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    emoji: Mapped[Optional[str]] = mapped_column(String(10))
    image_url: Mapped[Optional[str]] = mapped_column(String(512))
    gradient: Mapped[Optional[str]] = mapped_column(String(255))
    tag: Mapped[Optional[str]] = mapped_column(String(50))
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    sizes: Mapped[List[str]] = mapped_column(ARRAY(String), nullable=False, default=list)
    rating: Mapped[Optional[float]] = mapped_column(Numeric(3, 2), default=0)
    review_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    inventory: Mapped[List["ProductInventory"]] = relationship("ProductInventory", back_populates="product", cascade="all, delete-orphan")
    reviews: Mapped[List["ProductReview"]] = relationship("ProductReview", back_populates="product", cascade="all, delete-orphan")
    wishlist_items: Mapped[List["Wishlist"]] = relationship("Wishlist", back_populates="product", cascade="all, delete-orphan")


class ProductInventory(Base):
    __tablename__ = "product_inventory"
    __table_args__ = (UniqueConstraint("product_id", "size"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    product_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    size: Mapped[str] = mapped_column(String(20), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    product: Mapped["Product"] = relationship("Product", back_populates="inventory")


class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(100))
    last_name: Mapped[Optional[str]] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    address_line1: Mapped[Optional[str]] = mapped_column(String(255))
    address_line2: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    zip_code: Mapped[Optional[str]] = mapped_column(String(20))
    country: Mapped[str] = mapped_column(String(100), default="US")
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=False)
    total_orders: Mapped[int] = mapped_column(Integer, default=0)
    total_spent: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    orders: Mapped[List["Order"]] = relationship("Order", back_populates="customer")
    carts: Mapped[List["Cart"]] = relationship("Cart", back_populates="customer")
    wishlist_items: Mapped[List["Wishlist"]] = relationship("Wishlist", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    order_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    customer_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id"))
    customer_email: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_name: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    discount: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    shipping_cost: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    promo_code: Mapped[Optional[str]] = mapped_column(String(50))
    shipping_address: Mapped[Optional[dict]] = mapped_column(JSONB)
    notes: Mapped[Optional[str]] = mapped_column(Text)
    tracking_number: Mapped[Optional[str]] = mapped_column(String(100))
    shipped_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    delivered_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    status_history: Mapped[List["OrderStatusHistory"]] = relationship("OrderStatusHistory", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    order_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("products.id"))
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    size: Mapped[Optional[str]] = mapped_column(String(20))
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    order: Mapped["Order"] = relationship("Order", back_populates="items")


class Cart(Base):
    __tablename__ = "carts"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    session_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    customer_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id"))
    items: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="carts")


class Wishlist(Base):
    __tablename__ = "wishlists"
    __table_args__ = (UniqueConstraint("session_id", "product_id"),)

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    session_id: Mapped[str] = mapped_column(String(255), nullable=False)
    customer_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("customers.id"))
    product_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    customer: Mapped[Optional["Customer"]] = relationship("Customer", back_populates="wishlist_items")
    product: Mapped["Product"] = relationship("Product", back_populates="wishlist_items")


class PromoCode(Base):
    __tablename__ = "promo_codes"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    discount_type: Mapped[str] = mapped_column(String(20), nullable=False, default="percentage")
    discount_value: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    min_order: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    max_uses: Mapped[Optional[int]] = mapped_column(Integer)
    used_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class EmailSubscriber(Base):
    __tablename__ = "email_subscribers"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String(100), default="footer")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    order_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    old_status: Mapped[Optional[str]] = mapped_column(String(50))
    new_status: Mapped[str] = mapped_column(String(50), nullable=False)
    note: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    order: Mapped["Order"] = relationship("Order", back_populates="status_history")


class ProductReview(Base):
    __tablename__ = "product_reviews"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    product_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    order_id: Mapped[Optional[str]] = mapped_column(UUID(as_uuid=False), ForeignKey("orders.id"))
    customer_email: Mapped[Optional[str]] = mapped_column(String(255))
    customer_name: Mapped[Optional[str]] = mapped_column(String(100))
    rating: Mapped[int] = mapped_column(Integer, CheckConstraint("rating BETWEEN 1 AND 5"), nullable=False)
    review_text: Mapped[Optional[str]] = mapped_column(Text)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    product: Mapped["Product"] = relationship("Product", back_populates="reviews")


class QuoteRequest(Base):
    __tablename__ = "quote_requests"

    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(30))
    product_name: Mapped[str] = mapped_column(String(255), nullable=False)
    requirements: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, contacted, quoted, paid
    quoted_price: Mapped[Optional[float]] = mapped_column(Numeric(10, 2))
    stripe_link: Mapped[Optional[str]] = mapped_column(String(512))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)
