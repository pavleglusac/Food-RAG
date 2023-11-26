from langchain.llms import Ollama
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import ConversationChain


llm = Ollama(temperature=0)


def chatbot_function(message):
    return llm(message)


user_input = """
Biryani (/bɜːrˈjɑːni/) is a mixed rice dish originating among the Muslims of South Asia. It is made with rice, some type of meat (chicken, beef, goat, lamb, prawn, or fish) and spices. To cater to vegetarians, in some cases it is prepared without any meat, substituting vegetables for the meat.[1] Sometimes eggs and/or potatoes, are added.[2]
Biryani is one of the most popular dishes in South Asia, as well as among the diaspora from the region. Similar dishes are also prepared in other parts of the world such as in Iraq, Myanmar, Thailand, and Malaysia.[3] Biryani is the single most-ordered dish on Indian online food ordering and delivery services, and has been labelled as the most popular dish overall in India.[4][5] 
"""


user_prompt = """ 
    You are a semantic information extractor for food.
    All you can do is read  the information which the user sends you, and return a list of triples in format (subject, predicate, object).
    The triples should have information on specific dishes.
    Reply ONLY with triples in the format (subject, predicate, object).
    Do not reply with anything else.

    Example:
    # Pizza (English: /ˈpiːtsə/ PEET-sə, Italian: [ˈpittsa], Neapolitan: [ˈpittsə]) is a dish of Italian origin consisting of a usually round, flat base of leavened wheat-based dough topped with tomatoes, cheese, and often various other ingredients (such as various types of sausage, anchovies, mushrooms, onions, olives, vegetables, meat, ham, etc.), which is then baked at a high temperature, traditionally in a wood-fired oven.[1] 
    (pizza,origin,Italy)
    (pizza,ingredients,tomatoes)
    (pizza,ingredients,cheese)
    (pizza,ingredients,sausage)
    (pizza,ingredients,mushrooms)
    ...


    User:
    Biryani (/bɜːrˈjɑːni/) is a mixed rice dish originating among the Muslims of South Asia. It is made with rice, some type of meat (chicken, beef, goat, lamb, prawn, or fish) and spices. To cater to vegetarians, in some cases it is prepared without any meat, substituting vegetables for the meat.[1] Sometimes eggs and/or potatoes, are added.[2]
    Biryani is one of the most popular dishes in South Asia, as well as among the diaspora from the region. Similar dishes are also prepared in other parts of the world such as in Iraq, Myanmar, Thailand, and Malaysia.[3] Biryani is the single most-ordered dish on Indian online food ordering and delivery services, and has been labelled as the most popular dish overall in India.[4][5] 
"""


print(llm(user_prompt))
