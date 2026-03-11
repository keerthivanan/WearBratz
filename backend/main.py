from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Bratz Beauty Doll Store API",
    description="Full e-commerce backend: Products, Orders, Customers, Quotes, Cart, Wishlist, Promo Codes, n8n Automation",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================================================
# HEALTH CHECK
# ================================================================
@app.get("/health", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Bratz Beauty Store API",
        "version": "2.0.0",
        "endpoints": [
            "GET  /api/v1/products/",
            "POST /api/v1/orders/",
            "POST /api/v1/customers/",
            "GET  /api/v1/cart/{session_id}",
            "POST /api/v1/wishlist/toggle",
            "POST /api/v1/promo/validate",
            "POST /api/v1/subscribe",
            "POST /api/v1/quotes/",
            "POST /webhooks/stripe",
        ]
    }

# ================================================================
# API ROUTERS
# ================================================================
from app.api import products, quotes, store, payments, orders, customers, cart, store_utils, auth

app.include_router(auth.router,        prefix="/api/v1")
app.include_router(products.router,    prefix="/api/v1")
app.include_router(orders.router,      prefix="/api/v1")
app.include_router(customers.router,   prefix="/api/v1")
app.include_router(cart.router,        prefix="/api/v1")
app.include_router(store_utils.router, prefix="/api/v1")
app.include_router(quotes.router,      prefix="/api/v1")
app.include_router(store.router,       prefix="/api/v1")
app.include_router(payments.router,    prefix="/webhooks")
