from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from ..database import get_database
from ..models import User, Service
from bson import ObjectId

router = APIRouter(prefix="/admin", tags=["Admin"])

# Authentication Dependency (Mock for MVP, check is_admin flag strictly)
# In production, check JWT token claims
async def get_admin_user(user_email: str):
    db = await get_database()
    user = await db["users"].find_one({"email": user_email})
    if not user or not user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@router.get("/stats")
async def get_stats():
    db = await get_database()
    total_users = await db["users"].count_documents({})
    total_services = await db["services"].count_documents({})
    # Assuming we might have a verified flag logic later, for now just count all
    
    return {
        "total_users": total_users,
        "total_services": total_services,
        "active_reports": 0 # Placeholder
    }

@router.get("/users")
async def get_users():
    db = await get_database()
    users = await db["users"].find().to_list(100)
    # Serialize ObjectId
    for user in users:
        user["_id"] = str(user["_id"])
        user["password"] = "***" # Hide password
    return users

@router.put("/users/{user_id}/verify")
async def verify_user(user_id: str):
    db = await get_database()
    result = await db["users"].update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"is_provider": True}} # For now, verifying means ensuring they are a provider? Or maybe we add a 'verified' badge field later.
                                        # Let's assume 'certificate' logic handled in creation, 
                                        # maybe this just toggles a status.
                                        # For this MVP, let's say it makes them a provider if not already.
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User verified"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    db = await get_database()
    result = await db["users"].delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@router.delete("/services/{service_id}")
async def delete_service(service_id: str):
    db = await get_database()
    result = await db["services"].delete_one({"_id": ObjectId(service_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Service not found")
    return {"message": "Service deleted"}
