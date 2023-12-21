from rdflib import Graph

# Specify the path to the OWL file
owl_file_path = "/mnt/ACA058A9A0587C30/Faks/Master/Food-RAG/ontology/files/ingredients.rdf"

# Create a new RDF graph
graph = Graph()

# Parse the OWL file into the graph
graph.parse(owl_file_path, format="xml")

# Now you can work with the parsed graph
# For example, you can iterate over the triples in the graph
# for subject, predicate, object in graph:
#     print(subject, predicate, object)


# ask a sparql query
query = """
PREFIX ns1: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>
SELECT ?ingredient
WHERE {
ns1:biryani ns1:hasIngredient ?ingredient .
}
"""

# Execute the query 
results = graph.query(query)
# show the results
for row in results:
    print(row)