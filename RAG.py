from deepagents import create_deep_agent
from langchain.messages import HumanMessage

"""electric_Energy_Docs = ["https://en.wikipedia.org/wiki/Electrical_energy",
                        "https://www.thoughtco.com/electrical-energy-definition-and-examples-4119325",
                        "https://www.eia.gov/energyexplained/electricity/the-science-of-electricity.php",
                        "https://en.wikipedia.org/wiki/Electric_current",
                        "https://www.britannica.com/technology/electric-circuit",
                        "https://en.wikipedia.org/wiki/Voltage",
                        "https://learn.sparkfun.com/tutorials/alternating-current-ac-vs-direct-current-dc/all",
                        "https://www.wevolver.com/article/parallel-vs-series-circuits-differences-theory-and-practical-applications",
                        "https://en.wikipedia.org/wiki/Watt",
                        "https://cc-techgroup.com/blog/what-is-resistance/",
                        "https://en.wikipedia.org/wiki/Electrolysis",
                        "https://www.britannica.com/science/electricity"]"""
# electric energy, voltage, electric circuit, electric current, AC/DC, watts, parrallel vs series circuits, resistance, ohms, electrolysis,
# electricity, energy
# this was the old websites, which we might not use.

# ___________________________________________
# Evaluation questions in dict format (Luke), making 16. You guys can remove 6 or something if I made too many.
# ___________________________________________

eval_questions_dict = {1:"What is one houshold item that is using a lot of energy consumption?",
                       2:"How can I reduce my energy consumption?",
                       3:"What is causing the most energy consumption? The fridge, the oven or the kettle?",
                       4:"Would using solar panels reduce energy consumption?",
                       5:"Would five solar panels be able to generate enough energy for all household items in the average household?",
                       6:"What is one household item that is using little energy consumption?",
                       7:"What are simple things that I can do right now to reduce energy consumption?",
                       8:"Do lights use more energy consumption than fans?",
                       9:"Would leaving everything on reduce energy consumption?", # this should give a no answer.
                       10:"How many solar panels do we need for a large house with a lot of household items?", # a little ambiguous
                       11:"What is the average energy consumption for any household?",
                       12:"What would increase my energy consumption?",
                       13:"Do solar panels use more energy consumption than traditional methods?",
                       14:"What is using the least energy consumption? The lights, the TV or the fridge?",
                       15:"How do I reduce my energy consumption, without having to decrease the quality of life?", # Maybe?
                       16:"Would ten solar panels be able to generate enough energy for all household items in a large household?"}