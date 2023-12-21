from rdflib import Graph, Namespace, RDF

ontology_path = "../files/with_synonyms.rdf"
g = Graph()
g.parse(ontology_path, format="xml")

ns1 = Namespace("http://www.semanticweb.org/nevena/ontologies/2023/11/food_ontology.owl#")

g.add((ns1.Pizza, RDF.type, ns1.Dish))
g.add((ns1.VeganPizza, RDF.type, ns1.Pizza))
g.add((ns1.VegetarianPizza, RDF.type, ns1.Pizza))
g.add((ns1.CarnivorousPizza, RDF.type, ns1.Pizza))


vegan_pizzas = [
    (ns1.Focaccia, ["dough", "olive_oil"]),
    (ns1.SpinachArtichokePizza, ["dough", "spinach", "artichoke", "onion", "garlic", "olive_oil", "pepper"]),
    (ns1.HummusPizza, ["dough", "hummus", "pepper", "broccoli"]),
    (ns1.TaccoPizza, ["dough", "tomato", "beans", "corn", "olives", "onion"]),
    (ns1.BroccoliPizza, ["dough", "broccoli", "lime", "garlic", "olive_oil"]),
    (ns1.GrilledVeggiePizza, ["mushrooms", "zucchini", "pepper", "onion", "wine", "olive_oil", "tomato"]),
]

for pizza, ingredients in vegan_pizzas:
    g.add((pizza, RDF.type, ns1.VeganPizza))
    for ingredient in ingredients:
        g.add((pizza, ns1.hasIngredient, ns1[ingredient.replace(" ", "_")]))

vegetarian_pizzas = [
    (ns1.PizzaCaprese, ["dough", "tomato_sauce", "oregano", "mozzarella", "tomato", "basil", "olive_oil"]),
    (ns1.PestoPizza, ["dough", "basil", "parmesan", "mozzarella", "garlic", "olive_oil", "tomato"]),
    (ns1.TunaPizza, ["dough", "tuna", "olive", "mushrooms", "corn", "cheese"]),
    (ns1.LoadedMexicanPizza, ["dough", "beans", "onion", "garlic", "pepper", "chilli", "tomato", "cheddar", "spinach"]),
    (ns1.TomatoBaguettePizza, ["baguette", "olive_oil", "mushrooms", "onion", "garlic", "mozzarella", "basil", "tomato"]),
    (ns1.Fungi, ["dough", "tomato_sauce", "cheese", "mushrooms", "olive_oil", "garlic", "oregano"]),
    (ns1.Margheritta, ["dough", "tomato_sauce", "olive_oil", "garlic", "oregano", "mozzarella"]),
    (ns1.GreekPitaPizza, ["dough", "artichoke", "tomato", "olive", "parsley", "feta_cheese", "pita_bread"]),
    (ns1.EggplantFlatbreadPizza, ["naan_flatbread", "eggplant", "garlic", "oregano", "tomato", "mozzarella", "parmesan"]),
]

for pizza, ingredients in vegetarian_pizzas:
    g.add((pizza, RDF.type, ns1.VegetarianPizza))
    for ingredient in ingredients:
        g.add((pizza, ns1.hasIngredient, ns1[ingredient.replace(" ", "_")]))

carnivorous_pizzas = [
    (ns1.Capriciossa, ["dough", "cheese", "tomato_sauce", "ham", "mushrooms"]),
    (ns1.Hawaii, ["dough", "cheese", "ham", "pineapple"]),
    (ns1.Mediteranea, ["dough", "tomato_sauce", "onion", "seafood", "olive", "mushrooms"]),
    (ns1.Fiorentina, ["dough", "egg", "ham", "cheese", "ham", "tomato_sauce", "spinach"]),
    (ns1.Carbonara, ["dough", "sour_cream", "garlic", "cheese", "ham", "egg"]),
    (ns1.HungarianPizza, ["dough", "cheese", "sausage", "tomato_sauce", "ham"]),
    (ns1.Diavola, ["dough", "tomato_sauce", "mozzarella", "spicy_salami", "chili", "olive_oil"]),
    (ns1.Pepperoni, ["dough", "tomato_sauce", "cheese", "sausage", "chili"]),
    (ns1.BBQChickenPizza, ["dough", "barbeque_sauce", "chicken_breasts", "pepper", "onion", "cheese", "cilantro"]),
]
for pizza, ingredients in carnivorous_pizzas:
    g.add((pizza, RDF.type, ns1.CarnivorousPizza))
    for ingredient in ingredients:
        g.add((pizza, ns1.hasIngredient, ns1[ingredient.replace(" ", "_")]))

g.serialize(destination="../files/pizza.rdf", format="xml")
