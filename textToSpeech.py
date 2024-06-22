import os
import io
import random

from google.cloud import texttospeech
from pydub import AudioSegment
from pydub.playback import play

# Set Google application credentials for Text-to-Speech API access
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "third-shade-425412-m6-a8400f8dd8be.json"


class TextToSpeech:
    """
    A class to convert text to speech with varying audio styles (whisper, regular, loud) using Google's Text-to-Speech API.

    Attributes:
        client (TextToSpeechClient): A client for interacting with Google's Text-to-Speech API.
        speech_style (str): An identifier for the speech style ('W' for whisper, 'R' for regular, 'L' for loud).
        text (str): The text content to be converted to speech.
        voice_params (dict): Configuration parameters for different voice styles including voice type, volume, rate, and pitch.

    Methods:
        get_audio(): Generates an audio file from text based on the specified style (whisper, regular, loud).
    """

    def __init__(self, speech_style, text):
        """
        Initializes the TextToSpeech instance with the provided speech style and text.

        Parameters:
            speech_style (str): An identifier for the desired speech style ('W', 'R', 'L').
            text (str): The text to be converted to speech.
        """
        self.client = texttospeech.TextToSpeechClient()
        self.speech_style = speech_style.upper()  # Ensure it is uppercase for consistency
        self.text = text
        self.voice_params = {
            "W": {"voice_name": "en-US-Wavenet-B",
                  "volume": "x-soft",
                  "rate": 0.8,
                  "pitch": -3,
                  "volume_gain_db": -5},  # Whisper
            "R": {
                "voice_name": "en-US-Wavenet-D",
                "volume": "medium",
                "rate": 1.0,
                "pitch": 0.0,
                "volume_gain_db": 0},  # Regular
            "L": {
                "voice_name": "en-US-Wavenet-B",
                "volume": 4,
                "rate": 1.5,
                "pitch": 3,
                "volume_gain_db": 10
            }
        }

    def get_audio(self):
        """
        Generates and plays an audio file from the text, using the style specified by 'can_string'.

        Returns:
            str: The filename of the saved audio file.
        """
        # Retrieve voice settings from the parameters or default to regular if undefined
        voice_settings = self.voice_params.get(self.speech_style, self.voice_params["R"])

        # Setup the synthesis input and voice parameters
        synthesis_input = texttospeech.SynthesisInput(text=self.text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US" if self.speech_style in ["L", "R"] else "en-UK",
            name=voice_settings['voice_name'],
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16,  # Set to WAV format
            pitch=voice_settings['pitch'],
            speaking_rate=voice_settings['rate'],
            volume_gain_db = voice_settings['volume_gain_db']
        )

        # Request speech synthesis
        response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Load and play the audio in memory
        audio_stream = io.BytesIO(response.audio_content)
        audio = AudioSegment.from_file(audio_stream, format="wav")

        # Adjust volume based on the style
        if self.speech_style == "L":
            audio += 15  # Increase volume by 15dB
        elif self.speech_style == "W":
            audio -= 25  # Decrease volume by 25dB

        play(audio)
        random_number = random.randint(1000, 9999)
        # Save the audio to a file
        filename = f"audioResponse/output_{self.speech_style}_{random_number}.wav"
        with open(filename, 'wb') as out:
            out.write(response.audio_content)
        print(f'Audio content written to file "{filename}"')
        return filename
