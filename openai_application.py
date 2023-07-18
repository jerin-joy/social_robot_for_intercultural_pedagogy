from openai_key import api_key
import openai

# Set up your OpenAI API credentials
openai.api_key = api_key


response = openai.Completion.create(
  model="text-curie-001",
  prompt = input("You: "),
  temperature=1,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

answer = response.choices[0].text.strip()
print("Nao: ", answer)