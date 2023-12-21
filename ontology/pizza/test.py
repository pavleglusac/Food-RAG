from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.plugins.sparql import prepareQuery

ontology_file_path = "../files/pizza.rdf"
g = Graph()
g.parse(ontology_file_path, format="xml")

food_ontology = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

sparql_query = """
    PREFIX food: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>

    SELECT ?subclass ?individual
    WHERE {
      ?subclass rdf:type/rdfs:subClassOf* food:Pizza.
      ?individual rdf:type ?subclass.
    }
"""

query = prepareQuery(sparql_query, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL, "food": food_ontology})
results = g.query(query)

current_subclass = None
print("Instances of Pizza Subclasses:")
for row in results:
    if current_subclass != row.subclass:
        if current_subclass is not None:
            print()  # Separate output for each subclass
        print(f"Subclass: {row.subclass}")
        current_subclass = row.subclass
    print(f"  Individual: {row.individual}")
