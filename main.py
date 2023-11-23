import gradio as gr
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.llms import Ollama
import os
import time
import random
from langchain.prompts.prompt import PromptTemplate
from dotenv import load_dotenv



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

Examples:
# How many people played in Top Gun?
MATCH (m:Movie {{title:"Top Gun"}})<-[:ACTED_IN]-()
RETURN count(*) AS numberOfActors

# Give me the list of actors sorted by the number of movies they played in.
MATCH (a:Actor)-[:ACTED_IN]->(m:Movie)
RETURN a.name AS actor, count(*) AS numberOfMovies
ORDER BY numberOfMovies DESC


The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)
# Load environment variables
load_dotenv()

neo4j_config = {
    "url": "neo4j+s://0d9a0c6b.databases.neo4j.io",
    "username": os.getenv("NEO4J_USER"),
    "password": os.getenv("NEO4J_PASSWORD"),
}

print(neo4j_config)


neo4j_graph = Neo4jGraph(url=neo4j_config["url"], username=neo4j_config["username"], password=neo4j_config["password"])
# check if the graph is connected
print(neo4j_graph.get_schema)
print(neo4j_graph.get_structured_schema)

# close the connection _driver
llm = Ollama(temperature=0)
qa_llm = Ollama(temperature=0.1)

graph_cypher_params = {
    "graph": neo4j_graph,
    "llm": llm,
    "verbose": True,
    "cypher_prompt":CYPHER_GENERATION_PROMPT,
}


qa_chain = GraphCypherQAChain.from_llm(**graph_cypher_params)

# Gradio Chatbot Interface
def chatbot_function(message):
    return qa_chain(message)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

    def respond(message, chat_history):
        # Assuming chatbot_function returns a dictionary with 'query' and 'result' keys
        result = chatbot_function(message)
        bot_response = result['result']  # Extract the response part
        chat_history.append((message, bot_response))  # Append as a tuple
        return "", chat_history


    msg.submit(respond, [msg, chatbot], [msg, chatbot])


demo.launch()
neo4j_graph._driver.close()