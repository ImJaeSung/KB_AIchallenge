#%%
import openai
from openai import OpenAI
#%%
# api_key
# client = OpenAI(api_key="sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0")
#%%
# exampling with word and definition
def exampling_definition(openai_info:list, word: str, definition: str) -> str:
    client = OpenAI(api_key=openai_info[0])

    prompt = """
    Please generate an appropriate response to the given requirements and instructions.\n
    Requirements and Instructions : \n
    1. Give an example situation where a financial consumer would use the financial word in korean. \n
    2. Be brief, with a maximum of 5 sentences.
    3. Facts must not be changed. \n
    4. Be polite, please. \n
    """+ f'\Word: {word}\n' + f'\nDefintion: {definition}\n' + 'Situation: \n'

    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant that explains financial terms to people who have trouble understanding them in korean."
        },
        {
            "role": "user", 
            "content": prompt
        }
    ]


    response = client.chat.completions.create(
        model=openai_info[1],  # model(gpt4 가능)
        messages=messages,
        max_tokens=500,
        temperature=0.5
    )
    example = response.choices[0].message.content.strip()
    return example

#%%
# changing answer(response -> simplify answer)
def simplify_definition(openai_info:list, word, definition: str) -> str:
    client = OpenAI(api_key=openai_info[0])
    
    prompt = """
    Please generate an appropriate response to the given requirements and instructions.\n
    Requirements and Instructions : \n
    1. You must explain the financial term to people who have trouble understanding them in korean. \n
    2. If you think a financial consumer does not know the following definition,
        you should rewrite the definition so that it is easy for the person to understand, not too long, and free of difficult words.  \n
    3. The given financial term must be included in the corresponding explanation. \n
    4. The given financial term should be included in your reponse.
    5. Facts must not be changed. \n
    6. Be polite, please.\n
    """+ f'\Word: {word}\n' + f'\nDefintion: {definition}\n' + 'Rewritten Definition: \n'

    messages = [
        {
            "role": "system", 
            "content": "You're a helpful assistant that explains financial terms to people who have trouble understanding them in korean."
        },
        {
            "role": "user", 
            "content": prompt}
    ]

    response = client.chat.completions.create(
        model=openai_info[1],  # model(gpt4 가능)
        messages=messages,
        max_tokens=200,
        temperature=0.5
    )
    simplified_definition = response.choices[0].message.content.strip()
    return simplified_definition

# %%
def product_cleaning(openai_info, best_product: str) -> str:
    client = OpenAI(api_key=openai_info[0])

    prompt = """
    Please generate an appropriate response to the given requirements and instructions.\n
    Requirements and Instructions : \n
    1. When given the product information, please summarize the - product category, - product name, and - product features 
        in the form of itemwise using dash(-) into one line each in korean. \n
    2. Facts must not be changed. \n
    3. Be polite, please. \n
    """+ f'\Financial product information: {best_product}\n' + 'Rewritten Financial product information: \n'

    messages = [
        {
            "role": "system", 
            "content": "You are a helpful assistant that explain financial product in korean."},
        {
            "role": "user", 
            "content": prompt
        }
    ]


    response = client.chat.completions.create(
        model=openai_info[1],  # model(gpt4 가능)
        messages=messages,
        max_tokens=200,
        temperature=0.5
    )
    product = response.choices[0].message.content.strip()
    return product