# VoiceNoteAssistantGPT

VoiceNoteAssistantGPT is a web application that transcribes audio recordings and generates AI-generated responses using the OpenAI GPT-3.5 Turbo model. It allows users to upload audio files in the M4A format and receive transcriptions along with AI-generated responses.

## Installation

1. Clone the repository:

```
$ git clone <repository_url>
```

2. Install the required dependencies:

```shell
$ pip install -r requirements.txt
```

3. Set up environment variables:

-   Create a .env file in the root directory of the project.
-   Add the following environment variables to the .env file:

```plaintext
OPENAI_API_KEY=<your_openai_api_key>
PUSHOVER_USER_KEY=<your_pushover_user_key>
PUSHOVER_API_TOKEN=<your_pushover_api_token>
USERNAME=<your_username>
PASSWORD=<your_password>
```

## Usage

1. Start the application:

    ```shell
    $ uvicorn main:app --reload
    ```

    or if you want to make it accessible in a local network:

    ```shell
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

    The application will be accessible at `http://localhost:8000`.

2. Open your web browser and navigate to `http://localhost:8000` to access the application.
3. Authenticate using your username and password (set that up in .env file).
4. Upload an M4A audio file using the provided form. (iPhone shortcut coming soon)
5. The application will transcribe the audio file in the background and generate an AI-generated response using the OpenAI GPT-3.5 Turbo model.
6. Once the transcription and response generation are completed, you will be able to see the transcriptions and AI-generated responses on the main page.

## Logging

The application logs events and errors to a log file named app.log. The log file is located in the same directory as the application.

## Credits

VoiceNoteAssistantGPT is built using the following libraries and APIs:

OpenAI GPT-3.5 Turbo: Provides the AI-generated response generation capabilities.  
FastAPI: A modern, fast (high-performance) web framework for building APIs with Python.  
Whisper: A library for speech recognition using the Whisper ASR system.
dotenv: Loads environment variables from a .env file.  
Pushover: A service for sending push notifications to various devices and platforms.

## License

This project is licensed under the MIT License.
