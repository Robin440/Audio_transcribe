from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any

# Global response structure function with optional details
def global_response(
    status_code: int, 
    message: str, 
    data: Optional[Dict[str, Any]] = None, 
    details: Optional[Dict[str, Any]] = None
):
    response = {
        "status": status_code,
        "message": message,
        "data": data
    }
    if details:
        response["details"] = details
    return response

# Custom response for HTTP 200
def HTTP_200(data=None, message="Success", details=None):
    return JSONResponse(
        content=global_response(200, message, data, details),
        status_code=200
    )

# Custom response for HTTP 400
def HTTP_400(message="Bad Request", data=None, details=None):
    return JSONResponse(
        content=global_response(400, message, data, details),
        status_code=400
    )

# Custom response for HTTP 401
def HTTP_401(message="Unauthorized", data=None, details=None):
    return JSONResponse(
        content=global_response(401, message, data, details),
        status_code=401
    )

# Custom response for HTTP 404
def HTTP_404(message="Not Found", data=None, details=None):
    return JSONResponse(
        content=global_response(404, message, data, details),
        status_code=404
    )

# Custom response for HTTP 500
def HTTP_500(message="Internal Server Error", data=None, details=None):
    return JSONResponse(
        content=global_response(500, message, data, details),
        status_code=500
    )

# Add other status codes as needed...




"""
Example Usage with Details

In your FastAPI routes, you can now pass additional details to provide more context:

from fastapi import FastAPI
from .response import HTTP_200, HTTP_400, HTTP_500

app = FastAPI()

@app.get("/example")
async def example():
    data = {"key": "value"}
    return HTTP_200(data=data)

@app.get("/bad-request")
async def bad_request():
    details = {"error": "Invalid parameters", "expected_format": "JSON"}
    return HTTP_400(message="This is a bad request example", details=details)

@app.get("/server-error")
async def server_error():
    details = {"exception": "Database connection failed"}
    return HTTP_500(message="Something went wrong", details=details)


"""
