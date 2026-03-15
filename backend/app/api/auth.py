from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import Customer
from app.core.config import settings
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uuid

router = APIRouter(prefix="/api/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()
ALGORITHM = "HS256"
TOKEN_EXPIRE_DAYS = 30


def create_token(customer_id: str, email: str) -> str:
    expire = datetime.utcnow() + timedelta(days=TOKEN_EXPIRE_DAYS)
    return jwt.encode({"sub": customer_id, "email": email, "exp": expire}, settings.SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class SignupBody(BaseModel):
    full_name: str
    email: str
    password: str


class LoginBody(BaseModel):
    email: str
    password: str


def user_response(customer: Customer, token: str) -> dict:
    return {
        "token": token,
        "user": {
            "id": customer.id,
            "email": customer.email,
            "first_name": customer.first_name or "",
            "last_name": customer.last_name or "",
            "phone": customer.phone or "",
            "total_orders": customer.total_orders,
            "total_spent": float(customer.total_spent),
        },
    }


@router.post("/signup")
async def signup(body: SignupBody, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.email == body.email.lower()))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    parts = body.full_name.strip().split(" ", 1)
    customer = Customer(
        id=str(uuid.uuid4()),
        email=body.email.lower(),
        first_name=parts[0],
        last_name=parts[1] if len(parts) > 1 else "",
        password_hash=pwd_context.hash(body.password),
    )
    db.add(customer)
    await db.commit()
    await db.refresh(customer)

    return user_response(customer, create_token(customer.id, customer.email))


@router.post("/login")
async def login(body: LoginBody, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.email == body.email.lower()))
    customer = result.scalar_one_or_none()

    if not customer or not customer.password_hash or not pwd_context.verify(body.password, customer.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return user_response(customer, create_token(customer.id, customer.email))


@router.get("/me")
async def get_me(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    payload = decode_token(credentials.credentials)
    result = await db.execute(select(Customer).where(Customer.id == payload["sub"]))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="User not found")
    return user_response(customer, credentials.credentials)
