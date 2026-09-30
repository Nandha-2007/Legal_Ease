import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router
from utils.config import BACKEND_HOST, BACKEND_PORT, APP_NAME, APP_SUBTITLE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("legalease.main")

# Initialize FastAPI application
app = FastAPI(
    title=f"{APP_NAME} - {APP_SUBTITLE}",
    description="REST API for automated, AI-powered legal document generation.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Enable CORS for Streamlit frontend and web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": f"Welcome to {APP_NAME} AI Legal Document Generator API",
        "status": "online",
        "docs": "/docs",
        "health": "/health",
    }

# Include API routes
app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {APP_NAME} API server at http://{BACKEND_HOST}:{BACKEND_PORT}")
    uvicorn.run("main:app", host=BACKEND_HOST, port=BACKEND_PORT, reload=True)
