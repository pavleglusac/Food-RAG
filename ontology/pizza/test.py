from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.plugins.sparql import prepareQuery

ontology_file_path = "../files/pizza.rdf"
g = Graph()
g.parse(ontology_file_path, format="xml")

food_ontology = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

sparql_query = """
    PREFIX food: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>

    SELECT ?subclass
    WHERE {
      ?subclass rdf:type owl:Class.
      ?subclass rdfs:subClassOf food:Pizza.
    }
"""

query = prepareQuery(sparql_query, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL, "food": food_ontology})
results = g.query(query)

print("Subclasses of Pizza:")
for row in results:
    print(row.subclass)
