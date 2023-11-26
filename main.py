import gradio as gr
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.llms import Ollama
import os
import time
import random
from template import CYPHER_GENERATION_PROMPT
from dotenv import load_dotenv


load_dotenv()

neo4j_config = {
    "url": "neo4j+s://0d9a0c6b.databases.neo4j.io:7687",
    "username": os.getenv("NEO4J_USER"),
    "password": os.getenv("NEO4J_PASSWORD"),
}

neo4j_graph = Neo4jGraph(url=neo4j_config["url"], username=neo4j_config["username"], password=neo4j_config["password"])
# check if the graph is connected
print(neo4j_graph.get_schema)
print(neo4j_graph.get_structured_schema)

# llm is ollama codellama:7b-instruct
llm = Ollama(model="codellama:7b-instruct", temperature=0)

graph_cypher_params = {
    "graph": neo4j_graph,
    "llm": llm,
    "verbose": True,
    "cypher_prompt":CYPHER_GENERATION_PROMPT,
}

qa_chain = GraphCypherQAChain.from_llm(**graph_cypher_params)


def chatbot_function(message):
    return qa_chain(message)


with gr.Blocks() as demo:
    chatbot = gr.Chatbot(height=600)
    msg = gr.Textbox()
    with gr.Row():
        clear = gr.ClearButton([msg, chatbot])
        submit = gr.Button()

    def respond(message, chat_history):
        result = chatbot_function(message)
        bot_response = result['result']
        chat_history.append((message, bot_response))
        return "", chat_history

    submit.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])


demo.launch()
neo4j_graph._driver.close()