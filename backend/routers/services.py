from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..models import Service
from ..database import get_database

router = APIRouter(prefix="/services", tags=["Services"])

@router.post("/", response_model=Service)
async def create_service(service: Service):
    db = await get_database()
    
    # Enrichment: Get provider's profile data
    provider = await db["users"].find_one({"email": service.provider_email})
    if provider:
        service.provider_phone = provider.get("phone")
        service.provider_image = provider.get("profile_image")

    # Auto-generate Dummy Certificate
    import datetime
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    service.certificate = f"Certified {service.category} Expert - Verified by GigFinder on {date_str} for {service.title}"

    result = await db["services"].insert_one(service.dict())
    created_service = await db["services"].find_one({"_id": result.inserted_id})
    created_service["_id"] = str(created_service["_id"])
    return created_service

@router.get("/search", response_model=List[Service])
async def search_services(
    lat: Optional[float] = Query(None, description="Latitude of the user"),
    lon: Optional[float] = Query(None, description="Longitude of the user"),
    radius: float = Query(5000, description="Search radius in meters"), # Default 5km
    category: Optional[str] = None
):
    db = await get_database()
    
    query = {}
    if category:
        query["category"] = category

    # Try geospatial search if we have valid coordinates
    if lat and lon and (abs(lat) > 0.1 or abs(lon) > 0.1):
        try:
            await db["services"].create_index([("location", "2dsphere")])
            geo_query = {**query}
            geo_query["location"] = {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "$maxDistance": radius
                }
            }
            
            services = []
            async for service in db["services"].find(geo_query):
                service["_id"] = str(service["_id"])
                services.append(service)
            
            if services:
                print(f"DEBUG: Found {len(services)} services via GEO search")
                return services
        except Exception as e:
            print(f"DEBUG: Geo-search failed or no index: {e}")

    # Fallback: Find without location filter (but still with category if provided)
    # This ensures services with location: null (manual addresses) show up
    services = []
    async for service in db["services"].find(query):
        service["_id"] = str(service["_id"])
        services.append(service)
    
    print(f"DEBUG: Found {len(services)} services via FALLBACK search")
    return services

@router.get("/{service_id}", response_model=Service)
async def get_service(service_id: str):
    db = await get_database()
    from bson import ObjectId
    try:
        oid = ObjectId(service_id)
    except Exception:
         raise HTTPException(status_code=400, detail="Invalid service ID format")
         
    service = await db["services"].find_one({"_id": oid})
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    
    service["_id"] = str(service["_id"])
    return service
