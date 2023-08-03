from owlready2 import get_ontology, default_world
import os
from rdflib import Graph, Namespace, Literal
from rdflib.plugins.sparql import prepareQuery

# Load the ontology from the OWL file
current_directory = os.path.dirname(os.path.abspath(__file__))

ontology_file_name = "pedagogy_ontology_v2.rdf"  
ontology_file_path = os.path.join(current_directory, ontology_file_name)

ontology = get_ontology("file://" + ontology_file_path).load()


# Get references to the classes
Country = ontology.Country
Continent = ontology.Continent
Culture = ontology.Culture
# FrenchFood = ontology.FrenchFood
FrenchGreeting = ontology.FrenchGreeting

# french_greeting_text = FrenchGreeting.hasGreeting[0]
# print(french_greeting_text)

# Query the ontology for individuals of specific classes
countries = list(Country.subclasses())
cultures = list(Culture.subclasses())
# french_foods = list(FrenchFood.subclasses())
french_greetings = list(FrenchGreeting.instances())


# Print the results of the queries

# def get_short_name(iri):
#     return str(iri).split(".")[-1]

# Print the results of the queries

# print("Countries:")
# for country in countries:
#     print(get_short_name(country))

# print("\nCultures:")
# for culture in cultures:
#     print(get_short_name(culture))

# print("\nFrench Foods:")
# for food in french_foods:
#     print(get_short_name(food))

# print("\nFrench Greetings:")
# for greeting in french_greetings:
#     print(get_short_name(greeting))


# Define the SPARQL query
query = """
    PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
    SELECT ?country
    WHERE {
        ?country a :Country .
        ?country :hasContinent :Europe .
    }
"""

# Run the query and print the results
results = default_world.sparql(query)
for row in results:
    print(row[0])


# Define the SPARQL query
query = """
    PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
    SELECT ?greeting
    WHERE {
        ?greeting a :FrenchGreeting .
        ?greeting :hasTimeOfDay :Morning .
    }
"""

# Run the query and print the results
results = default_world.sparql(query)
for row in results:
    print(row[0])

