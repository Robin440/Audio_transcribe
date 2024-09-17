from app.config import s3_client, AUDIO_FILES_BUCKET
from fastapi import HTTPException
import os

bucket = 'physician-assist-voice-nlp-poc-audiofiles-bucket'
def download_audio_from_s3(file_key):
    """
    This function will  download an audio file from S3 bucket.

    Args:
        file_key (_type_): name of the audio with format

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        # Define the local path where the file will be saved
        local_path = os.path.join("audio", file_key.split("/")[-1])

        # Ensure the 'audio' directory exists
        os.makedirs("audio", exist_ok=True)

        # Download the file from S3
        s3_response = s3_client.get_object(Bucket=AUDIO_FILES_BUCKET, Key=file_key)
        file_stream = s3_response["Body"].read()

        # Save the file to the local directory
        with open(local_path, "wb") as f:
            f.write(file_stream)

        # Return a success message with the local path
        return local_path

    # Error handling for HTTP exceptions
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
