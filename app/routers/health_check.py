from fastapi import APIRouter, HTTPException
import redis
import requests
from celery import Celery
from app.config import CELERY_BROKER_URL

router = APIRouter()
# redis://redis:6379/0

# Initialize Celery and Redis
celery_app = Celery('tasks', broker='redis://redis:6379/0')
redis_client = redis.Redis(host='redis', port=6379, db=0)

@router.get("/health")
def health_check():
    """
    # Health check endpoint

    ## Method : GET

    ## Body params : NA

    ## Path params : NA

    ##  Response : 200 OK

    
    _note_: As of now celery and redis  are being used in this endpoint.if you want check any external and internal api
            , please add to the api. 
    """ 
    status = {"status": "healthy", "details": {}}

    # Check Celery
    try:
        celery_status = celery_app.control.ping(timeout=1)
        status["details"]["celery"] = "Celery workers are available"
        status["status"] = "healthy"
        if not celery_status:
            status["details"]["celery"] = "Celery workers are not responding"
            status["status"] = "unhealthy"
    except Exception as e:
        status["details"]["celery"] = f"Celery check failed: {str(e)}"
        status["status"] = "unhealthy"

    # Check Redis
    try:
        redis_client.ping()
        status["details"]["redis"] = "Redis is available"
        status["status"] = "healthy"
    except redis.ConnectionError:
        status["details"]["redis"] = "Redis is not available"
        status["status"] = "unhealthy"

    # # Check External APIs
    # try:
    #     response = requests.get("http://example.com/api/status")
    #     if response.status_code != 200:
    #         status["details"]["external_api"] = "External API is not available"
    #         status["status"] = "unhealthy"
    # except requests.RequestException:
    #     status["details"]["external_api"] = "External API check failed"
    #     status["status"] = "unhealthy"

    # # Check Internal APIs (example)
    # try:
    #     response = requests.get("http://localhost:8000/internal-api/health")
    #     if response.status_code != 200:
    #         status["details"]["internal_api"] = "Internal API is not available"
    #         status["status"] = "unhealthy"
    # except requests.RequestException:
    #     status["details"]["internal_api"] = "Internal API check failed"
    #     status["status"] = "unhealthy"

    return status
