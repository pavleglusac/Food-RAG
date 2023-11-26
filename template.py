from langchain.prompts.prompt import PromptTemplate


CYPHER_GENERATION_TEMPLATE = """
Task:Generate Cypher statement to query a graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Never include any comments in your Cypher statement, nor any explanations or apologies, only executeable Cypher.

Schema:
{schema}

Notes: 
Do not include any explanations or apologies in your responses. Do not make jokes, be straightforward and concise.
Do not include any text except the generated Cypher statement.
Reply ONLY with the generated Cypher statement that can be executed in Neo4j directly.
NEVER start your response with "Here is the Cypher statement:" or anything similar.
NEVER include any text except the generated Cypher statement.
When asked for string LENGTH use the SIZE function.


When asked if a Dish contains a specific ingredient, use the following query:

MATCH (dish:Dish {{name: <DISH NAME>}})-[:CONTAINS*0..]->(ingredient)
WITH dish, COLLECT(ingredient.name) AS ingredients
OPTIONAL MATCH (ingredient)-[:MADE_OF*0..]->(subIngredient:Ingredient {{name: <TARGET INGREDIENT>}})
WITH ingredients, COLLECT(subIngredient.name) AS subIngredients
RETURN <TARGET INGREDIENT> IN ingredients OR <TARGET INGREDIENT> IN subIngredients AS containsFlour

But use it ONLY if you are asked if a Dish contains a specific ingredient, never if you are asked for a list of ingredients.

Examples:
# How many people played in Top Gun?
MATCH (m:Movie {{title:"Top Gun"}})<-[:ACTED_IN]-()
RETURN count(*) AS numberOfActors

# Give me the list of actors sorted by the number of movies they played in.
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
RETURN a.name AS actor, count(*) AS numberOfMovies
ORDER BY numberOfMovies DESC


# Give me what the hambuger is made of.
MATCH (dish:Dish {{name: "Hamburger"}})-[:MADE_OF]->(ingredient)
RETURN ingredient.name AS ingredient


The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
