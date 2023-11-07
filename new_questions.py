import random

questions = [
    "Hello there, little Earthlings! My name is Robo, and I come from a faraway planet called Zogar. Where are you from, {}? ",
    "On Zogar, everything sparkles like diamonds, and the trees sing songs with the wind. Imagine that in my home, we communicate through light patterns. How do you express yourselves here, {}? ",
    "I have also discovered that you like eating something called food. In my planet, we eat crystals! What kind of food do you eat in your country, {}?",  
    "However, one day, I decided to take a journey across the galaxies to visit your beautiful planet Earth. As I landed, I felt the soft grass beneath my metal feet and heard the cheerful chirping of birds. What kinds of animals do you have here, {}, and what do you do with them? ",
    "Once on Earth, I met some friendly children who were playing in a park. Their eyes lit up with wonder as they saw me. They had never met a robot like me before! I was so excited to learn about Earth and its incredible creatures. What do you do for fun in your country, {}? ",
    "The children I met showed me around their town, and we discovered amazing things together. It reminded me when, in my planet, we have a celebration called 'Twinkle Day' where we dance under the stars. What special celebrations do you have here, {}?",
    "As the day came to an end, we gathered under the evening sky, watching as the stars began to twinkle. We closed our eyes and made wishes for friendship, kindness, and more intergalactic adventures. What would you wish for, {}, if you could have any adventure in the universe?",
    "And so, dear Earthlings, this day will forever hold a special place in my metal heart. I'll carry the memories of our time together back to Zogar, and I'll always cherish the day I met you. Until we meet again among the stars, remember that you have a friend in me, Robo, from the planet Zogar, {}.",

]

children_names = ["Angela", "Luca", "Marco", "Francesca"]

# Function to get a question with a random child's name
def get_question(index):
    child_name = random.choice(children_names)
    return questions[index].format(child_name)