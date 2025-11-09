"""
Main API Gateway for ThriveMentor
This serves as the entry point and routes requests to appropriate microservices
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth_service.main import app as auth_app
from career_service.main import app as career_app
from health_service.main import app as health_app
from finance_service.main import app as finance_app

app = FastAPI(
    title="ThriveMentor API Gateway",
    description="AI-Powered Personal Dashboard - API Gateway",
    version="1.0.0"
)

# CORS middleware for Flutter frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount sub-applications
app.mount("/auth", auth_app)
app.mount("/career", career_app)
app.mount("/health", health_app)
app.mount("/finance", finance_app)

@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to ThriveMentor API",
        "version": "1.0.0",
        "services": {
            "auth": "/auth",
            "career": "/career",
            "health": "/health",
            "finance": "/finance"
        },
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api_gateway"}

# Note: In a production microservices architecture, you would use
# service discovery, API gateway patterns, or reverse proxy (nginx/traefik)
# to route requests. For simplicity, we're using a single FastAPI app.
# You can split these into separate services and use HTTP calls between them.

