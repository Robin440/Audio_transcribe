from fastapi import FastAPI, HTTPException
import time
import uuid
import boto3
import json
from app.config import transcribe_client, AUDIO_FILES_BUCKET, TEXT_FILES_BUCKET, s3_client

# AWS configuration
audio_files_bucket = AUDIO_FILES_BUCKET
text_file_bucket = TEXT_FILES_BUCKET

# Initialize the AWS Transcribe client
transcribe = transcribe_client


def get_transcription_by_file_name(file_name):
    try:
        response = s3_client.get_object(Bucket=TEXT_FILES_BUCKET, Key=file_name)
        transcription = json.loads(response["Body"].read().decode("utf-8"))
        return transcription
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")


def transcribe_audio_with_aws(filename: str):
    try:
        text_file_name = filename.replace(".mp3", "")
        job_name = f"{text_file_name}_{str(uuid.uuid4())}_job"
        job_uri = f"s3://{audio_files_bucket}/{filename}"

        # Start the transcription job
        try:
            transcribe.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={"MediaFileUri": job_uri},
                LanguageCode="en-US",
                OutputBucketName=text_file_bucket,
                OutputKey=f"{text_file_name}.txt",
                Settings={"ShowSpeakerLabels": True, "MaxSpeakerLabels": 4},
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Wait for transcription job to complete
        while True:
            job_status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            status = job_status["TranscriptionJob"]["TranscriptionJobStatus"]
            if status in ["COMPLETED", "FAILED"]:
                break
            time.sleep(10)  # Wait for 10 seconds before checking again

        if status == "FAILED":
            raise HTTPException(status_code=400, detail="Transcription job failed")

        # Fetch the transcript file URL
        transcript_file_uri = job_status["TranscriptionJob"]["Transcript"][
            "TranscriptFileUri"
        ]

        # Ensure we have a valid URL
        if not transcript_file_uri:
            raise HTTPException(
                status_code=400, detail="Transcript file URI not available"
            )

        # Extract filename from the URL
        output_file = transcript_file_uri.split("/")[-1]

        # Download the transcription file content from S3
        response = get_transcription_by_file_name(output_file)

        # Process the transcription data
        transcription_text = response["results"]["transcripts"][0]["transcript"]

        # Process conversation data with speaker labels
        conversations = []
        current_speaker = None
        current_conversation = []
        start_time = None
        end_time = None

        for item in response["results"]["items"]:
            speaker = item.get("speaker_label", "")
            text = item["alternatives"][0]["content"]
            start_time = item.get("start_time", start_time)
            end_time = item.get("end_time", end_time)

            if current_speaker is None:
                current_speaker = speaker

            if speaker != current_speaker:
                conversations.append(
                    {
                        "speaker": current_speaker,
                        "conversation": " ".join(current_conversation),
                        "start_time": start_time,
                        "end_time": end_time,
                    }
                )
                current_conversation = []
                current_speaker = speaker
                start_time = item.get("start_time")
                end_time = item.get("end_time")
            current_conversation.append(text)

        # Add the last conversation
        if current_speaker:
            conversations.append(
                {
                    "speaker": current_speaker,
                    "conversation": " ".join(current_conversation),
                    "start_time": start_time,
                    "end_time": end_time,
                }
            )
        data =  {
            "transcription_text": transcription_text,
            "conversations": conversations,
        }
        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
