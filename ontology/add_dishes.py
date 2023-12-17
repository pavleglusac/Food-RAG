from rdflib import Graph, URIRef, Namespace, RDF, OWL

ontology_file_path = "files\\empty_ontology_protege.rdf"
g = Graph()
g.parse(ontology_file_path, format="xml")

food_ontology = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

dishes = [
    "bolognese sauce",
    "chicken curry",
    "ice cream",
    "moussaka",
    "kimchi",
    "sashimi",
    "nachos",
    "sushi",
    "jambalaya",
    "biryani",
    "cordon bleu (dish)",
    "baklava",
    "verhackert",
    "cheesecake",
    "caesar salad",
    "pancakes",
    "tiramisu",
    "goulash"
]

for dish in dishes:
    dish_individual = food_ontology[dish.replace(" ", "_").lower()]
    g.add((dish_individual, RDF.type, food_ontology.Dish))

g.serialize(destination="files\\dishes.rdf", format="xml")
