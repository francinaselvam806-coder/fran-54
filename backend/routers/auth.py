from fastapi import APIRouter, HTTPException, status
from ..models import User
from ..database import get_database
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class LoginRequest(BaseModel):
    email: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    db = await get_database()
    
    # Check if user already exists
    existing_user = await db["users"].find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password
    user_dict = user.dict()
    user_dict["password"] = get_password_hash(user.password)
    
    # Insert user
    new_user = await db["users"].insert_one(user_dict)
    
    # Create valid return object
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    created_user["_id"] = str(created_user["_id"]) # Serialize ObjectId
    
    return created_user

@router.post("/login")
async def login(login_request: LoginRequest):
    db = await get_database()
    user = await db["users"].find_one({"email": login_request.email})
    
    if not user or not verify_password(login_request.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # For MVP, returning simple success. In prod, return JWT.
    return {
        "message": "Login successful", 
        "user_id": str(user["_id"]), 
        "username": user["username"], 
        "email": user["email"],
        "is_provider": user.get("is_provider", False),
        "address": user.get("address"),
        "phone": user.get("phone"),
        "profile_image": user.get("profile_image"),
        "is_admin": user.get("is_admin", False)
    }
