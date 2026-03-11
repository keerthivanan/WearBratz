from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Any, Dict
from datetime import datetime

# ================================================================
# PRODUCTS
# ================================================================
class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    compare_at_price: Optional[float] = None
    category: Optional[str] = None
    tags: Optional[Any] = None
    images: Optional[Any] = None
    inventory_quantity: int = 0
    inventory_policy: str = "deny"
    status: str = "draft"
    seo_title: Optional[str] = None
    seo_description: Optional[str] = None
    handle: Optional[str] = None
    cost: Optional[float] = None
    created_by: Optional[str] = "manual"

class ProductCreate(ProductBase):
    sku: str

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    inventory_quantity: Optional[int] = None
    status: Optional[str] = None
    category: Optional[str] = None

class ProductResponse(ProductBase):
    id: str
    sku: str
    view_count: int = 0
    wishlist_count: int = 0
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RecommendationRequest(BaseModel):
    currentProductId: str
    dollType: Optional[str] = None
    category: Optional[str] = None
    priceRange: Optional[List[float]] = None


# ================================================================
# CUSTOMERS
# ================================================================
class CustomerCreate(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email_marketing_consent: bool = False

class CustomerUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    default_address: Optional[Dict] = None
    email_marketing_consent: Optional[bool] = None

class CustomerResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    total_orders: int = 0
    total_spent: float = 0.0
    email_marketing_consent: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


# ================================================================
# ORDERS
# ================================================================
class OrderLineItem(BaseModel):
    product_id: str
    product_name: str
    size: Optional[str] = None
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_email: str
    customer_name: Optional[str] = None
    line_items: List[OrderLineItem]
    subtotal: float
    tax: float = 0.0
    shipping: float = 0.0
    discount: float = 0.0
    total: float
    shipping_address: Optional[Dict] = None
    billing_address: Optional[Dict] = None
    notes: Optional[str] = None
    promo_code: Optional[str] = None
    stripe_payment_intent_id: Optional[str] = None

class OrderResponse(BaseModel):
    id: str
    order_number: str
    customer_id: Optional[str] = None
    customer_email: Optional[str] = None
    subtotal: float
    tax: float
    shipping: float
    discount: float
    total: float
    financial_status: str
    fulfillment_status: str
    line_items: Any
    shipping_address: Optional[Any] = None
    tracking_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderUpdateStatus(BaseModel):
    financial_status: Optional[str] = None
    fulfillment_status: Optional[str] = None
    tracking_number: Optional[str] = None
    tracking_url: Optional[str] = None
    notes: Optional[str] = None


# ================================================================
# CART (persistent carts — NOT abandoned carts)
# ================================================================
class CartItem(BaseModel):
    product_id: str
    product_name: str
    price: float
    quantity: int
    size: Optional[str] = None
    image_url: Optional[str] = None

class CartUpsert(BaseModel):
    session_id: str
    items: List[CartItem]
    customer_id: Optional[str] = None

class CartResponse(BaseModel):
    id: str
    session_id: str
    customer_id: Optional[str] = None
    items: Any
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ================================================================
# WISHLIST
# ================================================================
class WishlistToggle(BaseModel):
    session_id: str
    product_id: str
    customer_id: Optional[str] = None

class WishlistResponse(BaseModel):
    id: str
    session_id: str
    product_id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ================================================================
# PROMO CODES
# ================================================================
class PromoCodeValidate(BaseModel):
    code: str
    order_subtotal: float

class PromoCodeResponse(BaseModel):
    valid: bool
    code: Optional[str] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    discount_amount: Optional[float] = None
    message: str


# ================================================================
# EMAIL SUBSCRIBERS
# ================================================================
class SubscriberCreate(BaseModel):
    email: str
    source: str = "footer"


# ================================================================
# CUSTOM QUOTES
# ================================================================
class CustomQuoteBase(BaseModel):
    customer_email: str
    customer_name: Optional[str] = None
    doll_type: Optional[str] = None
    outfit_description: str
    reference_images: Optional[Any] = None
    special_requests: Optional[str] = None
    budget: Optional[str] = None
    deadline: Optional[str] = None

class CustomQuoteCreate(CustomQuoteBase):
    pass

class CustomQuoteResponse(CustomQuoteBase):
    id: str
    quote_number: str
    status: str
    quoted_price: Optional[float] = None
    quoted_delivery_days: Optional[int] = None
    pdf_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ================================================================
# STORE FEATURES (waitlist, reviews, abandoned carts)
# ================================================================
class WaitlistCreate(BaseModel):
    product_id: str
    customer_email: str

class AbandonedCartCreate(BaseModel):
    session_id: str
    customer_email: Optional[str] = None
    items: List[Any]
    subtotal: float

class ProductReviewCreate(BaseModel):
    product_id: str
    order_id: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[List[Any]] = []

class ProductReviewResponse(BaseModel):
    id: str
    product_id: str
    rating: int
    title: Optional[str] = None
    content: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ================================================================
# INVENTORY
# ================================================================
class InventoryUpdateRequest(BaseModel):
    quantity_change: int
    reason: str  # 'restock', 'adjustment', 'return'
    notes: Optional[str] = None
