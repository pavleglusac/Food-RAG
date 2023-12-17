from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.plugins.sparql import prepareQuery

ontology_file_path = "files\\ingredients.rdf"
g = Graph()
g.parse(ontology_file_path, format="xml")

food_ontology = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")


# sa + i bez
sparql_query = """
    PREFIX food: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>
    
    SELECT ?ingredient
    WHERE {
      food:ice_cream food:hasIngredient+ ?ingredient.
    }
"""

query = prepareQuery(sparql_query, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL, "food": food_ontology})
results = g.query(query)

print("Dishes and their ingredients:")
for row in results:
    print(row)
