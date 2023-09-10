from translate_class import SpeechToTextTranslator
from openai_class import InformationExtractor
from owlready2 import get_ontology, default_world
from datetime import datetime
import socket
import time as t

class SparqlQuery:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()
    
    def run_query(self, query):
        results = default_world.sparql(query)
        for row in results:
            print(row[0].name)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

now = datetime.now()
hour = now.hour

# Check if it's morning or evening
if 6 <= hour < 18:
    time = "Morning"
else:
    time = "Evening"

def send_nao(Nao_text, language_code):
    if language_code == "en-US":
        language_code = 'English'
    elif language_code == "it-IT":
        language_code = 'Italian'
    elif language_code == "de-DE":
        language_code = 'German'

    message = f"{Nao_text}|{language_code}"

    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print(data)
    return(data)


text = "Hello, my name is Nao. Where do you come from?"
language_code = "en-US"

receipt1 = send_nao(text, language_code)

# print("Nao came from a faraway alien planet called Zog, where robots lived in harmony with nature.")
# print("One day, Nao landed on Earth and met a group of curious children. ")
# print("The children were amazed to see an alien robot standing in front of them.")
# print('Nao: "Hello, young adventurers! I come from a planet called Zog. Where do you come from?"')

# Set the project ID, list of languages, and path to the audio file
# if receipt1 == "b'received'"

project_id = "decent-digit-395614"
language_codes = ["en-US", "de-DE", "it-IT"]
audio_file = "output.wav"

translator = SpeechToTextTranslator(project_id, language_codes, audio_file)

translator.record(audio_file)

transcribed_text, og_language = translator.transcribe_multiple_languages_v2()

# print(transcribed_text)
# print(og_language)

# target_language = input("Specify the code for the target language: ")

# text = translator.translate_text(target_language)

# print(f"Translated text: {text}")

information_extractor = InformationExtractor()

prompt = f"Which country would someone be if he says: {transcribed_text}. Output just the country name"

country = information_extractor.extract_information(transcribed_text, prompt, temperature = 0)

# print(country)

# Create an instance of the SparqlQuery class
sparql_query = SparqlQuery("/home/jerin/robotics/Thesis/pedagogy_ontology_v2.rdf")

# Define the SPARQL query
query = """
    PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
    SELECT ?greeting ?food
    WHERE {{
        ?greeting :hasCountry :{} .
        ?greeting :hasTimeOfDay :{} .
        ?food :hasFood :{} .
    }}
""".format(country, time, country)

# Run the query and print the combined results
results = default_world.sparql(query)
for row in results:
    greeting = row[0].name.replace('_', ' ')
    ontology_text = f"{greeting}, What is your favourite dish? Do you like {row[1].name}?"


text = translator.translate_text(og_language, ontology_text)

# print(f"Translated text: {text}")
send_nao(text, og_language)


client_socket.close()