import os
import math
from pydub import AudioSegment
import openai
from app.config import OPENAI_KEY
from app.response.responses import HTTP_200, HTTP_400, HTTP_401, HTTP_404, HTTP_500
import json
from app.routers.utils.detete_file import delete_file

# Set your OpenAI API key

openai.api_key = OPENAI_KEY


# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    print("//////////////////////////////////////")
    try:
        with open(file_path, "rb") as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1", file=audio_file, response_format="srt"
            )
            return response if isinstance(response, str) else response.get("text")
    except Exception as e:
        raise ValueError(f"An error occurred during transcription: {e}")

# Function to identify speakers and format conversation
def identify_speakers(transcribed_text):
    if not transcribed_text:
        return None

    # Define the system message for formatting
    system_message = {
        "role": "system",
        "content": (
            "You are an assistant that can identify speakers in a conversation. "
            "Your task is to format a transcribed conversation into JSON format, "
            "with each line of dialogue labeled with the speaker and timestamp."
        ),
    }

    # Define the user message with the transcribed text input
    user_message = {
        "role": "user",
        "content": (
            "The following is a transcription of a conversation between multiple speakers. "
            "Identify each speaker and format the text as a dialogue with speaker labels and timestamps."
            f"Transcribed Text : {transcribed_text}."
            "'speaker', 'conversation', 'start_time','end_time'."
            "do not add json key name in out"
        ),
    }

    try:
        response = openai.chat.completions.create(
            model="gpt-4-turbo",
            messages=[system_message, user_message],
            max_tokens=3000,
            temperature=0.5,
            # response_format={ "type": "json_object" }
        )
        formatted_conversation = response.choices[0].message.content.strip()
        return formatted_conversation
    except Exception as e:
        return HTTP_400(
            details={
                "identify_speakers"
                f"An error occurred during speaker identification: {e}"
            }
        )


def remove_newline_literals(text):
    """
    This function removes the literal string "\n" (backslash + n) from the given text
    and replaces it with a space.

    Args:
        text (str): The input text from which the "\n" literal should be removed.

    Returns:
        str: The modified text with "\n" replaced.
    """
    # Replace the literal "\n" (backslash + n) with a space
    cleaned_text = text.replace("\n", "")

    return cleaned_text


import re


def remove_timestamps(text):
    # Regular expression to match the timestamp format
    pattern = r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}"

    # Use re.sub to replace the matched timestamps with an empty string
    clean_text = re.sub(pattern, "", text)

    # Optional: Remove any extra newlines or spaces left behind
    clean_text = re.sub(r"\n+", "\n", clean_text).strip()

    return clean_text


# Function to split audio if larger than 20 MB
def split_audio_if_large(file_path, chunk_size_mb=20):
    file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MB
    if file_size <= chunk_size_mb:
        return [file_path]  # No need to split

    # Load audio with pydub
    audio = AudioSegment.from_file(file_path)
    duration_ms = len(audio)  # Get the duration in milliseconds

    # Calculate how many chunks are needed based on the file size
    total_chunks = math.ceil(file_size / chunk_size_mb)
    chunk_duration_ms = duration_ms / total_chunks  # Duration per chunk

    # Split the audio into smaller chunks
    audio_chunks = []
    for i in range(total_chunks):
        start_time = i * chunk_duration_ms
        end_time = (i + 1) * chunk_duration_ms
        chunk = audio[start_time:end_time]
        chunk_path = f"chunk_{i + 1}.mp3"
        chunk.export(chunk_path, format="mp3")
        audio_chunks.append(chunk_path)

    return audio_chunks


def transcribe_audio_with_openai(file_path):
    """

    This is main function of audio transcription with  OpenAI.
    
    In this function we are  using the following steps:

    1. Spliting the audio if the file size is above than 20 mb.(Openai Whisper model only supports 26 mb)

    2. Transcribe the audio files into  text using the OpenAI Whisper model.

    3.  Cleaning the text by removing the newline  characters and extra spaces.

    4 . Creating chat converstion by OpenAI chat complelation model.

    5. Removing time stamps from  the text .

    6 . Converting chat converation json string to json format.

    7 . Deleting downloaded audio  files.

    Args:
        file_path (_type_): name of the audio file.

    Returns:
        _type_: _description_
    """
    print(f"open ai key ======== {openai.api_key}")
    audio_file_path = file_path

    # Split the audio if needed
    audio_chunks = split_audio_if_large(audio_file_path, chunk_size_mb=20)

    full_transcription = ""

    # Transcribe each chunk
    for chunk_path in audio_chunks:
        transcribed_text = transcribe_audio(chunk_path)
        if transcribed_text:
            full_transcription += transcribed_text
        else:
            return HTTP_400(
                details={
                    "non_binary_error": f"Failed to transcribe chunk: {chunk_path}"
                }
            )

    # Identify speakers and format conversation
    if full_transcription:
        # removing unwanted  characters
        full_transcription = remove_newline_literals(full_transcription)
        # converting text to conversation
        formatted_conversation = identify_speakers(full_transcription)
        # removing time stamps
        full_transcription = remove_timestamps(full_transcription)
        # converting json string to json format
        formatted_conversation = json.loads(formatted_conversation)
        if formatted_conversation:
            # delete audio file
            delete_status = delete_file(audio_file_path)
            data = {
                "transcribed_text": full_transcription,
                "chat": formatted_conversation,
                "delete_status":delete_status
            }
            print(f"open ai data ========= {data}")
            return data
        else:
            delete_status = delete_file(audio_file_path)
            return HTTP_400(
                details={"non_binary_error": "Failed to identify speakers.","delete_status":delete_status}
            )
    else:
        delete_status = delete_file(audio_file_path)
        return HTTP_400(details={"non_binary_error": "No transcription available.","delete_status":delete_status})
