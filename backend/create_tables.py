"""
Run this script once to create all DB tables and seed initial products.
Usage: cd backend && python create_tables.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.models import Base, Product, ProductInventory, PromoCode
import uuid


SEED_PRODUCTS = [
    {
        "name": "Y2K Plaid Mini",
        "price": 59.99,
        "category": "Skirts",
        "emoji": "🩷",
        "tag": "BESTSELLER",
        "sizes": ["XS", "S", "M", "L"],
        "stock": 40,
        "rating": 4.8,
        "review_count": 124,
        "description": "Channel early-2000s energy in this iconic plaid mini skirt. Cut with a flirty A-line silhouette and finished with a zip-back closure.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCQ9t8j4B8u5Hk5JEXyHBiTFUg5itOexzoXhASYzXtoZg5lukjZy9Hl5WbeNxlINcei0SoWNO2UVCPmt36OgvnY3v7rt30cjqdCQKZRIL0AxxgQKbKCfnj6wsEqBi6IQ7gyLoqzHzPK5c99QRdvaliljNqj6o7ezLcDFbOagpzqGlxr-G1-mifqpo8imrgfokp4rTQOCNNHtRMMXlOO1d4_EHtbYvSuIQqLPVMXHQ1ucxdF8yVXIKv-QsFvCxgAzuFy2gCcoN299sA",
    },
    {
        "name": "Chrome Crop Jacket",
        "price": 129.99,
        "category": "Jackets",
        "emoji": "🤍",
        "tag": "NEW DROP",
        "sizes": ["XS", "S", "M", "L", "XL"],
        "stock": 30,
        "rating": 4.7,
        "review_count": 89,
        "description": "Make a statement with this futuristic chrome crop jacket. The metallic finish catches the light beautifully.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCRM6QkKa9wEbdOwAIs3bFj1t-THtSHkXAkKdlOo_cId0mypVs6sy8pcZQJUyveSxNJx0UktYmvTViBkvxUjnNGxf-7kiBmu1Eb4zxXMIhf_8hLjdOSsvrv-qaw3FiuAXGGQEJTEywQicFCWaNfzOicUZfKX1p3oHGwZ0gP7ZPiUVLTv4F2hxVNms82DAYmS_piSsQ5shTcuwyme9axrujFjtiMZE463bxnsRGX-NUktSg4FdFaem8kQG-88hNHdfsnzSOa5MuTaCY",
    },
    {
        "name": "Velvet Bodycon Dress",
        "price": 79.99,
        "category": "Dresses",
        "emoji": "💜",
        "tag": "TRENDING",
        "sizes": ["XS", "S", "M", "L"],
        "stock": 25,
        "rating": 4.9,
        "review_count": 203,
        "description": "Luxuriously soft velvet hugs every curve in this show-stopping bodycon dress.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBnMv1i97FHjTzv673kwGsn04ldSslL0rwRMGSo6BfblQ29tAaZcVrrzKmuYuar1qDVy3INLkVBBG5yA_Ourmq6AMzEfSomZFjCHMnObmedLpVkeOOWyv07jldxz-08L4ID-9fX8RDMYqGBHp0F5RC4UoPyNGETMxBb5xQKnR1hOEmOYLshuLHvAOujOtQPxx6P2Hp9YDK1dLVwCMZJfC6ECS8Ylg3zHx1XLWY0ydzsastUD2tMuvpeZDWZAMJEVVUkDYv_Jvo",
    },
    {
        "name": "Bubble Hem Mini Skirt",
        "price": 49.99,
        "original_price": 69.99,
        "category": "Skirts",
        "emoji": "🩵",
        "tag": "SALE",
        "sizes": ["XS", "S", "M"],
        "stock": 20,
        "rating": 4.5,
        "review_count": 67,
        "description": "The bubble hem trend is having a major moment and this mini skirt delivers it perfectly.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDq6_-D5ND5F6sP-gzUY5P6p25PhoquO-4Wc-U7eBqlidYRsLtSqTSV3vFMT0niCi1OKDe30La4islhw_WZrUWWisJSENdHflT-aDoBxlThCKX9Gbv_d3wn6c9_sR-5KnHg7iHHN04JxcBfEwt1RhlQXOcykZyluGZbvnunc0EKb19WHbZxTwJMl9m1S2SCi0Ki-r9JFoeNRGt3TCEsl0t1eEw_lT9-aCbGYGUrUxwwYA_MxrTiUz5zHTG8IWp9k9mDl9rk_e5t1ys",
    },
    {
        "name": "Rhinestone Corset Top",
        "price": 64.99,
        "category": "Tops",
        "emoji": "✨",
        "tag": "LIMITED",
        "sizes": ["XS", "S", "M", "L"],
        "stock": 15,
        "rating": 4.9,
        "review_count": 156,
        "description": "Encrusted with hand-placed rhinestones, this corset top is pure glamour.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCQ9t8j4B8u5Hk5JEXyHBiTFUg5itOexzoXhASYzXtoZg5lukjZy9Hl5WbeNxlINcei0SoWNO2UVCPmt36OgvnY3v7rt30cjqdCQKZRIL0AxxgQKbKCfnj6wsEqBi6IQ7gyLoqzHzPK5c99QRdvaliljNqj6o7ezLcDFbOagpzqGlxr-G1-mifqpo8imrgfokp4rTQOCNNHtRMMXlOO1d4_EHtbYvSuIQqLPVMXHQ1ucxdF8yVXIKv-QsFvCxgAzuFy2gCcoN299sA",
    },
    {
        "name": "Faux Fur Trim Jacket",
        "price": 149.99,
        "category": "Jackets",
        "emoji": "🖤",
        "tag": "NEW DROP",
        "sizes": ["S", "M", "L", "XL"],
        "stock": 20,
        "rating": 4.6,
        "review_count": 91,
        "description": "Cozy meets chic with this faux fur trimmed jacket.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuCRM6QkKa9wEbdOwAIs3bFj1t-THtSHkXAkKdlOo_cId0mypVs6sy8pcZQJUyveSxNJx0UktYmvTViBkvxUjnNGxf-7kiBmu1Eb4zxXMIhf_8hLjdOSsvrv-qaw3FiuAXGGQEJTEywQicFCWaNfzOicUZfKX1p3oHGwZ0gP7ZPiUVLTv4F2hxVNms82DAYmS_piSsQ5shTcuwyme9axrujFjtiMZE463bxnsRGX-NUktSg4FdFaem8kQG-88hNHdfsnzSOa5MuTaCY",
    },
    {
        "name": "Satin Slip Midi Dress",
        "price": 89.99,
        "category": "Dresses",
        "emoji": "🌸",
        "tag": "BESTSELLER",
        "sizes": ["XS", "S", "M", "L"],
        "stock": 30,
        "rating": 4.8,
        "review_count": 178,
        "description": "Effortless and elegant, this satin slip midi dress drapes beautifully.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuBnMv1i97FHjTzv673kwGsn04ldSslL0rwRMGSo6BfblQ29tAaZcVrrzKmuYuar1qDVy3INLkVBBG5yA_Ourmq6AMzEfSomZFjCHMnObmedLpVkeOOWyv07jldxz-08L4ID-9fX8RDMYqGBHp0F5RC4UoPyNGETMxBb5xQKnR1hOEmOYLshuLHvAOujOtQPxx6P2Hp9YDK1dLVwCMZJfC6ECS8Ylg3zHx1XLWY0ydzsastUD2tMuvpeZDWZAMJEVVUkDYv_Jvo",
    },
    {
        "name": "Knit Mesh Crop Top",
        "price": 44.99,
        "category": "Tops",
        "emoji": "💗",
        "tag": "TRENDING",
        "sizes": ["XS", "S", "M"],
        "stock": 35,
        "rating": 4.7,
        "review_count": 112,
        "description": "This mesh knit crop top brings texture and edge to any outfit.",
        "image_url": "https://lh3.googleusercontent.com/aida-public/AB6AXuDq6_-D5ND5F6sP-gzUY5P6p25PhoquO-4Wc-U7eBqlidYRsLtSqTSV3vFMT0niCi1OKDe30La4islhw_WZrUWWisJSENdHflT-aDoBxlThCKX9Gbv_d3wn6c9_sR-5KnHg7iHHN04JxcBfEwt1RhlQXOcykZyluGZbvnunc0EKb19WHbZxTwJMl9m1S2SCi0Ki-r9JFoeNRGt3TCEsl0t1eEw_lT9-aCbGYGUrUxwwYA_MxrTiUz5zHTG8IWp9k9mDl9rk_e5t1ys",
    },
]


async def main():
    print("🔌 Connecting to Neon DB...")
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

    print("📦 Creating all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created!")

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Seed products
        print("🌱 Seeding products...")
        for p_data in SEED_PRODUCTS:
            product_id = str(uuid.uuid4())
            sizes = p_data.pop("sizes")
            stock = p_data.pop("stock")

            product = Product(id=product_id, **p_data)
            session.add(product)

            per_size_stock = stock // len(sizes)
            for size in sizes:
                session.add(ProductInventory(
                    id=str(uuid.uuid4()),
                    product_id=product_id,
                    size=size,
                    stock=per_size_stock,
                ))

        # Seed promo code
        print("🎟️  Seeding promo codes...")
        session.add(PromoCode(
            id=str(uuid.uuid4()),
            code="BRATZ10",
            discount_type="percentage",
            discount_value=10,
            min_order=0,
            max_uses=None,
        ))

        await session.commit()

    print("✅ Database setup complete! 8 products + 1 promo code (BRATZ10) created.")
    print("🚀 Now run: uvicorn main:app --reload")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
