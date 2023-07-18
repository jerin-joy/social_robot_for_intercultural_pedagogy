import os
from owlready2 import get_ontology

current_directory = os.path.dirname(os.path.abspath(__file__))

ontology_file_name = "ontology_v1.rdf"  
ontology_file_path = os.path.join(current_directory, ontology_file_name)

ontology = get_ontology("file://" + ontology_file_path).load()

Culture = ontology.Culture

ItalianGreeting = ontology.ItalianGreeting

all_greetings = list(ontology.Greeting.instances())

italian_greeting_text = ItalianGreeting.hasText[0]

print(italian_greeting_text)
