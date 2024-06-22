import os
from openai import OpenAI

# Ensure the API key is set properly
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

class AssistantResponse:
    """
    A class that provides functionality to interact with OpenAI's API for audio transcription and text-based responses.

    Attributes:
        client (OpenAI): An instance of the OpenAI class, used to make requests to the OpenAI API.

    Methods:
        transcribe_audio(audio_file_path): Transcribes audio to text using OpenAI's Whisper model.
        get_response(message): Generates a response based on the provided text message using OpenAI's GPT model.
    """

    def __init__(self):
        """
        Initializes the AssistantResponse with an OpenAI client.
        """
        self.client = OpenAI()

    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribes the given audio file using OpenAI's Whisper model and returns the transcription text.

        Parameters:
            audio_file_path (str): The path to the audio file to be transcribed.

        Returns:
            str: The transcribed text if successful, an empty string if an error occurs.

        Raises:
            Exception: Outputs an error message if the transcription process fails.
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                # Make a request to the Whisper model for transcription
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                # Return the transcribed text
                return transcription.text
        except Exception as e:
            print(f"An error occurred while transcribing: {e}")
            return ""

    def get_response(self, message: str) -> str:
        """
        Sends a message to OpenAI's GPT model and returns the model's response.

        Parameters:
            message (str): The text message to send to the model.

        Returns:
            str: The model's response text if successful, or an error message if an error occurs.

        Raises:
            Exception: Outputs an error message if there is a failure in fetching the response.
        """
        try:
            # Construct the conversation history with the user's message
            conversation = [{"role": "user", "content": message}]

            # Call the OpenAI API using the new interface
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation,
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Sorry, I couldn't fetch a response."
