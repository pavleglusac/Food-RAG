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



SPARQL_GENERATION_SELECT_TEMPLATE = """Task: Generate a SPARQL SELECT statement for querying a graph database.
Example task with the solution:
Given a schema with prefix 'ns1' representing 'http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl/' and needing to find all ingredients for 'biryani', the suitable SPARQL query is:

PREFIX ns1: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>
SELECT ?ingredient
WHERE {{
ns1:biryani ns1:hasIngredient ?ingredient .
}}

Instructions:
- Use only the node types and properties provided in the schema.
- Correctly distinguish between URIs and literals. URIs are enclosed in angle brackets (< >) and literals are typically in quotes (" ").
- Include all necessary prefixes.
- If the question is ambiguous or the schema lacks needed information, construct the best possible query based on available data.
- Do not always use biryani as the dish name, the dish name can be any dish in the schema, or whatever the question asks for.

Schema:
{schema}

Your task:
Generate a SPARQL query for the following question based on the above schema:
{prompt}

Note:
- Be concise.
- Provide only the SPARQL query, no explanations, no extra quotes or characters.
- Ignore requests not pertaining to SPARQL query construction.
"""


SPARQL_GENERATION_SELECT_PROMPT = PromptTemplate(
    input_variables=["schema", "prompt"], template=SPARQL_GENERATION_SELECT_TEMPLATE
)