from openai_key import api_key
import openai

# Set up your OpenAI API credentials
openai.api_key = api_key

def extract_country(sentence):
    prompt = f"Extract the name of the country from the following sentence: {sentence}\nCountry: "
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = [
            {"role":"user", "content":prompt}
        ],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    country = response['choices'][0]['message']['content']
    return country

sentence = input("Where do you come from? ")
country = extract_country(sentence)
print(f"The country in the sentence '{sentence}' is: {country}")