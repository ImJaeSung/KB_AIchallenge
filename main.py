# %%
import random
import argparse
import json
import os
import pandas as pd
import numpy as np
from typing import Optional
from pydantic import BaseModel

# %%
## langchain
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.text_splitter import CharacterTextSplitter

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# %%
# our modules
from modules import Cosine_Similarity, Web_Research
from modules.Embedding import get_embedder
from modules.Openai_utils import exampling_definition, simplify_definition, product_cleaning
from modules.utils import TextProcessor, postprocessing, set_random_seed  
from modules.recommender import topK_product_rec, best_product_rec 

# %%
def get_args(debug):
    parser = argparse.ArgumentParser('parameters')

    parser.add_argument("--seed", type=int, default=0, 
                        help="seed for repeatable results")

    parser.add_argument('--embedding_type', type=str, default='openai',
                        help='embedding type (options: openai, huggingface)')
    
    parser.add_argument('--gpt_ver', type=str, default='gpt4',
                        help='gpt prompt model (options: gpt4, gpt3.5)')
    
    parser.add_argument('--threshold', type=float, default=0.9,
                        help='consine similarity threshold between question and word')
    
    parser.add_argument(
        "--question",
        type=str,
        nargs="?",
        help="the question your finanical term"
    )

    if debug:
        return parser.parse_args(args=[])
    else:
        return parser.parse_args()

# %%
def getAiAnswer(df, question):
    # %%
    print(f"Question: {question}")
    config = vars(get_args(debug=False))

    set_random_seed(config["seed"])
    
    # base
    web_word = None
    web_definition = None
    web_link = None
    ret_word = None
    ret_definition = None
    ret_score = None
    data_dir = './assets'
    
    if config["gpt_ver"] == "gpt4":
        openai_api_key = "xxx" # put your OpenAI key for GPT-4
        openai_model = "gpt-4"
    elif config["gpt_ver"] == "gpt3.5":
        openai_api_key = "xxx" # put your OpenAI key for GPT-3.5
        openai_model = "gpt-3.5-turbo"

    openai_info = [openai_api_key, openai_model]
    # %%
    """question embedding"""
    embedder = get_embedder(
        embedding_type=config["embedding_type"], api_key=openai_api_key
    )
    embedding_q = embedder.embed([question])

    # Cosine simliarity with DB -> result  
    print("KB DB와 유사도 결과 비교\n")

    cosine = Cosine_Similarity.CosineSimilarityCalculator(
        threshold=config["threshold"]
    )
    result = cosine.calculate_similarity(embedding_q, df)
    #%%
    """generating answer"""
    
    if result == '해당 단어에 대한 정의가 사전에 정의되어있지 않습니다. 외부 검색 결과로 알려드리겠습니다.':
        
        print("KB DB 내에 해당 단어의 정보가 없음...\n")
        
        query = question
        web_research = Web_Research.WebResearch()
        _, links_blog = web_research.get_blog_links(query)
        contents_blog = web_research.get_blog_contents(links_blog)

        _, links_dict = web_research.get_dict_links(query)
        contents_dict = web_research.get_dict_contents(links_dict)

        contents = contents_blog + contents_dict
        links = links_blog + links_dict

        # Document class
        class Document(BaseModel):
            page_content: str
            metadata: Optional[dict] = None

        # text splitting
        text_splitter = CharacterTextSplitter(
            separator=' ',
            chunk_size=400,
            chunk_overlap=200,
            length_function=len,
        )

        text_list = []
        link_list = []

        for content, link in zip(contents, links):
            text = text_splitter.split_text(content)
            text_list.extend(text)
            link_list.extend([link] * len(text))

        docs_objects = [Document(
            page_content=text, metadata={"source": link}
        ) for text, link in zip(text_list, link_list)
        ]

        # openai embedding model
        embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

        # faiss vectorstore
        vectorstore = FAISS.from_documents(
            docs_objects,
            embedding=embeddings_model,
            distance_strategy=DistanceStrategy.COSINE
        )

        print("외부 retriver를 통한 vectorstore 생성...\n")

        # web_retriever
        retriever = vectorstore.as_retriever(
            search_type='mmr',
            search_kwargs={'k': 5, 'lambda_mult': 0.5}
        )

        docs = retriever.invoke(query)
        docs_link = docs[0].metadata['source']

        # Prompt
        template = '''Answer the question based only on the following context:
        {context}

        Question: {question}

        Please speak politely.
        '''

        prompt = ChatPromptTemplate.from_template(template)

        # Model
        llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model='gpt-3.5-turbo',
            temperature=0,
            max_tokens=500,
        )

        def format_docs(docs):
            return '\n\n'.join([d.page_content for d in docs])

        # Chain
        chain = prompt | llm | StrOutputParser()

        # Run
        text_processor = TextProcessor()
        web_word = text_processor.extract_first_noun_phrase(query)
        web_definition = chain.invoke(
            {'context': (format_docs(docs)), 'question': query}
        )
        web_link = docs_link
        embedding_word = embedder.embed([web_word])

        new_df = pd.DataFrame(
            {'word': web_word, 'definition': web_definition, 'embedding': embedding_word}
        )

        # updating new definition
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        new_df.to_csv(f'{data_dir}/data_{web_word}.csv', index=False)


    else:
        print("DB 내 단어 정보 생성...\n")
        ret_word = result['word']
        ret_definition = result['definition']
        ret_score = result['score']

    # %%
    word = ret_word if ret_word is not None else web_word
    definition = ret_definition if ret_definition is not None else web_definition
    plus_info = ret_score if ret_score is not None else web_link  # DB: similarity score, WEB: source link

    """simplify the answer"""
    definition_gen = simplify_definition(openai_info, word, definition)
    exampling_gen = exampling_definition(openai_info, word, definition)

    #%%
    """Mydata"""
    with open(f'{data_dir}/textual_mydata.json', 'r', encoding='utf-8') as jsonfile:
        textual_mydata = json.load(jsonfile) # import my data

    definition_first = postprocessing(definition)

    mydata = random.choice(textual_mydata)
    print(f'People: {mydata} \n')
    
    full_query = mydata + " " + question + " " + definition_first
    #%%
    """recommed the product"""
    with open(f'{data_dir}/textual_product.json', 'r', encoding='utf-8') as jsonfile:
        textual_data = json.load(jsonfile) # import KB product information
    
    textual_embedding = np.load(f'{data_dir}/textual_product.npy')
    topk_product, _ = topK_product_rec(
        full_query, textual_data, textual_embedding, k=5
    )
    #%%
    """BM25"""
    best_product, _ = best_product_rec(topk_product, full_query)
    recommend_product = product_cleaning(openai_info, best_product)
    #%%
    """Final answer"""
    if plus_info == ret_score:
        answer = f'1. 단어 정의\n{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.\n{definition_gen}\n해당 단어의 정의는 {plus_info:.4f}의 저희 dictionary 상에서 높은 유사도를 보유합니다.\n\n2. 예시 상황\n아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.\n{exampling_gen}\n\n3. 상품 추천\n{recommend_product}'
    elif plus_info == web_link:
        answer = f'1. 단어 정의\n{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.\n{definition_gen}\n해당 단어의 추가 정보는 {plus_info} 링크에서 더욱 자세하게 확인가능합니다.\n\n2. 예시 상황\n아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.\n{exampling_gen}\n\n3. 상품 추천\n{recommend_product}'
    #%%
    return answer
#%%
if __name__ == '__main__':

    config = vars(get_args(debug=False))
    
    """dataset"""
    df = pd.read_csv('./assets/data.csv')
    df['embedding'] = df['embedding'].apply(json.loads)
    
    print(getAiAnswer(df, config["question"]))