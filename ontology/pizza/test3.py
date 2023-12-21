from rdflib import Graph, Namespace, RDF, RDFS, OWL
from rdflib.plugins.sparql import prepareQuery

ontology_file_path = "extended_pizza.rdf"
g = Graph()
g.parse(ontology_file_path, format="xml")

food_ontology = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

# Check if "Pepperoni" is a class or individual
sparql_query_pepperoni = f"""
    PREFIX food: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>

    SELECT ?type
    WHERE {{
      food:Pepperoni rdf:type ?type.
    }}
"""

query_pepperoni = prepareQuery(sparql_query_pepperoni, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL, "food": food_ontology})
results_pepperoni = g.query(query_pepperoni)

print("Type of Pepperoni:")
for row in results_pepperoni:
    print(f"Pepperoni is a: {row.type}")

# Check if "VeganPizza" is a class or individual
sparql_query_vegan_pizza = f"""
    PREFIX food: <http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#>

    SELECT ?type
    WHERE {{
      food:VeganPizza rdf:type ?type.
    }}
"""

query_vegan_pizza = prepareQuery(sparql_query_vegan_pizza, initNs={"rdf": RDF, "rdfs": RDFS, "owl": OWL, "food": food_ontology})
results_vegan_pizza = g.query(query_vegan_pizza)

print("Type of VeganPizza:")
for row in results_vegan_pizza:
    print(f"VeganPizza is a: {row.type}")
