# %%
import argparse
import json
import os
import sys
import numpy as np
import pandas as pd
from typing import List, Optional
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
from modules import Cosine_Similarity, Web_Research, Text_Preprocess
from modules.Embedding import get_embedder
from modules.Openai_utils import exampling_definition, simplify_definition

# %%
api_key = "sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0"


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
    config = vars(get_args(debug=True))

    # base
    web_word = None
    web_definition = None
    web_link = None
    ret_word = None
    ret_definition = None
    ret_score = None

    # %%
    ### 3

    # 3-1. question에 대한 embedding vector 생성
    embedder = get_embedder(embedding_type=config["embedding_type"], api_key=api_key)
    embedding_q = embedder.embed([question])

    # DB에서 코사인 유사도로 retriver -> result 추출
    print("KB DB와 유사도 결과 비교\n")

    # cosine class에서 함수 불러오기
    cosine = Cosine_Similarity.CosineSimilarityCalculator(threshold=config["threshold"])
    result = cosine.calculate_similarity(embedding_q, df)

    if result == '해당 단어에 대한 정의가 사전에 정의되어있지 않습니다. 외부 검색 결과로 알려드리겠습니다.':
        print("KB DB 내에 해당 단어의 정보가 없음\n")
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
            separator='.',
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

        docs_objects = [Document(page_content=text, metadata={"source": link}) for text, link in
                        zip(text_list, link_list)]

        # openai embedding model
        openai_api_key = "sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0"
        embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

        # faiss vectorstore
        vectorstore = FAISS.from_documents(docs_objects,
                                           embedding=embeddings_model,
                                           distance_strategy=DistanceStrategy.COSINE
                                           )
        vectorstore

        print("외부 retriver를 통한 vectorstore 생성\n")

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
        text_processor = Text_Preprocess.TextProcessor()
        web_word = text_processor.extract_first_noun_phrase(query)
        web_definition = chain.invoke({'context': (format_docs(docs)), 'question': query})
        web_link = docs_link
        embedding_word = embedder.embed([web_word])

        new_df = pd.DataFrame({'word': web_word, 'definition': web_definition, 'embedding': embedding_word})

        data_dir = './assets'
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        new_df.to_csv(f'{data_dir}/data_{web_word}.csv', index=False)


    else:
        ret_word = result['word']
        ret_definition = result['definition']
        ret_score = result['score']

    # %%
    ### 4
    # print("\n1차 retriver 생성\n")

    # 두개의 retriever 중 생성된 해답에 대한 최종 word, definition, plus_info 생성
    # DB 먼저 확인 -> 없음 WEB 결과

    word = ret_word if ret_word is not None else web_word
    definition = ret_definition if ret_definition is not None else web_definition
    plus_info = ret_score if ret_score is not None else web_link  # EB에서는 유사도, WEB에서는 링크

    ### 5
    definition_gen = simplify_definition(definition)
    exampling_gen = exampling_definition(word, definition)

    ### 최종

    if plus_info == ret_score:
        answer = f'1. 단어 정의\n{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.\n{definition_gen}\n해당 단어의 정의는 {plus_info}의 저희 dictionary 상에서 높은 유사도를 보유합니다.\n2. 예시 상황\n아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.\n{exampling_gen}'
    elif plus_info == web_link:
        answer = f'1. 단어 정의\n{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.\n{definition_gen}\n해당 단어의 추가 정보는 {plus_info} 링크에서 더욱 자세하게 확인가능합니다.\n2. 예시 상황\n아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.\n{exampling_gen}'

    return answer