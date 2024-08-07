# %%
import random
import argparse
import json
import os
import sys
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
from langchain import hub

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# %%
## kb_handler
from modules import Cosine_Similarity, Web_Research
from modules.Embedding import get_embedder
from modules.Openai_utils import exampling_definition, simplify_definition, product_cleaning
from modules.utils import TextProcessor, postprocessing 
from modules.recommender import topK_product_rec, best_product_rec 

# %%
def get_args(debug):
    parser = argparse.ArgumentParser('parameters')

    parser.add_argument('--embedding_type', type=str, default='openai',
                        help='embedding type (options: openai, huggingface)')
    parser.add_argument('--threshold', type=float, default=0.9,
                        help='consine similarity threshold between question and word')

    if debug:
        return parser.parse_args(args=[])
    else:
        return parser.parse_args()

# %%
def getAiAnswer(df, question):
    # %%
    # question = "기회비용 정의가 뭐야?" # for debugging
    print(f"Question: {question}")
    config = vars(get_args(debug=True))
    
    # base
    web_word = None
    web_definition = None
    web_link = None
    ret_word = None
    ret_definition = None
    ret_score = None
    data_dir = './assets'
    openai_api_key = "sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0"
    # %%
    """question embedding"""
    embedder = get_embedder(
        embedding_type=config["embedding_type"], api_key=openai_api_key
    )
    embedding_q = embedder.embed([question])

    # DB에서 코사인 유사도로 retriver -> result 추출
    print("KB DB와 유사도 결과 비교\n")

    # cosine class에서 함수 불러오기
    cosine = Cosine_Similarity.CosineSimilarityCalculator(
        threshold=config["threshold"]
    )
    result = cosine.calculate_similarity(embedding_q, df)
    #%%
    """generating answer:   
    [1] 두개의 retriever 중 생성된 해답에 대한 최종 word, definition, plus_info 생성
    [2] DB 먼저 확인 -> 없음 WEB 결과
    """
    
    if result == '해당 단어에 대한 정의가 사전에 정의되어있지 않습니다. 외부 검색 결과로 알려드리겠습니다.':
        
        print("KB DB 내에 해당 단어의 정보가 없음...\n")
        
        query = question
        web_research = Web_Research.WebResearch()
        titles_blog, links_blog = web_research.get_blog_links(query)
        contents_blog = web_research.get_blog_contents(links_blog)

        titles_dict, links_dict = web_research.get_dict_links(query)
        contents_dict = web_research.get_dict_contents(links_dict)

        contents = contents_blog + contents_dict
        links = links_blog + links_dict

        # Document 클래스 정의
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

        # #TODO: 기존의 사전에 붙이기 
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
    plus_info = ret_score if ret_score is not None else web_link  # EB에서는 유사도, WEB에서는 링크

    """simplify the answer"""
    definition_gen = simplify_definition(word, definition)
    exampling_gen = exampling_definition(word, definition)

    #%%
    """Mydata"""
    with open(f'{data_dir}/textual_mydata.json', 'r', encoding='utf-8') as jsonfile:
        textual_mydata = json.load(jsonfile) # import my data

    # my_textual_data = "나이는 28살, 성별은 남성, 직업은 공무원, 소득은 월 280만원" # for debugging
    definition_first = postprocessing(definition)

    mydata = random.choice(textual_mydata)
    print(f'People: {mydata} \n')
    
    full_query = mydata + " " + question + " " + definition_first
    #%%
    """recommed the product"""
    with open(f'{data_dir}/textual_product.json', 'r', encoding='utf-8') as jsonfile:
        textual_data = json.load(jsonfile) # import KB product data
    
    textual_embedding = np.load(f'{data_dir}/textual_product.npy')
    topk_product, topk_score = topK_product_rec(
        full_query, textual_data, textual_embedding, k=5
    )
    # recommend_product = product_cleaning(topk_product)
    #%%
    """BM25"""
    best_product, best_score = best_product_rec(topk_product, full_query)
    recommend_product = product_cleaning(best_product)
    #%%
    """Final answer"""
    #TODO: output 문장 정리
    if plus_info == ret_score:
        answer = f'1. 단어 정의\n{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.\n{definition_gen}\n\n해당 단어의 정의는 {plus_info:.4f}의 저희 dictionary 상에서 높은 유사도를 보유합니다.\n\n2. 예시 상황\n아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.\n{exampling_gen}\n\n3. 상품 추천\n{recommend_product}'
    elif plus_info == web_link:
        answer = f'1. 단어 정의\n{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.\n{definition_gen}\n해당 단어의 추가 정보는 {plus_info} 링크에서 더욱 자세하게 확인가능합니다.\n\n2. 예시 상황\n아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.\n{exampling_gen}\n\n3. 상품 추천\n{recommend_product}'
    #%%
    return answer
#%%
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python test_tmp.py <question>")
        sys.exit(1)

    question = sys.argv[1]
    
    """dataset"""
    df = pd.read_csv('./assets/data.csv')
    df['embedding'] = df['embedding'].apply(json.loads)
    
    print(getAiAnswer(df, question))