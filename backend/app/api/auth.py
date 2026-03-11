from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid

from app.core.database import get_db
from app.models import Customer
from app.services.auth import (
    hash_password, verify_password, create_access_token,
    decode_access_token, verify_google_token
)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer(auto_error=False)


# ================================================================
# Schemas
# ================================================================
class SignupRequest(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class GoogleAuthRequest(BaseModel):
    id_token: str  # The Google ID token from the frontend

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


# ================================================================
# Helpers
# ================================================================
def _make_user_dict(customer: Customer) -> dict:
    return {
        "id": customer.id,
        "email": customer.email,
        "customer_code": customer.customer_code,
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "total_orders": customer.total_orders or 0,
        "total_spent": customer.total_spent or 0.0,
    }


async def _generate_customer_code(db: AsyncSession) -> str:
    """Generate a unique sequential code like Wearbratz01, Wearbratz02, ..."""
    count_result = await db.execute(select(func.count(Customer.id)))
    count = count_result.scalar() or 0
    return f"Wearbratz{(count + 1):02d}"


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Customer:
    if not credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_access_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    result = await db.execute(select(Customer).where(Customer.id == payload["sub"]))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# ================================================================
# SIGNUP — Email + Password
# ================================================================
@router.post("/signup", response_model=AuthResponse, status_code=201)
async def signup(body: SignupRequest, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(Customer).where(Customer.email == body.email.lower()))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    # Require a minimum password length
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters.")

    customer_code = await _generate_customer_code(db)
    new_user = Customer(
        id=str(uuid.uuid4()),
        email=body.email.lower(),
        customer_code=customer_code,
        first_name=body.first_name,
        last_name=body.last_name,
        auth_provider_id="email",
    )
    # Store hashed password via raw SQL to avoid model column mapping issues
    db.add(new_user)
    await db.flush()  # get the ID
    from sqlalchemy import text as sqla_text
    await db.execute(
        sqla_text("UPDATE customers SET password_hash = :ph WHERE id = :uid"),
        {"ph": hash_password(body.password), "uid": new_user.id}
    )
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token({"sub": new_user.id, "email": new_user.email})
    return AuthResponse(access_token=token, user=_make_user_dict(new_user))


# ================================================================
# LOGIN — Email + Password
# ================================================================
@router.post("/login", response_model=AuthResponse)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.email == body.email.lower()))
    user = result.scalar_one_or_none()

    if not user or user.auth_provider_id != "email":
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    # Fetch password_hash via raw SQL
    from sqlalchemy import text as sqla_text
    pw_result = await db.execute(
        sqla_text("SELECT password_hash FROM customers WHERE id = :uid"),
        {"uid": user.id}
    )
    pw_row = pw_result.first()
    stored_hash = pw_row[0] if pw_row else None

    if not stored_hash or not verify_password(body.password, stored_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = create_access_token({"sub": user.id, "email": user.email})
    return AuthResponse(access_token=token, user=_make_user_dict(user))


# ================================================================
# GOOGLE OAUTH — Verify ID token from frontend
# ================================================================
@router.post("/google", response_model=AuthResponse)
async def google_auth(body: GoogleAuthRequest, db: AsyncSession = Depends(get_db)):
    """
    Frontend sends the Google ID token (from Google Sign-In button).
    We verify it server-side and create/find the user.
    """
    google_info = verify_google_token(body.id_token)
    if not google_info:
        raise HTTPException(status_code=400, detail="Invalid Google token.")

    email = google_info["email"].lower()
    google_id = google_info["google_id"]

    # Check if user already exists by email
    result = await db.execute(select(Customer).where(Customer.email == email))
    user = result.scalar_one_or_none()

    if user:
        # Update Google ID if not set
        if not user.auth_provider_id or user.auth_provider_id == "email":
            user.auth_provider_id = f"google:{google_id}"
        await db.commit()
        await db.refresh(user)
    else:
        # Create new user from Google
        name_parts = google_info.get("name", "").split(" ", 1)
        customer_code = await _generate_customer_code(db)
        user = Customer(
            id=str(uuid.uuid4()),
            email=email,
            customer_code=customer_code,
            first_name=name_parts[0] if name_parts else None,
            last_name=name_parts[1] if len(name_parts) > 1 else None,
            auth_provider_id=f"google:{google_id}",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = create_access_token({"sub": user.id, "email": user.email})
    return AuthResponse(access_token=token, user=_make_user_dict(user))


# ================================================================
# GET ME — Current user profile
# ================================================================
@router.get("/me")
async def get_me(current_user: Customer = Depends(get_current_user)):
    return _make_user_dict(current_user)


# ================================================================
# LOGOUT — Client just discards the token, but we provide this for future blacklisting
# ================================================================
@router.post("/logout")
async def logout():
    return {"status": "ok", "message": "Logged out. Delete your token client-side."}
