from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.products import router as products_router
from app.api.orders import router as orders_router
from app.api.cart import router as cart_router
from app.api.wishlist import router as wishlist_router
from app.api.customers import router as customers_router
from app.api.subscribe import router as subscribe_router
from app.api.promos import router as promos_router
from app.api.webhook import router as webhook_router
from app.api.quotes import router as quotes_router
from app.api.auth import router as auth_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Luxury E-Commerce Backend — WearBratz / Bratz Drip",
    version=settings.API_VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products_router)
app.include_router(orders_router)
app.include_router(cart_router)
app.include_router(wishlist_router)
app.include_router(customers_router)
app.include_router(subscribe_router)
app.include_router(promos_router)
app.include_router(webhook_router)
app.include_router(quotes_router)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
