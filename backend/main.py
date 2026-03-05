from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .routers import auth, services, ai, admin
from fastapi import Request
from fastapi.responses import JSONResponse
import logging

app = FastAPI(title="Hyperlocal Gig Finder")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal Server Error: {str(exc)}"},
    )

# CORS setup

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    from .database import get_database
    db_status = "unknown"
    try:
        await get_database()
        db_status = "connected"
    except Exception as e:
        db_status = f"failed: {str(e)}"
    
    return {
        "status": "healthy", 
        "database": db_status,
        "environment": os.getenv("RENDER", "local")
    }

app.include_router(auth.router)
app.include_router(services.router)
app.include_router(ai.router)
app.include_router(admin.router)

# Serve static files from the frontend directory - must be at the end to not override API routes
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
