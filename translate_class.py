import os
import html
import speech_recognition as sr
from google.cloud import translate_v2, speech_v2, texttospeech_v1
from typing import List, Tuple
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
from pydub import AudioSegment



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"resonant-tract-404715-632e6ffe2635.json"

class SpeechToTextTranslator:
    def __init__(self, project_id: str, language_codes: List[str], audio_file: str):
        self.project_id = project_id
        self.language_codes = language_codes
        self.audio_file = audio_file
        self.last_spoken_sentence = None

    def record(self, audio_file: str) -> None:
        r = sr.Recognizer()

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)

            print("Please say something.. ")

            audio = r.listen(source)

        # Save the recorded audio to a file
        with open(audio_file, "wb") as f:
            f.write(audio.get_wav_data())


    def transcribe_multiple_languages_v2(self) -> Tuple[str, cloud_speech.RecognizeResponse]:
        """Transcribe an audio file."""
        # Set the path to your API key
        # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"google_key.json"

        # Instantiates a client
        client = SpeechClient()

        # Reads a file as bytes
        with open(self.audio_file, "rb") as f:
            content = f.read()

        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=self.language_codes,
            model="latest_long",
        )

        request = cloud_speech.RecognizeRequest(
            recognizer=f"projects/{self.project_id}/locations/global/recognizers/_",
            config=config,
            content=content,
        )

        # Transcribes the audio into text
        response = client.recognize(request=request)

        if response.results:
            for result in response.results:
                pass
            return result.alternatives[0].transcript, result.language_code
        else:
            return None, None  # or some other default value

        # for result in response.results:
        #     # print(f"Transcript: {result.alternatives[0].transcript}")
        #     pass

        
        # # Check if it's a translation request
        # translated_sentence = self.information_extractor.handle_translation_request(result.alternatives[0].transcript, self)

        # if translated_sentence is not None:
        #     # If it's a translation request, use the translated sentence in your robot's response
        #     print(translated_sentence)
        # else:
        #     # If it's not a translation request, return the transcribed text and language code as usual
        #     return result.alternatives[0].transcript, result.language_code

        # return result.alternatives[0].transcript, result.language_code

    def translate_text(self, target_language: str, ontology_text: str) -> str:
        translate_client = translate_v2.Client()
        
        # Call the function to transcribe the audio file
        # text, response = self.transcribe_multiple_languages_v2()
        
        output = translate_client.translate(ontology_text, target_language=target_language)
        
        translated_text = html.unescape(output['translatedText'])
    
        return translated_text
    
    def translate_last_sentence(self, target_language):
        if self.last_spoken_sentence is None:
            print("I haven't spoken anything yet.")
        else:
            translated_text = self.translate_text(target_language, self.last_spoken_sentence)
            return translated_text


    def synthesize_speech(self, target_language: str, text: str) -> None:

        self.last_spoken_sentence = text
        speech_client = texttospeech_v1.TextToSpeechClient()
        
        translated_text = self.translate_text(target_language, text)
        
        synthesis_input = texttospeech_v1.SynthesisInput(text=translated_text)

        if target_language == 'en-US':
            voice1 = texttospeech_v1.VoiceSelectionParams(
                language_code=target_language,
                ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE,
                name='en-US-Wavenet-F'  # This is an example of a female voice for US English
            )
        else:
            voice1 = texttospeech_v1.VoiceSelectionParams(
                language_code=target_language,
                ssml_gender=texttospeech_v1.SsmlVoiceGender.FEMALE
            )

        audio_config = texttospeech_v1.AudioConfig(
            audio_encoding=texttospeech_v1.AudioEncoding.MP3
        )

        response1 = speech_client.synthesize_speech(
            input=synthesis_input,
            voice=voice1,
            audio_config=audio_config
        )

        with open('audio.mp3', 'wb',) as output:
            output.write(response1.audio_content)
        
        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("audio.wav", format="wav")



