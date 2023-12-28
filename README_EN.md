# Food-RAG
Food-RAG is a project that enables users to easily explore the ingredients of various dishes by posing queries in natural language. The project has implemented an ontology in the form of an RDF graph that stores data about ingredients and dishes. Users are presented with a simple interface and given the ability to pose queries in a chat, which are later translated into SPARQL format and executed over the created ontology.

## Installation
For installation, it is necessary to use Python version 3.10 or newer.
The required Python packages are listed in the requirements.txt file and can be installed with
```shell
pip3 install -r requirements.txt
```

It is also necessary to have a .env file added to the project path or set system variables for OpenAI API keys.
The .env file follows this format:
```
OPENAI_API_KEY=<YOUR API KEY>
OPENAI_ORGANIZATION=<YOUR ORGANIZATION, IF YOU HAVE ONE>
```
## Running the Application
The application is run in the following way:
```shell
python3 main.py
```
// here maybe, among other things, explain the order in which those similar files are run

## Ontology
We created the initial version of the ontology using the **_Protégé_** tool. It contained only the classes *Dish* and *Ingredient*. The *ObjectProperty* relation *hasIngredient* is defined as transitive and its domain classes are *Dish* and *Ingredient*, and *range* Ingredient. This simple ontology is found in the file *empty_ontology_protege.rdf*.
Then, we inserted several well-known dishes and saved the created file under the name *dishes.rdf*.

The next step was to populate the ontology with ingredients of the already inserted dishes. For this purpose, we used the Python library **_wikipedia_**. It offers a simple function *summary(article, sentences)* for summarization. The first parameter is the name of the article on Wikipedia. The second is the number of sentences we want to use for summarization. In our case, we chose the value 3, as ingredients usually appear in the 3 most important sentences in articles about food on Wikipedia. Once we obtained a short representation of the article, it was necessary to extract data from that representation. This was achieved using the **UNI-NER** (*Universal Named Entity Recognition*) model. This is a smaller language model (7 billion parameters) intended for recognizing named entities. It works by passing it text and the name of the entity being extracted. In our case, the text passed was the summarized article, and the name of the entity being located was *"Ingredient"*. Image XX shows an example of how UNI-NER works:

![Image XX - Example of using UNI-NER](Uniner.png)
Image XX - Example of using UNI-NER

You can try UniNER at [this link](https://universal-ner.github.io/linku)

We did not have enough memory to run this model locally, so instead, we ran it on **_Google Colab_**. After extracting data about each dish from the list, we **recursively** called extraction functions on the obtained ingredients and repeated this process as long as there are data about ingredients. In this way, we obtained a graph of ingredients for each dish. By inserting this data into the existing ontology, we obtained the file *ingredients.rdf*.

After inserting data into the ontology, we realized that our ontology does not recognize synonyms. For example, ingredients *"sugar"*, *"sugars"*, and *"table sugar"* were recognized as different even though they represent the same ingredient. We initially tried to solve this problem using only the **_“word2vec”_** model, but it did not yield sufficiently good results. After that, we ran the **_BERT_** *sentence-transformer* for similarity calculation: *"paraphrase-multilingual-MiniLM-L12-v2"*. The recognized synonyms were saved in the file *bert_synonyms.csv*. However, these synonyms were not perfectly recognized, so we manually filtered them and entered them into the file *filtered_synonyms.csv*. Finally, we inserted these synonyms into the ontology in the file *with_synonyms.rdf*. We introduced a new transitive relation *hasSynonym*.

Considering that the data about dishes were mostly automatically generated and sometimes incomplete, we decided to thoroughly elaborate one type of food in the ontology. We chose pizza. We created a taxonomy of pizzas, and part of it is shown in Image XX:

![Image XX - Part of the pizza taxonomy](onto.png)

Image XX - Part of the pizza taxonomy

## Queries
Bearing in mind that the target demographic group of the application does not exist, as it is intended for everyone, it is necessary for its use to be as simple as possible. The classic way to interact with ontologies is using SPARQL queries, which require knowledge of rigid syntax and details of

 the ontology itself. Therefore, an abstraction layer was added in the form of a large language model that would generate SPARQL queries based on free text. Then, these queries would be executed over the RDF graph, and the query results would be interpreted by the large language model, to convert them into text suitable for the user.
An example of one of the queries would be:
```sparql
PREFIX ns1: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>

SELECT ?ingredient
WHERE {
   ns1:biryani ns1:hasIngredient ?ingredient .
}
```
The large language models used were GPT 4, GPT 3.5, and Code LLaMa. To run the Code LLaMa model, it is necessary to have the [Ollama](https://ollama.ai/) server running and the "codellama:7b-instruct" model downloaded.
For simplifying the data flow, the LangChain library was used for communicating with language models. Code LLaMa generally generates correct queries, however, it often adds comments at the beginning of the query.
For example, one of the standard errors would look like this:

```sparql
``Here is the query to get all the ingredients for biryani
PREFIX ns1: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>

SELECT ?ingredient
WHERE {
   ns1:biryani ns1:hasIngredient ?ingredient .
}
``
```

Such errors are relatively common and follow a similar format - added explanation or comment at the beginning of the query. To add a function to ```GraphSparqlQAChain``` that cleans unwanted characters from the beginning and end, we decided that the quickest solution would be to copy the original LangChain code into a separate file and implement added functionalities there, which is located within the ```sparql_chain.py``` file. The function for cleaning unwanted looks like this:

```python
def clean_sparql(sparql: str) -> str:
    """Clean SPARQL query."""
    sparql = sparql.replace("```", "")
    # remove anything until either SELECT or UPDATE
    sparql = sparql[max(sparql.find("SELECT"), sparql.find("UPDATE")) :]
    # remove anything after the last }
    sparql = sparql[: sparql.rfind("}") + 1]
    return sparql
```

It certainly contains an edge-case where, for example, the LLM's own comment contains the key words UPDATE or SELECT, which can be corrected with additional preprocessing. The best solution would be to have a query parser/validator, and each time call the LLM telling it to correct the errors that the validator returns.

## Application Interface

For building the interface of the described application, the [gradio](https://www.gradio.app/) library was used. Gradio is a library that enables rapid creation of simple interfaces, and its primary purpose is ML applications.
Our interface is shown in Image XX.

![Image XX - Interface appearance](UI.png)

## Authors
#### Pavle Glušac, R2 15/2023
#### Nevena Radešić, R2 2/2023
```
