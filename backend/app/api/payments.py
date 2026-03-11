from fastapi import APIRouter, Request, HTTPException
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

router = APIRouter(tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    if not STRIPE_WEBHOOK_SECRET:
        return {"status": "warning", "message": "Stripe webhook secret missing, cannot verify"}

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")
        
    if event.type == 'checkout.session.completed':
        # Hand off to n8n logic here later
        print("Checkout session completed:", event.data.object.id)
    
    elif event.type == 'payment_intent.succeeded':
        print("Payment intent succeeded:", event.data.object.id)
        
    return {"status": "success"}
