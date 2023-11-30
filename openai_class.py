from openai_key import api_key
import openai
import time
import requests

class InformationExtractor:
    def __init__(self):
        # Set up your OpenAI API credentials
        openai.api_key = api_key

    def extract_information(self, text: str, prompt: str, temperature = 0.5, max_retries=5, timeout=5) -> str:
        for i in range(max_retries):
            try:
                start_time = time.time()  # Start the timer
                response = openai.ChatCompletion.create(
                    model = "gpt-3.5-turbo",
                    messages = [
                        {"role":"user", "content":prompt}
                    ],
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=temperature,
                    timeout=timeout  # Add a timeout
                )
                end_time = time.time()  # End the timer

                print("Time taken for OpenAI API request: {} seconds".format(end_time - start_time))
                information = response['choices'][0]['message']['content']
                return information
            except (openai.error.OpenAIError, requests.exceptions.Timeout):
                print(f"Request failed or timed out, retrying ({i+1}/{max_retries})")
                time.sleep(1)  # Wait for 1 second before retrying
        raise Exception("Request failed or timed out after multiple attempts")



# extractor = InformationExtractor()
# text = input("Enter the text: ")
# prompt = f"Extract the name of the country from the following text: {text}\nCountry: "
# country = extractor.extract_information(text, prompt)
# print(f"The country in the text '{text}' is: {country}")

# prompt = f"Extract the name of the food from the following text: {text}\nFood: "
# food = extractor.extract_information(text, prompt)
# print(f"The food in the text '{text}' is: {food}")
