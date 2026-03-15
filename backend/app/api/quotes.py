from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.models import QuoteRequest
from pydantic import BaseModel, EmailStr
from typing import Optional
import httpx
import os

router = APIRouter(prefix="/quotes", tags=["quotes"])

class QuoteCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    product_name: str
    requirements: Optional[str] = None

async def trigger_n8n_quote_workflow(quote_id: str, data: QuoteCreate):
    """
    Triggers the n8n workflow for custom quote processing.
    """
    webhook_url = os.getenv("N8N_WEBHOOK_QUOTE_URL") # Need to ensure this is in .env or configured
    if not webhook_url:
        return
    
    async with httpx.AsyncClient() as client:
        try:
            await client.post(webhook_url, json={
                "quote_id": quote_id,
                **data.dict()
            })
        except Exception as e:
            print(f"Error triggering n8n: {e}")

@router.post("/", status_code=201)
async def create_quote_request(
    quote: QuoteCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    db_quote = QuoteRequest(**quote.dict())
    db.add(db_quote)
    await db.commit()
    await db.refresh(db_quote)
    
    # Trigger n8n automation in the background
    background_tasks.add_task(trigger_n8n_quote_workflow, db_quote.id, quote)
    
    return {"message": "Quote request received successfully", "quote_id": db_quote.id}
