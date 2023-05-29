import os
import speech_recognition as sr
from google.cloud import translate_v2, speech_v2, texttospeech_v1
import sounddevice as sd
import numpy as np
import audioop
from scipy.io import wavfile
import tempfile


def main():
    
    r = sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something.. ")

        audio = r.listen(source)

        try:

            text = r.recognize_google(audio, language = "en-GB")

        except Exception as e:
            print("Error: " + str(e))

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"google_key.json"

    translate_client = translate_v2.Client()
    speech_client = texttospeech_v1.TextToSpeechClient()

    target = input("Specify the code for the target language: ")

    output = translate_client.translate(text, target_language=target)

    text = output['translatedText']

    synthesis_input = texttospeech_v1.SynthesisInput(text = text)

    voice1 = texttospeech_v1.VoiceSelectionParams(
        language_code = target,
        ssml_gender = texttospeech_v1.SsmlVoiceGender.FEMALE
    )


    print(speech_client.list_voices)
    audio_config = texttospeech_v1.AudioConfig(
        audio_encoding = texttospeech_v1.AudioEncoding.MP3
    )

    response1 = speech_client.synthesize_speech(
        input = synthesis_input,
        voice = voice1,
        audio_config = audio_config
    )

    with open('audio.mp3', 'wb',) as output:
        output.write(response1.audio_content)

    
    
if __name__ == "__main__":
    main()

# r = sr.Recognizer()

# with sr.Microphone() as source:

#     r.adjust_for_ambient_noise(source)

#     print("Please say something.. ")

#     audio = r.listen(source)

# request = speech_v2.types.cloud_speech.CreateRecognizerRequest(
#     parent=f"projects/top-amplifier-386514/locations/global",
#     recognizer_id="translatorproject",
#     recognizer=speech_v2.types.cloud_speech.Recognizer(
#         language_codes=["en-US"], model="latest_long"
#     ),
# )

# # Creates a Recognizer
# operation = speech_client.create_recognizer(request=request)
# recognizer = operation.result()
# recognizer = speech_client.get_recognizer(name="projects/top-amplifier-386514/locations/global/recognizers/translateproject")

# Reads a file as bytes
# with open(file_path, "rb") as f:
#     content = f.read()

# config = speech_v2.types.cloud_speech.RecognitionConfig(auto_decoding_config={})

# request = speech_v2.types.cloud_speech.RecognizeRequest(
#     recognizer=recognizer.name, config=config,content=content
# )


# # Transcribes the audio into text
# response = speech_client.recognize(request=request)

# for result in response.results:
#     print(f"Transcript: {result.alternatives[0].transcript}")


# Example usage
# sample_rate = 44100  # Sample rate (e.g., 44100 Hz)

# print("Please speak. Recording will start when you start speaking and stop when you stop.")
# audio = record_audio(sample_rate)
# print("Recording finished.")

# # Save the recorded audio to a file
# file_path = "recorded_audio.wav"
# wavfile.write(file_path, sample_rate, audio)

# print(f"Audio saved to: {file_path}")



