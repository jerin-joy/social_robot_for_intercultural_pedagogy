# sparql_query_questions_class.py

from owlready2 import get_ontology, default_world
import random

class SparqlQueryQuestions:
    def __init__(self, ontology_path):
        self.ontology = get_ontology(ontology_path).load()

    def run_query(self, country, time):
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

    def process_greeting_and_food(self, results):
        # Convert the results to a list
        results_list = list(results)

        # Get the greeting from the first result
        greeting = results_list[0][0].name.replace('_', ' ')

        # Get all food items from the results
        foods = [row[1].name for row in results_list]

        # Select a random food item
        random_food = random.choice(foods)

        # List of question formats
        question_formats = [
            "{greeting}! Today, we're going on a culinary journey. Our first stop is {random_food}, a beloved dish in this region.",
            "{greeting}, let's dive into the world of gastronomy. Have you ever tried {random_food}? It's a dish that many people enjoy here.",
            "{greeting}, did you know that {random_food} is a popular dish in this part of the world? It's quite fascinating!",
            "{greeting}, as we explore different cultures, let's not forget about their unique cuisines. For instance, {random_food} is a dish that's well-loved here."
        ]


        # Select a random question format
        question_format = random.choice(question_formats)

        # Generate the text
        return question_format.format(greeting=greeting, random_food=random_food), random_food
    
    def get_country_capital(self, country):
        query = """
            PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
            SELECT ?capital
            WHERE {{
                :{} :hasCapital ?capital .
            }}
        """.format(country)

        results = default_world.sparql(query)
        return self.process_country_capital(results, country)

    def process_country_capital(self, results, country):
        # Convert the results to a list
        results_list = list(results)

        # Get the capital from the first result
        capital = results_list[0][0].name.replace('_', ' ')

        # Generate the text
        return "Oh, that's wonderful! {} is a beautiful country. Did you know that the capital of {} is {}?".format(country, country, capital)

    
    def get_ingredients(self, food):
        query = f"""
            PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
            SELECT ?ingredient
            WHERE {{
                :{food} :hasIngredient ?ingredient .
            }}
        """
        results = default_world.sparql(query)
        ingredients = [row[0].name.replace('_', ' ') for row in results]
        return ', '.join(ingredients)

    def generate_question(self, food, ingredients, country):
        question = f"Did you know that {food} is traditionally made with {ingredients} in {country}? Have you ever helped make it at home?"
        return question
    
    def get_description(self, food):
        query = f"""
            PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
            SELECT ?description
            WHERE {{
                :{food} :hasDescription ?description .
            }}
        """
        results = default_world.sparql(query)
        description = [row[0].name.replace('_', ' ') for row in results]
        return ', '.join(description)
    
    def get_phrases(self, language):
        query = f"""
            PREFIX : <http://www.semanticweb.org/jerin/ontologies/2023/6/pedagogy-ontology-v2#>
            SELECT ?sentence ?translation
            WHERE {{
                ?sentence :has{language}Translation ?translation .
            }}
        """
        results = default_world.sparql(query)
        phrases = [(row[0].name.replace('_', ' '), row[1].name.replace('_', ' ')) for row in results]
        return phrases


