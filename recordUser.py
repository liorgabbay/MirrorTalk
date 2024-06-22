import random
import pyaudio
import math
import struct
import wave
import keyboard


class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk_size=1024, silence_threshold=None):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk_size = chunk_size
        self.silence_threshold = silence_threshold
        self.audio_interface = pyaudio.PyAudio()
        self.stream = None

    def rms(self, frame):
        # Calculate Root Mean Square (RMS) of audio frame
        count = len(frame) // 2
        format = "%dh" % count
        shorts = struct.unpack(format, frame)
        sum_squares = sum(s ** 2 for s in shorts)
        return math.sqrt(sum_squares / count)

    def record(self):
        """Record audio until silence is detected based on a dynamic threshold or Ctrl + W is pressed."""
        self.stream = self.audio_interface.open(format=self.format, channels=self.channels,
                                                rate=self.rate, input=True, frames_per_buffer=self.chunk_size)
        print("Recording started... Speak into the microphone. Press Ctrl + Q to stop.")

        frames = []
        num_silent = 0
        silence_limit = int((2 * self.rate) / self.chunk_size)  # 2 seconds of silence
        average_rms = []  # To calculate average RMS for dynamic threshold

        while True:
            data = self.stream.read(self.chunk_size)
            frames.append(data)

            current_rms = self.rms(data)
            average_rms.append(current_rms)

            # Calculate dynamic threshold after collecting some initial values
            if len(average_rms) > 30:
                # Set the silence threshold to be slightly below the average RMS
                self.silence_threshold = sum(average_rms) / len(average_rms) * 0.7

            if self.silence_threshold and current_rms < self.silence_threshold:
                num_silent += 1
            else:
                num_silent = 0

            # Stop if silence lasts long enough
            if num_silent >= silence_limit:
                print("Stopping recording due to silence.")
                break

            # Check for Ctrl + W to stop recording
            if keyboard.is_pressed('ctrl+Q'):  # Check if Ctrl + W is pressed
                print("Stopping recording by Ctrl + Q command.")
                break

        self.stop()
        return b''.join(frames)

    def stop(self):
        """Stop the audio stream and close resources."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio_interface.terminate()

    def save(self, data, filename="output.wav"):
        """Save the recorded audio to a WAV file with a random number in the filename."""
        random_number = random.randint(1000, 9999)
        base_filename, file_extension = filename.rsplit('.', 1)
        new_filename = f"userAudio/{base_filename}_{random_number}.{file_extension}"
        wf = wave.open(new_filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.audio_interface.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(data)
        wf.close()
        print(f"Audio content written to file '{new_filename}'")
        return new_filename

