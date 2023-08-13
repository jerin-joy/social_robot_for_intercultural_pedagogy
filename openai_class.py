from openai_key import api_key
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

# extractor = InformationExtractor()
# text = input("Enter the text: ")
# prompt = f"Extract the name of the country from the following text: {text}\nCountry: "
# country = extractor.extract_information(text, prompt)
# print(f"The country in the text '{text}' is: {country}")

# prompt = f"Extract the name of the food from the following text: {text}\nFood: "
# food = extractor.extract_information(text, prompt)
# print(f"The food in the text '{text}' is: {food}")
