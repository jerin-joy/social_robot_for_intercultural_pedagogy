# sparql_query_questions_class.py

from owlready2 import get_ontology, default_world
import random

class SparqlQueryQuestions:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

    def run_query(self, country, time):
        # List of query types and their corresponding processing methods
        query_types = ["greeting_and_food", "sport"]
        
        # Select a random query type
        query_type = random.choice(query_types)
        
        if query_type == "greeting_and_food":
            query = """
                PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
                SELECT ?greeting ?food
                WHERE {{
                    ?greeting :hasCountry :{} .
                    ?greeting :hasTimeOfDay :{} .
                    ?food :hasFood :{} .
                }}
            """.format(country, time, country)
            results = default_world.sparql(query)
            return self.process_greeting_and_food(results)
        
        elif query_type == "sport":
            query = """
                PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
                SELECT ?greeting ?sport
                WHERE {{
                    ?greeting :hasCountry :{} .
                    ?greeting :hasTimeOfDay :{} .
                    ?sport :isPopularIn :{} .
                }}
            """.format(country, time, country)
            results = default_world.sparql(query)
            return self.process_sport(results)

    def process_greeting_and_food(self, results):
        # Convert the results to a list
        results_list = list(results)

        # Get the greeting from the first result
        greeting = results_list[0][0].name.replace('_', ' ')

        # Get all food items from the results
        foods = [row[1].name for row in results_list]

        # Select a random food item
        random_food = random.choice(foods)

        # Generate the text
        return f"{greeting}, What is your favourite dish? Do you like {random_food}?"

    def process_sport(self, results):
        # Convert the results to a list
        results_list = list(results)

        # Get the greeting from the first result
        greeting = results_list[0][0].name.replace('_', ' ')

        # Get all sports from the results
        sports = [row[1].name for row in results_list]

        # Select a random sport
        random_sport = random.choice(sports)

        # Generate the question
        return f"{greeting}, Nice to meet you. What sports do you like? Do you like {random_sport}?"
