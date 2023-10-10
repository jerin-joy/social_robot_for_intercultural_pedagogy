from openai_key import api_key
from translate_class import SpeechToTextTranslator
import openai

class InformationExtractor:
    def __init__(self):
        # Set up your OpenAI API credentials
        openai.api_key = api_key

    def extract_information(self, text: str, prompt: str, temperature = 0.5) -> str:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = [
                {"role":"user", "content":prompt}
            ],
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=temperature,
        )
        information = response['choices'][0]['message']['content']
        return information

    def handle_translation_request(self, text: str, translator: SpeechToTextTranslator):
        # Use OpenAI API to check if text is a translation request
        prompt = f"The user said: '{text}'. If the user is asking for a translation, return the target language code. Otherwise, return 'Not a translation request'."
        target_language = self.extract_information(text, prompt)

        if target_language != 'Not a translation request':
            # If it's a translation request, call translate_last_sentence
            translated_sentence = translator.translate_last_sentence(target_language)
            return translated_sentence
        else:
            # If it's not a translation request, return None
            return None

# extractor = InformationExtractor()
# text = input("Enter the text: ")
# prompt = f"Extract the name of the country from the following text: {text}\nCountry: "
# country = extractor.extract_information(text, prompt)
# print(f"The country in the text '{text}' is: {country}")

# prompt = f"Extract the name of the food from the following text: {text}\nFood: "
# food = extractor.extract_information(text, prompt)
# print(f"The food in the text '{text}' is: {food}")
