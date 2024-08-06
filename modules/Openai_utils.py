#%%
import openai
from openai import OpenAI
#%%
# api_key
client = OpenAI(api_key="sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0")
#%%
# exampling with word and definition
def exampling_definition(word: str, definition: str) -> str:

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"다음 정의를 금융소비자가 해당 단어를 사용할만한 예시 상황을 최대 5문장 안으로 간단하게 말해주세요. : \n\n단어 : {word}, \n\n정의: {definition}\n\n예시상황:"}
    ]


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # model(gpt4 가능)
        messages=messages,
        max_tokens=500,
        temperature=0.1
    )
    example = response.choices[0].message.content.strip()
    return example

#%%
# changing answer(response -> simplify answer)
def simplify_definition(definition: str) -> str:

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"다음 정의를 금융소비자가 해당 단어를 모른다고 생각했을 때 그 사람이 이해하기 쉽고 너무 길지 않으며 어려운 단어들이 없도록 정의를 재생성해 주세요. 이때 단어를 말해주고 문장을 시작해주세요.:\n\n정의: {definition}\n\n재작성된 정의:"}
    ]


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # model(gpt4 가능)
        messages=messages,
        max_tokens=200,
        temperature=0.1
    )
    simplified_definition = response.choices[0].message.content.strip()
    return simplified_definition

#%%
# exampling with word and definition
def exampling_definition(word: str, definition: str) -> str:

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"다음 정의를 금융소비자가 해당 단어를 사용할만한 예시 상황을 최대 5문장 안으로 간단하게 말해주세요. : \n\n단어 : {word}, \n\n정의: {definition}\n\n예시상황:"}
    ]


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # model(gpt4 가능)
        messages=messages,
        max_tokens=500,
        temperature=0.1
    )
    example = response.choices[0].message.content.strip()
    return example
# %%
def product_cleaning(top_k_sentence: str) -> str:

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"다음 {top_k_sentence} 과 같은 금융상품이 있습니다. 이것의 상품분류와 상품이름 상품특징을 itemwise하여 각각 한줄로 정리해주세요."}
    ]


    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # model(gpt4 가능)
        messages=messages,
        max_tokens=200,
        temperature=0.1
    )
    product = response.choices[0].message.content.strip()
    return product