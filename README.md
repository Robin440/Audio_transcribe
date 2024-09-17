# Generate Transcribe
This project is a FastAPI-based application designed to process audio transcription using either AWS Transcribe or OpenAI's transcription services. Users can submit an audio file and choose between AWS or OpenAI as the transcription provider. The application outputs both a fully transcribed text and a structured conversation format, which includes speaker labels, conversation text, and timestamps for each speaker. The transcription tasks are handled asynchronously using Celery with Redis as a message broker, ensuring efficient background processing for large or time-consuming jobs.

## Step 1: Clone this repo to your local machine.
To clone the repo , navigate to your desired project directory in your terminal or command prompt and run the following command:
    ```git clone <repo>```

##  Step 2: Install virtual environment.
To install virtual environment , you can use pip, which is Python's package manager. You can install it by. 
    ```
        pip install virtualenv
    ```
And  then create a virtual environment by.
    ```
        virtualenv <env_name>
    ```
Replace <env_name> with the name of your virtual environment.

Activate  the virtual environment by.
    For macOS /Linux:
    ```
        source <env_name>/bin/activate
    ```
For windows.
    ```
        <env_name>\Scripts\activate
    ```
You should see the name of your virtual environment printed in your command line.

##   Step 3: Install required packages.
To install the packages which are used for this project by running.
    ```
        pip install -r requirements.txt
    ```
This will install all the packages listed in the requirements.txt file.

##  Step 4: Configure AWS Transcribe and OpenAI.
You need to configure AWS Transcribe and OpenAI in the config.py file.
For AWS Transcribe, you need to set the ```AWS_ACCESS_KEY_ID```, ```AWS_SECRET_ACCESS_KEY```, and ```AWS_REGION_NAME``` variables.
For OpenAI, you need to set the ```OPENAI_API_KEY``` variable.
You can find these values in your AWS and OpenAI dashboards.
Make sure to replace the placeholders with your actual values.
for better practice use ```.env```

##   Step 5: Run the application.
To run the application, navigate to the project directory in your terminal or command prompt
    For production.
    ```bash
        fastapi run
    ```
    For development.
    ```
        uvicorn app.main:app --reload
    ```
    or 
    ```
        fastapi dev
    ```

This will start the application and you can access it by visiting http://localhost:8000
    in your web browser.**
    **You can use the API endpoints to interact with the application.**

## Step  6: Test the application.

To test the endpoints , you can use a tool like Postman ,cURL or swagger
    You can find the API documentation in the /docs endpoint of the application http://localhost:8000/docs.
    You can use the API endpoints to test the functionality of the application.


## Contribution.

Feel  free to contribute to this project by submitting pull requests or issues.

## License.
This project is licensed under the MIT License.

