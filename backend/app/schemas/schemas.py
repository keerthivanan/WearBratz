from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List, Any
from datetime import datetime
from decimal import Decimal


# ─────────────────────────────────────────
# PRODUCT SCHEMAS
# ─────────────────────────────────────────

class ProductInventoryOut(BaseModel):
    size: str
    stock: int

    model_config = {"from_attributes": True}


class ProductOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: str
    emoji: Optional[str] = None
    gradient: Optional[str] = None
    tag: Optional[str] = None
    stock: int
    sizes: List[str]
    rating: Optional[float] = None
    review_count: int
    is_active: bool
    created_at: datetime
    inventory: List[ProductInventoryOut] = []

    model_config = {"from_attributes": True}


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    original_price: Optional[float] = None
    category: str
    emoji: Optional[str] = None
    gradient: Optional[str] = None
    tag: Optional[str] = None
    stock: int = 0
    sizes: List[str] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    category: Optional[str] = None
    emoji: Optional[str] = None
    gradient: Optional[str] = None
    tag: Optional[str] = None
    stock: Optional[int] = None
    sizes: Optional[List[str]] = None
    is_active: Optional[bool] = None


# ─────────────────────────────────────────
# CUSTOMER SCHEMAS
# ─────────────────────────────────────────

class CustomerCreate(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str = "US"
    is_subscribed: bool = False


class CustomerOut(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str
    is_subscribed: bool
    total_orders: int
    total_spent: float
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
# ORDER SCHEMAS
# ─────────────────────────────────────────

class OrderItemCreate(BaseModel):
    product_id: Optional[str] = None
    product_name: str
    size: Optional[str] = None
    price: float
    quantity: int = 1


class OrderItemOut(BaseModel):
    id: str
    product_id: Optional[str] = None
    product_name: str
    size: Optional[str] = None
    price: float
    quantity: int
    subtotal: float

    model_config = {"from_attributes": True}


class ShippingAddress(BaseModel):
    full_name: str
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    country: str = "US"
    phone: Optional[str] = None


class OrderCreate(BaseModel):
    customer_email: EmailStr
    customer_name: Optional[str] = None
    items: List[OrderItemCreate]
    shipping_address: ShippingAddress
    promo_code: Optional[str] = None
    notes: Optional[str] = None


class OrderOut(BaseModel):
    id: str
    order_number: str
    customer_email: str
    customer_name: Optional[str] = None
    status: str
    subtotal: float
    discount: float
    shipping_cost: float
    total: float
    promo_code: Optional[str] = None
    shipping_address: Optional[dict] = None
    tracking_number: Optional[str] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    created_at: datetime
    items: List[OrderItemOut] = []

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
# CART SCHEMAS
# ─────────────────────────────────────────

class CartItemIn(BaseModel):
    product_id: str
    product_name: str
    price: float
    quantity: int = 1
    size: Optional[str] = None
    emoji: Optional[str] = None
    image: Optional[str] = None


class CartSave(BaseModel):
    session_id: str
    items: List[CartItemIn]
    customer_id: Optional[str] = None


class CartOut(BaseModel):
    id: str
    session_id: str
    items: List[Any]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
# WISHLIST SCHEMAS
# ─────────────────────────────────────────

class WishlistToggle(BaseModel):
    session_id: str
    product_id: str
    customer_id: Optional[str] = None


class WishlistItemOut(BaseModel):
    id: str
    product_id: str
    product: Optional[ProductOut] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─────────────────────────────────────────
# PROMO CODE SCHEMAS
# ─────────────────────────────────────────

class PromoCodeCheck(BaseModel):
    code: str
    order_total: float


class PromoCodeResult(BaseModel):
    valid: bool
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    message: str


# ─────────────────────────────────────────
# SUBSCRIBE SCHEMA
# ─────────────────────────────────────────

class SubscribeRequest(BaseModel):
    email: EmailStr
    source: str = "footer"


class SubscribeResponse(BaseModel):
    success: bool
    message: str


# ─────────────────────────────────────────
# WEBHOOK SCHEMA
# ─────────────────────────────────────────

class WebhookPayload(BaseModel):
    event: str
    data: dict


# ─────────────────────────────────────────
# GENERIC RESPONSE
# ─────────────────────────────────────────

class MessageResponse(BaseModel):
    message: str
    success: bool = True
