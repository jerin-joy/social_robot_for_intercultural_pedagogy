from translate_class import SpeechToTextTranslator
from openai_class import InformationExtractor
from owlready2 import get_ontology, default_world
from datetime import datetime
import socket
import time as t
from pydub import AudioSegment
from questions import SparqlQueryQuestions

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

project_id = "decent-digit-395614"
language_codes = ["en-US", "de-DE", "it-IT"]
audio_file = "output.wav"

translator = SpeechToTextTranslator(project_id, language_codes, audio_file)


text = "I'm Nao. Where do you come from?"
language_code = "en-US"
translator.synthesize_speech(language_code, text)

receipt1 = send_nao(text, language_code)


translator.record(audio_file)

transcribed_text, og_language = translator.transcribe_multiple_languages_v2()


information_extractor = InformationExtractor()

prompt = f"Which country would someone be if he says: {transcribed_text}. Output just the country name"

country = information_extractor.extract_information(transcribed_text, prompt, temperature = 0)


# Create an instance of the SparqlQuery class
sparql_query = SparqlQueryQuestions("/home/jerin/robotics/Thesis/pedagogy_ontology_v2.rdf")

# Run the query and get the combined results
ontology_text = sparql_query.run_query(country, time)

print(ontology_text)


text = translator.translate_text(og_language, ontology_text)
translator.synthesize_speech(og_language, text)

# print(f"Translated text: {text}")
send_nao(text, og_language)


client_socket.close()