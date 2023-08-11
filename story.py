# from translate_class import SpeechToTextTranslator
from openai_class import InformationExtractor

print("Once upon a time, in a distant galaxy, there was a friendly robot named Nao. ")
print("Nao came from a faraway alien planet called Zog, where robots lived in harmony with nature.")
print("One day, Nao landed on Earth and met a group of curious children. ")
print("The children were amazed to see an alien robot standing in front of them.")
print('Nao: "Hello, young adventurers! I come from a planet called Zog. Where do you come from?"')

# Set the project ID, list of languages, and path to the audio file
# project_id = "top-amplifier-386514"
# language_codes = ["en-US", "de-DE", "it-IT"]
# audio_file = "output.wav"

# translator = SpeechToTextTranslator(project_id, language_codes, audio_file)

# translator.record(audio_file)

# target_language = input("Specify the code for the target language: ")

# text = translator.translate_text(target_language)

text = "I come from Berlin"

print(f"Translated text: {text}")

information_extractor = InformationExtractor()

prompt = f"Extract the name of the country from the following text: {text}\nCountry: "

print(information_extractor.extract_information(text, prompt))