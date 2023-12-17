# !pip install -q transformers einops accelerate langchain bitsandbytes
# !pip install sentencepiece
# !pip install wikipedia

##############################################################
from langchain import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM
import transformers
import torch
from langchain import PromptTemplate,  LLMChain
import locale
import wikipedia

model = "Universal-NER/UniNER-7B-all"

tokenizer = AutoTokenizer.from_pretrained(model)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,
    max_length=1000,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)

llm = HuggingFacePipeline(pipeline = pipeline, model_kwargs = {'temperature':0})

template = """
              A virtual assistant answers questions from a user based on the provided text.
              USER: Text: {input_text}
              ASSISTANT: I’ve read this text.
              USER: What describes {entity_type} in the text?
              ASSISTANT:
           """

prompt = PromptTemplate(template=template, input_variables=["input_text","entity_type"])

llm_chain = LLMChain(prompt=prompt, llm=llm)

def getpreferredencoding(do_setlocale = True):
    return "UTF-8"
locale.getpreferredencoding = getpreferredencoding

entity_type="ingredient"


def get_ingredients(dish):
    try:
        ingredients = llm_chain.run({"input_text": wikipedia.summary(dish, sentences=3), "entity_type": entity_type})
        return ingredients
    except:
        return []


def insert_if_not_in_dict(sastojci, dishes, my_dict):
    dishes.extend([sastojak for sastojak in eval(sastojci) if sastojak not in my_dict])
    return dishes



def find_all_ingredients(dishes, dict):
    if len(dishes) == 0:
        return [], dict
    dish = dishes[0]
    sastojci = get_ingredients(dish)
    # print('dict', dict)
    # print('dishes', dishes)
    dishes.remove(dish)
    dishes, dict = find_all_ingredients(dishes, dict)
    if len(sastojci) > 0:
        dict[dish] = sastojci
        dishes = insert_if_not_in_dict(sastojci, dishes, dict)
    return dishes, dict,


dishes = [
            "Bolognese sauce",
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
            "Verhackert",
            "cheesecake",
            "caesar salad",
            "pancakes",
            "tiramisu",
            "goulash"
]

dict = {}
_, ingredient_dict = find_all_ingredients(dishes, dict)
ingredient_dict = {key.lower(): value.lower() if isinstance(value, str) else value for key, value in ingredient_dict.items()}
print(ingredient_dict)
'''
povratna vrijednost ovoga je 
{'chicken curry': ' ["onion", "tomato", "ginger", "garlic", "tomato puree", "chilli peppers", "turmeric", "cumin", "coriander", "cinnamon", "cardamom"]', 'ice cream': ' ["milk", "cream", "sweetener", "sugar", "alternative", "spice", "cocoa", "vanilla", "fruit", "stabilizers"]', 'moussaka': ' ["eggplant", "potato", "ground meat", "egg", "flour"]', 'kimchi': ' ["gochugaru", "spring onions", "garlic", "ginger", "jeotgal"]', 'sashimi': ' ["soy sauce"]', 'nachos': ' ["corn-", "wheat-based", "beef", "pork", "chicken", "seafood", "vegetables", "chesse"]', 'jambalaya': ' ["sausage", "pork", "chicken", "seafood", "crawfish", "shrimp", "onion", "celery", "green bell pepper", "okra", "carrots", "tomatoes", "corn", "chilis", "garlic"]', 'biryani': ' ["rice", "meat", "chicken", "beef", "goat", "lamb", "prawn", "fish", "spices", "vegetables"]', 'cordon bleu (dish)': ' ["meat", "cheese", "pork", "ham", "chicken"]', 'baklava': ' ["filo pastry", "nuts"]', 'verhackert': ' ["chopped bacon", "minced garlic", "salt", "sugar"]', 'cheesecake': ' ["cheese", "eggs", "sugar", "crushed cookies", "graham crackers", "pastry", "sponge cake"]', 'caesar salad': ' ["romaine lettuce", "lemon juice", "olive oil", "egg", "worcestershire sauce", "anchovies", "garlic", "dijon mustard", "parmesan cheese", "black pepper"]', 'pancakes': ' ["starch-based batter", "eggs", "milk", "butter", "oil"]', 'tiramisu': ' ["ladyfingers", "savoiardi", "coffee", "eggs", "sugar", "mascarpone", "cocoa"]', 'goulash': ' ["paprika"]', 'tomato puree': ' ["tomatoes"]', 'chilli peppers': ' []', 'cumin': ' []', 'coriander': ' []', 'cinnamon': ' []', 'cardamom': ' ["cardamom", "cardamon", "cardamum"]', 'cream': ' []', 'sweetener': ' []', 'sugar': ' ["sugar", "glucose", "fructose", "galactose", "sucrose", "lactose", "maltose"]', 'spice': ' []', 'vanilla': ' []', 'fruit': ' []', 'eggplant': ' []', 'potato': ' []', 'egg': ' []', 'gochugaru': ' []', 
'spring onions': ' ["allium", "garlic", "shallot", "leek", "chive", "chinese onions"]', 'jeotgal': ' []', 'soy sauce': ' ["soybeans", "roasted grain", "brine", "aspergillus oryzae", "aspergillus sojae molds"]', 'corn-': ' []', 'wheat-based': ' ["wheat", "barley malt"]', 'beef': ' []', 'seafood': ' []', 'vegetables': ' []', 'chesse': ' ["proteins", "fat", "milk", "enzymes", "rennet", "bacterial enzymes"]', 'sausage': ' ["ground meat", "salt", "spices", "flavourings", "grains", "breadcrumbs"]', 'crawfish': ' []', 'shrimp': ' []', 'celery': ' []', 'green bell pepper': ' []', 'tomatoes': ' []', 'rice': ' []', 'goat': ' []', 'fish': ' []', 'cheese': ' []', 'filo pastry': ' ["oil", "butter"]', 'minced garlic': ' []', 'salt': ' []', 'eggs': ' []', 'graham crackers': ' ["graham flour"]', 'pastry': ' ["flour", "water", "shortening", "butter", "lard", "sugar", "milk", "baking powder", "eggs"]', 'romaine lettuce': ' ["romaine", "cos lettuce", "lactuca sativa l. var. longifolia", "lettuce"]', 'lemon juice': ' []', 'worcestershire sauce': ' []', 'anchovies': ' []', 'dijon mustard': ' ["vinegar", "verjuice", "unripe grapes", "mustard seeds", "white wine", "water", "salt"]', 'parmesan cheese': ' ["cows\' milk"]', 'oil': ' []', 'ladyfingers': ' ["egg"]', 'savoiardi': ' ["egg", "sugar syrup", "liqueur", "coffee", "espresso"]', 'coffee': ' ["roasted coffee beans", "caffeine", "coffea plant\'s fruits", "unroasted green coffee beans"]', 'mascarpone': ' ["cream", "whey"]', 'paprika': ' ["capsicum annuum varietals", "chili peppers"]', 'cilantro': ' []', 'essential oil': ' []', 'cinnamaldehyde': ' []', 'glucose': ' []', 'fructose': ' []', 'galactose': ' []', 'lactose': ' []', 'allium': ' []', 'shallot': ' []', 'leek': ' []', 'chive': ' []', 
'chinese onions': ' []', 'soybeans': ' []', 'roasted grain': ' []', 'brine': ' []', 'aspergillus oryzae': ' []', 'aspergillus sojae molds': ' ["water", "salt"]', 'barley malt': ' ["sugar", "maltodextrines"]', 'proteins': ' []', 'fat': ' []', 'enzymes': ' []', 'bacterial enzymes': ' []', 'flavourings': ' ["sugars"]', 'grains': ' []', 'breadcrumbs': ' ["bread", "dry breads"]', 'shortening': ' ["shortening", "fat", "lard"]', 'lard': ' []', 'cos lettuce': ' []', 'vinegar': ' ["wine"]', 'verjuice': ' ["unripe grapes", "crab-apples", "herbs", "spices"]', 'mustard seeds': ' ["mustard seeds"]', "cows' milk": ' []', 'hydrocarbons': ' []', 'sugar syrup': ' ["inverted sugar syrup", "invert syrup", "invert sugar", "simple syrup", "sugar syrup", "sugar water", "bar syrup", "sucrose inversion", "table sugar"]', 'liqueur': ' ["grains", "fruits", "vegetables", "sugar"]', 'espresso': ' []', 'roasted coffee beans': ' ["coffee bean", "fruit", "pip", "coffee cherry", "cherry"]', 'unroasted green coffee beans': ' ["coffee bean", "pip"]', 'whey': ' []', 'capsicum annuum': ' ["paprika", "chili pepper", "jalape\\u00f1o", "cayenne", "bell pepper"]', 'chili peppers': ' []', 'cardamon': ' ["elettaria", "amomum"]', 'cardamum': ' ["cardamom"]', 'maltodextrines': ' ["maltodextrin"]', 'sugars': ' []', 'bread': ' []', 'wine': ' []', 'crab-apples': ' []', 'herbs': ' []', 'inverted sugar syrup': ' ["inverted sugar syrup", "invert syrup", "invert sugar", "simple syrup", "sugar syrup", "sugar water", "bar syrup", "sucrose inversion", "sucrose", "table sugar"]', 'invert syrup': ' ["inverted sugar syrup", "invert syrup", "invert sugar", "simple syrup", "sugar syrup", "sugar water", "bar syrup", "sucrose inversion", "sucrose", "table sugar"]', 'invert sugar': ' ["invert sugar"]', 
'simple syrup': ' ["inverted sugar syrup", "invert syrup", "invert sugar", "simple syrup", "sugar syrup", "sugar water", "bar syrup", "sucrose inversion", "glucose", "fructose", "table sugar"]', 'sugar water': ' ["inverted sugar syrup", "invert syrup", "invert sugar", "simple syrup", "sugar syrup", "sugar water", "bar syrup", "sucrose inversion", "sucrose", "table sugar"]', 'bar syrup': ' ["inverted sugar syrup", "invert syrup", "invert sugar", "simple syrup", "sugar syrup", "sugar water", "bar syrup", "sucrose inversion", "sucrose", "table sugar"]', 'sucrose inversion': ' ["sucrose", "table sugar"]', 'table sugar': ' ["molasses", "sucrose"]', 'fruits': ' []', 'caffeine': ' []', "coffea plant's fruits": ' ["coffee beans"]', 'coffee bean': ' ["coffee bean"]', 'chili pepper': ' ["capsaicin"]', 'jalapeño': ' []', 'cayenne': ' []', 'capsaicin': ' ["capsaicin", "capsaicinoids"]', 'capsaicinoids': ' []', 'elettaria': ' []', 'amomum': ' []', 'maltodextrin': ' ["maltodextrin"]', 'molasses': ' []', 'coffee cherry': ' []', 'cherry': ' []', 'coffee beans': ' ["coffee bean", "pip"]', '8-methyl-n-vanillyl-6-nonenamide': ' []', 'monosaccharides': ' ["monosaccharides", "simple sugars", "carbohydrates"]', 'disaccharide sucrose': ' []', 'sugarcane molasses': ' ["molasses"]', 'berries': ' []', 'simple sugars': ' []', 'carbohydrates': ' []', 'sugarcane': ' ["sucrose"]', 'sugar beet juice': ' ["sucrose"]'}
'''




