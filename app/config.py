from dotenv import load_dotenv
import os
import boto3
from pathlib import Path
# Load environment variables from .env file
env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

# Intialize openai key
OPENAI_KEY=os.getenv("OPENAI_KEY")

# Get AWS credentials and region from environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AUDIO_FILES_BUCKET=os.getenv("AUDIO_FILES_BUCKET")
TEXT_FILES_BUCKET=os.getenv("TEXT_FILES_BUCKET")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


# Intialize transcribe client
transcribe_client = boto3.client(
    'transcribe',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-west-1",
)



# Intialize message broker

CELERY_BROKER_URL=os.getenv('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND=os.getenv('CELERY_RESULT_BACKEND')

