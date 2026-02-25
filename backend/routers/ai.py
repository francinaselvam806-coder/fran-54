from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.ai_engine import recommend_services

router = APIRouter(prefix="/ai", tags=["AI"])

class QueryRequest(BaseModel):
    message: str

@router.post("/recommend")
async def get_recommendations(request: QueryRequest):
    """
    Takes a user query and returns semantically relevant services using SBERT.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Query message is required")
    
    try:
        results = await recommend_services(request.message)
        return results
    except Exception as e:
        print(f"❌ AI Recommendation Error: {e}")
        raise HTTPException(status_code=500, detail="Internal AI error")
