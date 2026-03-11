import asyncio
import os
import sys

# Add the parent directory to sys.path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import AsyncSessionLocal, engine, Base
from app.models import Product
from sqlalchemy import select

BRATZ_PRODUCTS = [
    {
        "title": "Y2K Plaid Mini",
        "sku": "SKU-PLAID-MINI-001",
        "price": 59.99,
        "category": "Skirts",
        "description": "The iconic Y2K plaid mini skirt your wardrobe is BEGGING for. Pair with platform boots for max bratz energy.",
        "status": "active",
        "inventory_quantity": 50,
        "handle": "y2k-plaid-mini"
    },
    {
        "title": "Chrome Crop Jacket",
        "sku": "SKU-CHROME-JKT-002",
        "price": 129.99,
        "category": "Jackets",
        "description": "Futuristic chrome jacket with iridescent sheen. Because why blend in when you were born to STAND OUT?",
        "status": "active",
        "inventory_quantity": 25,
        "handle": "chrome-crop-jacket"
    },
    {
        "title": "Velvet Bodycon Dress",
        "sku": "SKU-VELVET-DRS-003",
        "price": 79.99,
        "category": "Dresses",
        "description": "Midnight velvet hugs every curve perfectly. From club to brunch — this dress does it ALL.",
        "status": "active",
        "inventory_quantity": 40,
        "handle": "velvet-bodycon-dress"
    },
    {
        "title": "Hot Pink Cargo Pants",
        "sku": "SKU-PINK-CRGO-004",
        "price": 89.99,
        "category": "Pants",
        "description": "Statement cargo pants in signature Bratz hot pink. Six pockets because fashion girls carry LOTS of stuff.",
        "status": "active",
        "inventory_quantity": 30,
        "handle": "hot-pink-cargo-pants"
    },
    {
        "title": "Butterfly Mesh Top",
        "sku": "SKU-BFLY-MESH-005",
        "price": 44.99,
        "category": "Tops",
        "description": "Sheer mesh top with embroidered butterfly details. Layered over a bralette for that perfect bratz look.",
        "status": "active",
        "inventory_quantity": 60,
        "handle": "butterfly-mesh-top"
    },
    {
        "title": "Gold Chain Mini Dress",
        "sku": "SKU-GOLD-DRS-006",
        "price": 109.99,
        "category": "Dresses",
        "description": "24k energy only. This gold chain-detail mini dress is pure luxury meets downtown girl.",
        "status": "active",
        "inventory_quantity": 15,
        "handle": "gold-chain-mini-dress"
    },
    {
        "title": "Faux Fur Bolero",
        "sku": "SKU-FUR-BOLERO-007",
        "price": 74.99,
        "category": "Jackets",
        "description": "Fluffy faux fur bolero in cloud white. The layer your party outfit didn't know it needed.",
        "status": "active",
        "inventory_quantity": 20,
        "handle": "faux-fur-bolero"
    },
    {
        "title": "Rhinestone Corset Top",
        "sku": "SKU-RHINE-CRST-008",
        "price": 64.99,
        "category": "Tops",
        "description": "Hand-applied rhinestone details on a structured satin corset. Every night out deserves to sparkle.",
        "status": "active",
        "inventory_quantity": 35,
        "handle": "rhinestone-corset-top"
    }
]

async def seed():
    print("Seeding database...")
    async with AsyncSessionLocal() as session:
        # Check if products already exist
        result = await session.execute(select(Product))
        # Use scalar_one_or_none if you expect at most one, 
        # but here we just check if the list is empty
        existing_products = result.scalars().all()
        
        if existing_products:
            print(f"Database already contains {len(existing_products)} products. Skipping seed.")
            return

        for p_data in BRATZ_PRODUCTS:
            product = Product(**p_data)
            session.add(product)
        
        await session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
