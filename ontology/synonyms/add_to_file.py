from rdflib import Graph, Namespace, RDF, OWL

ontology_path = "../files/ingredients.rdf"
g = Graph()
g.parse(ontology_path, format="xml")

ns1 = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

has_synonym = ns1.hasSynonym
transitive_axiom = (has_synonym, RDF.type, OWL.TransitiveProperty)
g.add(transitive_axiom)

csv_file_path = "../files/filtered_synonyms.csv"

with open(csv_file_path, "r") as file:
    lines = file.readlines()

synonyms = [line.strip().split(",") for line in lines if line.strip()]

for synonym_pair in synonyms:
    term1, term2 = synonym_pair
    term1_uri = ns1[term1.replace(" ", "_")]
    term2_uri = ns1[term2.replace(" ", "_")]

    g.add((term1_uri, has_synonym, term2_uri))
    g.add((term2_uri, has_synonym, term1_uri))

g.serialize(destination="../files/with_synonyms.rdf", format="xml")
