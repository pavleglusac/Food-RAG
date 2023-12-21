import gradio as gr
from langchain.chains import GraphCypherQAChain
from sparql_chain import GraphSparqlQAChain
from langchain.llms import Ollama, OpenAI
import os
import time
import random
# from template import CYPHER_GENERATION_PROMPT
from dotenv import load_dotenv
from rdflib import Graph
from langchain.graphs import RdfGraph

from template import SPARQL_GENERATION_SELECT_PROMPT

load_dotenv()

# llm is ollama codellama:7b-instruct
llm_lamma = Ollama(model="codellama:7b-instruct", temperature=0)
llm_gpt4 = OpenAI(model="gpt4", temperature=0)
llm_gpt3_5 = OpenAI(model="gpt-3.5-turbo", temperature=0)

graph = RdfGraph(
    source_file="/mnt/ACA058A9A0587C30/Faks/Master/Food-RAG/ontology/files/ingredients.rdf",
    standard="owl",
    serialization="xml"
)
graph.load_schema()
print(graph.get_schema)
# graph = RdfGraph(graph)

# Create a chain for the RDF graph
qa_chain_llama = GraphSparqlQAChain.from_llm(llm_lamma, graph=graph, verbose=True, sparql_select_prompt=SPARQL_GENERATION_SELECT_PROMPT)

qa_chain_gpt4 = GraphSparqlQAChain.from_llm(llm_gpt4, graph=graph, verbose=True, sparql_select_prompt=SPARQL_GENERATION_SELECT_PROMPT)

qa_chain_gpt3_5 = GraphSparqlQAChain.from_llm(llm_gpt3_5, graph=graph, verbose=True, sparql_select_prompt=SPARQL_GENERATION_SELECT_PROMPT)


def chatbot_function(message, model="Code LLaMa"):
    if model == "Code LLaMa":
        return qa_chain_llama(message)
    elif model == "GPT4":
        return qa_chain_gpt4(message)
    elif model == "GPT3.5":
        return qa_chain_gpt3_5(message)
    else:
        return "Model not found"


with gr.Blocks() as demo:
    model_options = ["Code LLaMa", "GPT4", "GPT3.5"]
    model_dropdown = gr.Dropdown(choices=model_options, label="Select Model", value="Code LLaMa")
    chatbot = gr.Chatbot(height=600)
    msg = gr.Textbox()
    with gr.Row():
        clear = gr.ClearButton([msg, chatbot])
        submit = gr.Button()

    def respond(message, model, chat_history):
        result = chatbot_function(message, model=model_dropdown.value)
        bot_response = result['result']
        chat_history.append((message, bot_response))
        return "", model, chat_history

    submit.click(respond, [msg, model_dropdown, chatbot], [msg, model_dropdown, chatbot])
    msg.submit(respond, [msg, model_dropdown, chatbot], [msg, model_dropdown, chatbot])


demo.launch()