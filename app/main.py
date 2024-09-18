from fastapi import FastAPI
from app.routers import generate_transcribe
from app.routers import health_check
from prometheus_client import Counter,generate_latest
from pathlib import Path

# Load environment variables from .env file


app = FastAPI()

@app.get("/")
def read_root():
    """
    #  DOCS INFO (Swagger)
    _method_:  GET
    _summary_:  Root endpoint
    _description_:  This is the root endpoint of the API

    Returns:
        _type_: _description_
    """
    return {"message": "For generate transcribe from audio use /api/generate_transcribe\nor use /docs for more info"}

@app.get("/metrics")
def metrics():
    return generate_latest()


#  Routers
#TODO Routers
app.include_router(generate_transcribe.router, prefix="/api", tags=["generate _transcribe from audio"])
app.include_router(health_check.router, prefix="/api", tags=["health_check"])



