from assistenentResponse import AssistantResponse
from audioClassifier import AudioClassifier
from audioPreprocessor import AudioPreprocessor
from recordUser import AudioRecorder
from textToSpeech import TextToSpeech
import keyboard

should_continue = True

# ctrl + w to stop the run.
def on_ctrl_w(event):
    global should_continue
    if event.name == 'w' and keyboard.is_pressed('ctrl'):
        should_continue = False


keyboard.on_press(on_ctrl_w)

def main_loop():
    global should_continue
    # Initialize and train the classifier
    preprocessor = AudioPreprocessor('newData', ['whisperAudio', 'regularAudio', 'loudAudio'])
    data, labels = preprocessor.load_data()
    classifier = AudioClassifier(preprocessor=preprocessor)
    classifier.train(data, labels)
    classifier.evaluate()
    assistant = AssistantResponse()
    while should_continue:
        try:
            recorder = AudioRecorder()
            audio_data = recorder.record()
            record_path = recorder.save(audio_data)
            user_voice = classifier.predict(record_path)
            # print the result of the predication.
            print(user_voice)
            user_text = assistant.transcribe_audio(record_path)
            assistant_response = assistant.get_response(user_text)
            assistant_voice = TextToSpeech(user_voice, assistant_response)
            assistant_voice.get_audio()
        except Exception as e:
            print(f"An error occurred: {e}")
            break
    print("finish talking")


# Run the main loop
main_loop()
