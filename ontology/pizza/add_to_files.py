from rdflib import Graph, Namespace, RDF, OWL, RDFS

ontology_path = "../files/with_synonyms.rdf"
g = Graph()
g.parse(ontology_path, format="xml")

ns1 = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

g.add((ns1.VeganPizza, RDF.type, OWL.Class))
g.add((ns1.VeganPizza, RDFS.subClassOf, ns1.Pizza))

g.add((ns1.VegetarianPizza, RDF.type, OWL.Class))
g.add((ns1.VegetarianPizza, RDFS.subClassOf, ns1.Pizza))

g.add((ns1.CarnivorousPizza, RDF.type, OWL.Class))
g.add((ns1.CarnivorousPizza, RDFS.subClassOf, ns1.Pizza))

pizzas_and_ingredients = [
    (ns1.Focaccia, ns1.VeganPizza, ["dough", "olive_oil"]),
    (ns1.SpinachArtichokePizza, ns1.VeganPizza, ["dough", "spinach", "artichoke", "onion", "garlic", "olive_oil", "pepper"]),
    (ns1.HummusPizza, ns1.VeganPizza, ["dough", "hummus", "pepper", "broccoli"]),
    (ns1.TaccoPizza, ns1.VeganPizza, ["dough", "tomato", "beans", "corn", "olives", "onion"]),
    (ns1.BroccoliPizza, ns1.VeganPizza, ["dough", "broccoli", "lime", "garlic", "olive_oil"]),
    (ns1.GrilledVeggiePizza, ns1.VeganPizza, ["mushrooms", "zucchini", "pepper", "onion", "wine", "olive_oil", "tomato"]),

    (ns1.PizzaCaprese, ns1.VegetarianPizza, ["dough", "tomato_sauce", "oregano", "mozzarella", "tomato", "basil", "olive_oil"]),
    (ns1.PestoPizza, ns1.VegetarianPizza, ["dough", "basil", "parmesan", "mozzarella", "garlic", "olive_oil", "tomato"]),
    (ns1.TunaPizza, ns1.VegetarianPizza, ["dough", "tuna", "olive", "mushrooms", "corn", "cheese"]),
    (ns1.LoadedMexicanPizza, ns1.VegetarianPizza, ["dough", "beans", "onion", "garlic", "pepper", "chilli", "tomato", "cheddar", "spinach"]),
    (ns1.TomatoBaguettePizza, ns1.VegetarianPizza, ["baguette", "olive_oil", "mushrooms", "onion", "garlic", "mozzarella", "basil", "tomato"]),
    (ns1.Fungi, ns1.VegetarianPizza, ["dough", "tomato_sauce", "cheese", "mushrooms", "olive_oil", "garlic", "oregano"]),
    (ns1.Margheritta, ns1.VegetarianPizza, ["dough", "tomato_sauce", "olive_oil", "garlic", "oregano", "mozzarella"]),
    (ns1.GreekPitaPizza, ns1.VegetarianPizza, ["dough", "artichoke", "tomato", "olive", "parsley", "feta_cheese", "pita_bread"]),
    (ns1.EggplantFlatbreadPizza, ns1.VegetarianPizza, ["naan_flatbread", "eggplant", "garlic", "oregano", "tomato", "mozzarella", "parmesan"]),

    (ns1.Capriciossa, ns1.CarnivorousPizza, ["dough", "cheese", "tomato_sauce", "ham", "mushrooms"]),
    (ns1.Hawaii, ns1.CarnivorousPizza, ["dough", "cheese", "ham", "pineapple"]),
    (ns1.Mediteranea, ns1.CarnivorousPizza, ["dough", "tomato_sauce", "onion", "seafood", "olive", "mushrooms"]),
    (ns1.Fiorentina, ns1.CarnivorousPizza, ["dough", "egg", "ham", "cheese", "ham", "tomato_sauce", "spinach"]),
    (ns1.Carbonara, ns1.CarnivorousPizza, ["dough", "sour_cream", "garlic", "cheese", "ham", "egg"]),
    (ns1.HungarianPizza, ns1.CarnivorousPizza, ["dough", "cheese", "sausage", "tomato_sauce", "ham"]),
    (ns1.Diavola, ns1.CarnivorousPizza, ["dough", "tomato_sauce", "mozzarella", "spicy_salami", "chili", "olive_oil"]),
    (ns1.Pepperoni, ns1.CarnivorousPizza, ["dough", "tomato_sauce", "cheese", "sausage", "chili"]),
    (ns1.BBQChickenPizza, ns1.CarnivorousPizza, ["dough", "barbeque_sauce", "chicken_breasts", "pepper", "onion", "cheese", "cilantro"]),
]

for pizza, pizza_class, ingredients in pizzas_and_ingredients:
    g.add((pizza, RDF.type, pizza_class))
    for ingredient in ingredients:
        g.add((pizza, ns1.hasIngredient, ns1[ingredient.replace(" ", "_")]))

g.serialize(destination="../files/pizza.rdf", format="xml")
