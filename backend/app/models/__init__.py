from sqlalchemy import Column, String, Integer, Float, Boolean, JSON, DateTime, ForeignKey, Table, Index, text, Computed
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY, TSVECTOR
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

# ================================================================
# CUSTOMERS & AUTH
# ====================
class Customer(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    
    auth_provider_id = Column(String) # 'email' or 'google:ID'
    password_hash = Column(String) # For email/password auth
    
    email_marketing_consent = Column(Boolean, default=False)
    sms_marketing_consent = Column(Boolean, default=False)
    
    default_address = Column(JSONB)
    addresses = Column(JSONB) # Multiple addresses
    
    total_orders = Column(Integer, default=0)
    total_spent = Column(Float, default=0.0)
    average_order_value = Column(Float, default=0.0)
    last_order_date = Column(DateTime(timezone=True))
    
    tags = Column(JSONB) # Array of strings
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_seen_at = Column(DateTime(timezone=True))

    orders = relationship("Order", back_populates="customer")
    quotes = relationship("CustomQuote", back_populates="customer")
    reviews = relationship("ProductReview", back_populates="customer")

    __table_args__ = (
        Index('idx_customers_total_spent', text('total_spent DESC')),
    )


# ================================================================
# PRODUCTS & INVENTORY
# ====================
class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Product(Base):
    __tablename__ = "products"

    id = Column(String, primary_key=True, default=generate_uuid)
    sku = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    compare_at_price = Column(Float)
    cost = Column(Float)
    
    inventory_quantity = Column(Integer, default=0)
    inventory_policy = Column(String, default='deny') # 'deny' or 'continue'
    status = Column(String, default='draft', index=True) # 'draft', 'active', 'archived'
    category = Column(String, index=True) # Soft link or ID
    
    tags = Column(JSONB) # Array of tags
    images = Column(JSONB) # [{url, alt, position}]
    metadata_extra = Column("metadata", JSONB) # Custom fields
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    published_at = Column(DateTime(timezone=True))
    created_by = Column(String) # 'manual' or 'ai'
    
    seo_title = Column(String)
    seo_description = Column(String)
    handle = Column(String, unique=True, index=True) # URL slug
    
    view_count = Column(Integer, default=0)
    wishlist_count = Column(Integer, default=0)

    search_vector = Column(TSVECTOR, Computed("to_tsvector('english', title || ' ' || description)", persisted=True))

    __table_args__ = (
        Index('idx_products_search', 'search_vector', postgresql_using='gin'),
    )


class InventoryLog(Base):
    __tablename__ = "inventory_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    quantity_change = Column(Integer, nullable=False)
    reason = Column(String, nullable=False)
    order_id = Column(String, nullable=True) # nullable soft link
    notes = Column(String)
    created_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ================================================================
# SALES & ORDERS
# ====================
class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=generate_uuid)
    order_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), index=True)
    
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, default=0.0)
    shipping = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)
    total = Column(Float, nullable=False)
    
    financial_status = Column(String, default='pending') # pending, paid, refunded
    fulfillment_status = Column(String, default='unfulfilled') # unfulfilled, fulfilled, partial
    
    line_items = Column(JSONB, nullable=False) # [{product_id, title, quantity, price}]
    
    shipping_address = Column(JSONB)
    billing_address = Column(JSONB)
    tracking_number = Column(String)
    tracking_url = Column(String)
    
    stripe_payment_intent_id = Column(String)
    
    notes = Column(String)
    tags = Column(JSONB)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    fulfilled_at = Column(DateTime(timezone=True))
    cancelled_at = Column(DateTime(timezone=True))

    customer = relationship("Customer", back_populates="orders")
    quotes = relationship("CustomQuote", back_populates="order")
    status_history = relationship("OrderStatusHistory", back_populates="order")

    __table_args__ = (
        Index('idx_orders_status', 'financial_status', 'fulfillment_status'),
        Index('idx_orders_created', text('created_at DESC')),
    )

class OrderStatusHistory(Base):
    __tablename__ = "order_status_history"
    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False, index=True)
    status = Column(String, nullable=False)
    notes = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    order = relationship("Order", back_populates="status_history")


# ================================================================
# STORE FEATURES (Cart, Wishlist, Reviews, Promo)
# ================================================================
class Cart(Base):
    __tablename__ = "carts"
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    items = Column(JSONB, default='[]') # [{product_id, quantity, size}]
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, index=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class PromoCode(Base):
    __tablename__ = "promo_codes"
    id = Column(String, primary_key=True, default=generate_uuid)
    code = Column(String, unique=True, index=True, nullable=False)
    discount_type = Column(String, nullable=False) # 'percentage' or 'fixed'
    discount_value = Column(Float, nullable=False)
    min_order = Column(Float, default=0.0)
    max_uses = Column(Integer)
    used_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class EmailSubscriber(Base):
    __tablename__ = "email_subscribers"
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    source = Column(String, default='footer') # 'footer', 'popup', 'checkout'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProductReview(Base):
    __tablename__ = "product_reviews"
    id = Column(String, primary_key=True, default=generate_uuid)
    product_id = Column(String, ForeignKey("products.id"), index=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    order_id = Column(String) # Soft link
    rating = Column(Integer, nullable=False)
    title = Column(String)
    content = Column(String)
    status = Column(String, default='pending', index=True) # pending, approved, hidden
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="reviews")

class ProductWaitlist(Base):
    __tablename__ = "product_waitlist"
    id = Column(String, primary_key=True, default=generate_uuid)
    product_id = Column(String, ForeignKey("products.id"), nullable=False, index=True)
    customer_email = Column(String, nullable=False, index=True)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True)
    notified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AbandonedCart(Base):
    __tablename__ = "abandoned_carts"
    id = Column(String, primary_key=True, default=generate_uuid)
    session_id = Column(String, nullable=False)
    customer_email = Column(String, index=True)
    items = Column(JSONB, nullable=False)
    subtotal = Column(Float, nullable=False)
    recovered = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


# ================================================================
# SPECIALS & PAYMENTS
# ====================
class CustomQuote(Base):
    __tablename__ = "custom_quotes"
    id = Column(String, primary_key=True, default=generate_uuid)
    quote_number = Column(String, unique=True, index=True, nullable=False)
    customer_id = Column(String, ForeignKey("customers.id"), nullable=True, index=True)
    customer_email = Column(String, nullable=False)
    doll_type = Column(String)
    outfit_description = Column(String, nullable=False)
    status = Column(String, default='pending', index=True) # pending, quoted, accepted, rejected
    quoted_price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    order_id = Column(String, ForeignKey("orders.id"), nullable=True)
    customer = relationship("Customer", back_populates="quotes")
    order = relationship("Order", back_populates="quotes")

class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    id = Column(String, primary_key=True, default=generate_uuid)
    order_id = Column(String, index=True)
    stripe_id = Column(String, unique=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default='USD')
    status = Column(String) # succeeded, failed, pending
    created_at = Column(DateTime(timezone=True), server_default=func.now())
