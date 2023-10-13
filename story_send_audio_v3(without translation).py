from translate_class import SpeechToTextTranslator
# from translation_handler import TranslationHandler
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

translation_keywords = {
    "en-US": ["translate", "translation", "interpret", "interpreter", "convert"],
    "it-IT": ["tradurre", "tradurlo", "traduzione", "interpretare", "interprete", "convertire"],
    "Spanish": ["traducir", "traducción", "interpretar", "intérprete", "convertir"],
    "de-DE": ["übersetzen", "Übersetzung", "dolmetschen", "Dolmetscher", "umwandeln"]
}

def translation_request(transcribed_text, text_to_be_translated, og_language):
    # prompt = f"Robot asked Child: '{text_to_be_translated}', Child replied: '{transcribed_text}'. If translation is requested on the child's reply, give the translation of the question/reply('it'/'question' might refer to what robot asked) without asking follow-up questions. If No translation is requested, return just NO (Nothing else and no explanation). "
    prompt = f"Child asked robot: Can you translate {text_to_be_translated}. Provide its translation and the explanation in {og_language} "
    # prompt = f"Check if translation is explicitly requested in the following message: {transcribed_text}. If yes, give the translation without asking follow-up questions. If No, return just NO (Nothing else and no explanation). Does this reply ask to translate the previous question? If yes, return YES. If No, return No"
    response = information_extractor.extract_information(transcribed_text, prompt, temperature=0)
    print(response)
    # if response.lower() == "no":
    #     return None
    # translate_and_synthesize(og_language, ontology_text=response)
    send_nao(Nao_text=response, language_code=og_language)
    # return True

def is_translation_request(transcribed_text, og_language,text_to_be_translated):
    for keyword in translation_keywords[og_language]:
        if keyword in transcribed_text:
            print("It's a translation request")
            translation_request(transcribed_text, text_to_be_translated, og_language)
            return True
    return False

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

def get_response_make_dish(transcribed_text):
    prompt = f"The child was asked: 'Have you ever helped make _____(a dish) at home?'. The child replied: '{transcribed_text}'. Give a reply to the child's answer without asking a question."
    response = information_extractor.extract_information(transcribed_text, prompt, temperature=0)
    print(response)
    translate_and_synthesize(og_language, ontology_text=response)

def get_response_try_dish(transcribed_text):
    prompt = f"The child was asked: 'Have you ever tried _____(a dish)?'. The child replied: '{transcribed_text}'. Give a reply to the child's answer WITHOUT asking a question at the end."
    response = information_extractor.extract_information(transcribed_text, prompt, temperature=0)
    print(response)
    translate_and_synthesize(og_language, ontology_text=response)

def get_response_yes_or_no(transcribed_text):
    prompt = f"The child was asked: 'Would you like to learn a few simple phrases in ____ (language). The child replied: '{transcribed_text}'. Return a 'Yes' or 'No' based on the child's answer"
    response = information_extractor.extract_information(transcribed_text, prompt, temperature=0)
    print(response)
    translate_and_synthesize(og_language, ontology_text=response)
    return response.lower()

def get_country(transcribed_text):
    prompt = f"Which country would someone be if he says: {transcribed_text}. Output just the country name"
    return information_extractor.extract_information(transcribed_text, prompt, temperature=0)

def user_translation(transcribed_text):
    prompt = f"Robot asked child: 'What would you like to translate and to which language do you want to translate it?'. The child replied: {transcribed_text}. Give the response without asking follow-up questions."
    response = information_extractor.extract_information(transcribed_text, prompt, temperature=0)
    print(response)
    translate_and_synthesize(og_language, ontology_text=response)
    

project_id = "decent-digit-395614"
language_codes = ["en-US", "de-DE", "it-IT"]
audio_file = "output.wav"

information_extractor = InformationExtractor()
translator = SpeechToTextTranslator(project_id, language_codes, audio_file)
sparql_query = SparqlQueryQuestions("/home/jerin/robotics/Thesis/pedagogy_ontology_v2.rdf")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 12345))

time = "Morning" if 6 <= datetime.now().hour < 18 else "Evening"

while True:
    text = "I'm Nao. Where do you come from?"
    language_code = "en-US"
    translator.synthesize_speech(language_code, text)

    receipt1 = send_nao(text, language_code)

    # translator.record(audio_file)
    # transcribed_text, og_language = translator.transcribe_multiple_languages_v2()

    transcribed_text = input("Type your response: ")
    og_language = input("Write your language code: ")

    translation_request_result = is_translation_request(transcribed_text, og_language,text_to_be_translated=text)

    if translation_request_result is False:
        country = get_country(transcribed_text)

        ontology_text, random_food = sparql_query.run_query(country, time)
        print(ontology_text)
        translate_and_synthesize(og_language, ontology_text)
        break



ingredients = sparql_query.get_ingredients(random_food)
text = sparql_query.generate_question(random_food, ingredients, country)
print(text)
translate_and_synthesize(og_language, ontology_text=text)

translator.record(audio_file)
transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
# transcribed_text = input("Type your response: ")
# og_language = input("Write your language code: ")
get_response_make_dish(transcribed_text)

text = "Now, let's explore another culture. Where would you like to go next?"
print(text)
translate_and_synthesize(og_language, ontology_text=text)

translator.record(audio_file)
transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
# transcribed_text = input("Type your response: ")
# og_language = input("Write your language code: ")

country = get_country(transcribed_text)
if country == "Germany":
    native_language = "German"
if country == "Italy":
    native_language = "Italian"

ontology_text, random_food = sparql_query.run_query(country, time)
description = sparql_query.get_description(random_food)

text = f"Wonderful choice! In {country}, people enjoy {random_food}. It’s a delicious {description}. Have you ever tried it?"
print(text)
translate_and_synthesize(og_language, ontology_text=text)

translator.record(audio_file)
transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
# transcribed_text = input("Type your response: ")
# og_language = input("Write your language code: ")
get_response_try_dish(transcribed_text)

question =f"Apart from its cuisine, {country} is also known for its language. Would you like to learn a few simple phrases in {native_language}?"
print(question)
translate_and_synthesize(og_language, ontology_text=question)

translator.record(audio_file)
transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
# transcribed_text = input("Type your response: ")
# og_language = input("Write your language code: ")
response = get_response_yes_or_no(transcribed_text)
print(response)

if response == 'yes':
    phrases = sparql_query.get_phrases(native_language)
    phrase_strings = [f'"{translation}" means "{phrase}"' for phrase, translation in phrases]

    # Join the phrase strings into a single string with commas and spaces between them
    phrase_string = ', '.join(phrase_strings)

    phrases = f"Great! Here are a few phrases: {phrase_string}"
    print(phrases)
    translate_and_synthesize(og_language, ontology_text=phrases)

    question = "Would you like to hear it one more time?"
    print(question)
    translate_and_synthesize(og_language, ontology_text=question)

    translator.record(audio_file)
    transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
    # transcribed_text = input("Type your response: ")
    # og_language = input("Write your language code: ")
    response = get_response_yes_or_no(transcribed_text)
    print(response)

    if response == 'yes':
        phrases = sparql_query.get_phrases(native_language)
        phrase_strings = [f'"{translation}" means "{phrase}"' for phrase, translation in phrases]

        # Join the phrase strings into a single string with commas and spaces between them
        phrase_string = ', '.join(phrase_strings)

        phrases = f"Great! Here are a few phrases: {phrase_string}"
        print(phrases)
        translate_and_synthesize(og_language, ontology_text=phrases)
    else:
        text = "Okay. Let's move on to another topic."
        translate_and_synthesize(og_language, ontology_text=text)

else:
    text = "Okay. Let's move on to another topic."
    translate_and_synthesize(og_language, ontology_text=text)

text = f"Would you like to translate something in {og_language} to any other language?"
print(text)
translate_and_synthesize(og_language, ontology_text=text)

translator.record(audio_file)
transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
# transcribed_text = input("Type your response: ")
# og_language = input("Write your language code: ")
response = get_response_yes_or_no(transcribed_text)
print(response)

if response == 'yes':
    text = "What would you like to translate and to which language you want to translate it to?"
    print(text)
    translate_and_synthesize(og_language, ontology_text=text)
    translator.record(audio_file)
    transcribed_text, og_language = translator.transcribe_multiple_languages_v2()
    # transcribed_text = input("Type your response: ")
    # og_language = input("Write your language code: ")

    user_translation(transcribed_text)





    
    

client_socket.close()