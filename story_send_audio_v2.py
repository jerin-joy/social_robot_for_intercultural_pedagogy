from translate_class import SpeechToTextTranslator
from openai_class import InformationExtractor
from owlready2 import get_ontology, default_world
from datetime import datetime
import socket
from pydub import AudioSegment
from questions import SparqlQueryQuestions

class SparqlQuery:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

    def run_query(self, query):
        results = default_world.sparql(query)
        for row in results:
            print(row[0].name)

def send_nao(Nao_text, language_code):
    language_code = {'en-US': 'English', 'it-IT': 'Italian', 'de-DE': 'German'}.get(language_code, language_code)
    message = f"{Nao_text}|{language_code}"
    client_socket.sendall(message.encode())
    data = client_socket.recv(1024)
    print(data)
    return(data)

def translate_and_synthesize(og_language, ontology_text):
    text = translator.translate_text(og_language, ontology_text)
    translator.synthesize_speech(og_language, text)
    send_nao(text, og_language)

def get_response(transcribed_text):
    prompt = f"The child was asked: 'Have you ever helped make _____(a dish) at home?'. The child replied: '{transcribed_text}'. Give a reply to the child's answer without asking a question."
    response = information_extractor.extract_information(transcribed_text, prompt, temperature=0)
    print(response)
    translate_and_synthesize(og_language, ontology_text=response)

def get_country(transcribed_text):
    prompt = f"Which country would someone be if he says: {transcribed_text}. Output just the country name"
    return information_extractor.extract_information(transcribed_text, prompt, temperature=0)

project_id = "decent-digit-395614"
language_codes = ["en-US", "de-DE", "it-IT"]
audio_file = "output.wav"

translator = SpeechToTextTranslator(project_id, language_codes, audio_file)
information_extractor = InformationExtractor()
sparql_query = SparqlQueryQuestions("/home/jerin/robotics/Thesis/pedagogy_ontology_v2.rdf")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

time = "Morning" if 6 <= datetime.now().hour < 18 else "Evening"


text = "I'm Nao. Where do you come from?"
language_code = "en-US"
translator.synthesize_speech(language_code, text)

receipt1 = send_nao(text, language_code)

transcribed_text = input("Type your response: ")
og_language = input("Write your language code: ")

country = get_country(transcribed_text)

ontology_text, random_food = sparql_query.run_query(country, time)
print(ontology_text)
translate_and_synthesize(og_language, ontology_text)

ingredients = sparql_query.get_ingredients(random_food)
text = sparql_query.generate_question(random_food, ingredients, country)
print(text)
translate_and_synthesize(og_language, ontology_text=text)

transcribed_text = input("Type your response: ")
og_language = input("Write your language code: ")
get_response(transcribed_text)

translate_and_synthesize(og_language, "Now, let's explore another culture. Where would you like to go next?")

transcribed_text = input("Type your response: ")
og_language = input("Write your language code: ")

country = get_country(transcribed_text)

ontology_text, random_food = sparql_query.run_query(country, time)
description = sparql_query.get_description(random_food)

text = f"Wonderful choice! In {country}, people enjoy {random_food}. It’s a delicious {description}. Have you ever tried it?"
print(text)
translate_and_synthesize(og_language, ontology_text=text)

client_socket.close()
