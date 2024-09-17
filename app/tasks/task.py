from celery import shared_task
from app.routers.utils.transcribe_audio_aws import transcribe_audio_with_aws
from app.routers.utils.transcribe_audio import transcribe_audio_with_openai
from app.routers.utils.download_audio import download_audio_from_s3

@shared_task
def process_transcription(file_key: str, identifier: str):
    """
    Processes the transcription of an audio file using a specified transcription service.

    This function handles audio transcription based on the provided `identifier`. If the `identifier` is 'openai',

    it will download the audio file from an AWS S3 bucket and perform transcription using OpenAI. If the `identifier` is 'aws',

    it will directly transcribe the audio using AWS Transcribe service.

    Args:
        file_key (str): The filename of the audio file.
        identifier (str): The transcription service to use. It can be either 'aws' or 'openai'.

    Raises:
        ValueError: If the `identifier` is not recognized or if there's an issue with transcription.

    Returns:
        dict: A dictionary containing the transcription result and any relevant metadata.
    """

    if identifier == "openai":
        # Calling the function to process  the transcription using OpenAI
        file_path = download_audio_from_s3(file_key)
        return transcribe_audio_with_openai(file_path)

    elif identifier == "aws":
        # calling the  function to process the transcription using AWS Transcribe
        return transcribe_audio_with_aws(file_key)
        
    else:
        raise ValueError("Invalid identifier")
