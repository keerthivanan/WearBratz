from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models import CustomQuote
from app.models.schemas import CustomQuoteCreate, CustomQuoteResponse

# Temporarily skipping actual HTTP hit to n8n to avoid hanging if n8n is not up yet
# import httpx

router = APIRouter(prefix="/quotes", tags=["quotes"])

def generate_quote_number():
    return f"QUO-{datetime.now().strftime('%Y%m')}-{str(uuid.uuid4()).split('-')[0].upper()}"

async def trigger_n8n_custom_quote_workflow(quote_data: dict):
    """
    This function will be run in the background to send the quote data to n8n.
    For now, it's just a mock since n8n isn't fully configured yet.
    """
    # async with httpx.AsyncClient() as client:
    #     await client.post("http://localhost:5678/webhook/custom-quote", json=quote_data)
    print(f"Triggered n8n workflow for Quote {quote_data.get('quote_number')}")


@router.post("/", response_model=CustomQuoteResponse, status_code=201)
async def submit_custom_quote_request(
    quote_in: CustomQuoteCreate, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db)
):
    
    new_quote = CustomQuote(**quote_in.model_dump())
    new_quote.id = str(uuid.uuid4())
    new_quote.quote_number = generate_quote_number()
    new_quote.status = "pending"
    
    db.add(new_quote)
    await db.commit()
    await db.refresh(new_quote)
    
    # Trigger the n8n automation in the background
    quote_data_for_n8n = {
        "quote_id": new_quote.id,
        "quote_number": new_quote.quote_number,
        "customer_email": new_quote.customer_email,
        "customer_name": new_quote.customer_name,
        "doll_type": new_quote.doll_type,
        "outfit_description": new_quote.outfit_description
    }
    background_tasks.add_task(trigger_n8n_custom_quote_workflow, quote_data_for_n8n)
    
    return new_quote
