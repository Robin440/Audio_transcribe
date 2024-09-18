from fastapi import APIRouter, HTTPException, Path,Body
from fastapi.responses import StreamingResponse
import boto3
import os
from dotenv import load_dotenv
from app.routers.utils.download_audio import download_audio_from_s3
from app.routers.utils.transcribe_audio import transcribe_audio_with_openai
from app.response.responses import HTTP_200, HTTP_400, HTTP_404, HTTP_401, HTTP_500
from app.routers.utils.transcribe_audio_aws import transcribe_audio_with_aws
from app.tasks.task import process_transcription


# Load environment variables from .env file
load_dotenv()

router = APIRouter()


@router.post("/generate_transcribe/{file_key}/{identifier}/")
def generate_transcribe_with_AI_service(
    file_key: str = Path(
        ..., description="The key of the file to be downloaded from S3"
    ),
    identifier: str = Path(
        ..., description="The identifier for the file, e.g., aws/openai"
    ),
   callback_url: str = Body(..., description="The URL where the result should be sent")
):
    """
    # Generate Transcribe
    ## Description:
    * This endpoint is used to download a file from S3 bucket and generate  a transcription.
    ## Request and Response:
    * Request: Handle a POST method to ownload a file from S3 bucket and transcribe the auido to text.
    * Response: Return a StreamingResponse object with the downloaded file.
    ## Parameters:
    ### - Path Parameters:
    * file_key: The key of the file in the S3 bucket.
    ### - Body Parameters:
    * NA.

    """

    if not callback_url:
        raise HTTPException(status_code=HTTP_400, detail="Callback URL is required")

    # Checking file key is present in path params
    if not file_key:
        return HTTP_404(details={"file_key": "File key is missing."})

    # Checking  identifier is present in path params
    if not identifier:
        return HTTP_404(details={"identifier": "Identifier is missing."})

    # Checking if identifier is valid
    identifier_list = ["aws", "openai"]
    if identifier not in identifier_list:
        return HTTP_404(
            details={
                "identifier": "Invalid identifier,identifiers must be 'openai' or 'aws'."
            }
        )

    # Enqueue the task to Celery
    task = process_transcription.delay(file_key, identifier,callback_url)

    # Succes response
    return HTTP_200(
        data={"task_id": task.id, "status": "Task has been submitted for processing."}
    )
