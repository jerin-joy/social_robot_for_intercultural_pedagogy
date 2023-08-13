import os
import speech_recognition as sr
from google.cloud import translate_v2, speech_v2, texttospeech_v1
from typing import List
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech


def transcribe_multiple_languages_v2(
    project_id: str,
    language_codes: List[str],
    audio_file: str,
) -> cloud_speech.RecognizeResponse:
    """Transcribe an audio file."""
    # Set the path to your API key
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"decent-digit-395614-9ef078739d62.json"

    # Instantiates a client
    client = SpeechClient()

    # Reads a file as bytes
    with open(audio_file, "rb") as f:
        content = f.read()

    config = cloud_speech.RecognitionConfig(
        auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
        language_codes=language_codes,
        model="latest_long",
    )

    request = cloud_speech.RecognizeRequest(
        recognizer=f"projects/{project_id}/locations/global/recognizers/_",
        config=config,
        content=content,
    )

    # Transcribes the audio into text
    response = client.recognize(request=request)

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

    return result.alternatives[0].transcript, response


# Set the project ID, list of languages, and path to the audio file
project_id = "decent-digit-395614"
language_codes = ["en-US", "de-DE", "it-IT"]
audio_file = "output.wav"

r = sr.Recognizer()

# speech_input = input("Specify the code for the input language: ")

with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)

    print("Please say something.. ")

    audio = r.listen(source)
    
# Save the recorded audio to a file
with open(audio_file, "wb") as f:
    f.write(audio.get_wav_data())

# Call the function to transcribe the audio file
text, response = transcribe_multiple_languages_v2(project_id, language_codes, audio_file)


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