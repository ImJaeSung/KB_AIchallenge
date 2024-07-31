# langchain
from langchain_openai import ChatOpenAI

from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain_community.llms import HuggingFacePipeline  # Langchain LLM 관련 모듈 HuggingFace 파이프라인을 사용하는 LLM
from langchain_community.document_loaders import PyPDFLoader  # PDF 문서 로더
from langchain_community.vectorstores.utils import DistanceStrategy

from langchain.chains.question_answering import load_qa_chain  # 질의 응답 체인 로드
from langchain.chains import RetrievalQA, RetrievalQAWithSourcesChain  # 질의 응답 체인
from langchain.memory import ConversationSummaryMemory  # Langchain 메모리 관련 모듈대화 요약 메모리
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter  # Langchain 텍스트 분할기 모듈 문자 기반 텍스트 분할기
from langchain.prompts import PromptTemplate  # Langchain 프롬프트 템플릿 관련 모듈 프롬프트 템플릿
from langchain.schema import Document  # 문서 스키마
from langchain import hub
from langchain.storage import LocalFileStore

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough



from rank_bm25 import BM25Okapi

import faiss


# web crawling

from bs4 import BeautifulSoup
import requests
import re
import datetime
from tqdm import tqdm
import sys
import numpy as np
import pandas as pd
import re
import os
import pprint
from selenium import webdriver
import time
import urllib.request
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 기타

# PyTorch 관련 모듈
import torch  # PyTorch 프레임워크

# Transformers 관련 모듈
from transformers import (
    AutoModel,
    AutoModelForCausalLM,  # 언어 모델을 로드하는 함수
    AutoTokenizer,  # 토크나이저를 로드하는 함수
    BitsAndBytesConfig,  # 양자화 및 압축을 위한 설정
    TrainingArguments,  # 모델 훈련을 위한 인자 설정
    pipeline,  # 파이프라인을 생성하는 함수
    logging,  # 로깅을 위한 함수
    AutoConfig,  # 설정을 로드하는 함수
    GenerationConfig  # 텍스트 생성을 위한 설정
)

from sentence_transformers import SentenceTransformer, util
import openai
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel

## kb_handler
from KB_Handler import Cosine_Similarity, Embedding, Text_Preprocess, Web_Research

# base
web_word = None
web_definition = None
web_link = None
ret_word = None
ret_definition = None
ret_score = None


# 데이터 불러오는 부분

# preprocessing
def text_preprocess(text):
    cleaned_text = re.sub(r"(<span class='quot[0-9]'>|\n\r\n|</dl>|</dd>|<dl>|<dt>|</span>|<br/>|<br />|\[.*?\]|([^0-9가-힣A-Za-z.]))", "", text)
    return cleaned_text

# web crawling(fine_word_data)
def create_word_dict(num):

  global words_list, definitions_list

  word_address = 'https://fine.fss.or.kr/fine/fnctip/fncDicary/list.do?menuNo=900021&pageIndex=' + num + '&src=&kind=&searchCnd=1&searchStr='
  requested = requests.get(word_address, 'html.parser')
  soup = BeautifulSoup(requested.content, 'html.parser')

  words = soup.select('#content > div.bd-list.result-list > dl > dt') # word
  definitions =  soup.select('#content > div.bd-list.result-list > dl > dd') # defin

  words_list = []
  definitions_list = []

  for word, definition in zip(words, definitions):
    words_list.append(text_preprocess(word.get_text()))
    definitions_list.append(definition.get_text())

  return words_list, definitions_list

# dictionary
word_dict = []
definition_dict = []

for i in range(50,55):  # 50~55 페이지만 등록(메모리 이슈)
  word, definition = create_word_dict(str(i))
  word_dict.extend([w.split('.')[1] for w in word])
  definition_dict.extend(definition)


### 1
print("DB 데이터 저장 (따로 관리) -> dataframe 형태로 받아야함")
# Function to get the appropriate embedder
def get_embedder(embedding_type, **kwargs):
    if embedding_type == "openai":
        return Embedding.OpenAIEmbedder_toDB(api_key=kwargs.get("api_key"))
    elif embedding_type == "huggingface":
        return Embedding.HuggingfaceEmbedder_toDB(model_name=kwargs.get("model_name"))
    else:
        raise ValueError("Unsupported embedding type")

# openai version
OPENAI_API_KEY = "sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0"

DATA = word_dict  # word_list
DEFINITION = definition_dict # definition_list

embedding_type = "openai" # dim = 1536
embedder = get_embedder(embedding_type, api_key=OPENAI_API_KEY)
EMBEDDING = embedder.embed(DATA) # embedding_list

# DB data load
df = pd.DataFrame({'word': DATA, 'definition': DEFINITION, 'embedding': EMBEDDING})
print("df 완성\n")



### 2
print("사용자가 질문하기\n")

question = '퇴직연금의 정의가 뭐야?'
print(question)


### 3
print("1차적 retriever 생성\n")

# 3-1. question에 대한 embedding vector 생성
embedding_q = embedder.embed([question])

# DB에서 코사인 유사도로 retriver -> result 추출

# cosine class에서 함수 불러오기
cosine = Cosine_Similarity.CosineSimilarityCalculator(threshold=0.9)
result = cosine.calculate_similarity(embedding_q, df)

if result == '해당 단어에 대한 정의가 사전에 정의되어있지 않습니다. 외부 검색 결과로 알려드리겠습니다.':
  query = question
  web_research = Web_Research.WebResearch()
  titles_blog, links_blog = web_research.get_blog_links(query)
  contents_blog = web_research.get_blog_contents(links_blog)

  titles_dict, links_dict = web_research.get_dict_links(query)
  contents_dict = web_research.get_dict_contents(links_dict)

  contents = contents_blog + contents_dict
  links = links_blog + links_dict

else:
  ret_word = result['word']
  ret_definition = result['definition']
  ret_score = result['score']

print(f"단어 : {ret_word}")
print(f"정의 : {ret_definition}")
print(f"유사도 : {ret_score}")


### 4
print("\nDocument 정보를 text split 후 vector DB 저장\n")

# Document 클래스 정의
class Document(BaseModel):
    page_content: str
    metadata: Optional[dict] = None

# text splitting
text_splitter = CharacterTextSplitter(
    separator = '.',
    chunk_size = 400,
    chunk_overlap  = 200,
    length_function = len,
)

text_list = []
link_list = []
for content,link in zip(contents,links):
  text = text_splitter.split_text(content)
  text_list.extend(text)
  link_list.extend([link] * len(text))

docs_objects = [Document(page_content=text, metadata={"source": link}) for text, link in zip(text_list, link_list)]

# openai embedding model
openai_api_key = "sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0"
embeddings_model = OpenAIEmbeddings(openai_api_key=openai_api_key)

# faiss vectorstore
vectorstore = FAISS.from_documents(docs_objects,
                                   embedding = embeddings_model,
                                   distance_strategy = DistanceStrategy.COSINE
                                  )
vectorstore


### 5
print("vector DB에서 retriver 후 최종 docs 생성\n")
retriever = vectorstore.as_retriever(
    search_type='mmr',
    search_kwargs={'k': 5, 'lambda_mult': 0.5}
)

docs = retriever.get_relevant_documents(query)
docs_link = docs[0].metadata['source']


### 6
print("llm을 통해 1차 result 생성 \n")

# Prompt
template = '''Answer the question based only on the following context:
{context}

Question: {question}

Please speak politely.
'''

prompt = ChatPromptTemplate.from_template(template)

# Model
llm = ChatOpenAI(
    openai_api_key = openai_api_key,
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


### 7

# 두개의 retriever 중 생성된 해답에 대한 최종 word, definition, plus_info 생성
# DB 먼저 확인 -> 없음 WEB 결과

word = ret_word if ret_word is not None else web_word
definition = ret_definition if ret_definition is not None else web_definition
plus_info = ret_score if ret_score is not None else web_link # EB에서는 유사도, WEB에서는 링크


### 8
print("llm으로 재생성\n")

# api_key
client = OpenAI(api_key="sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0")

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

definition_gen = simplify_definition(definition)

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

exampling_gen = exampling_definition(word, definition)


### 최종
print('1. 단어의 정의')
print(f'{word}에 대한 정의를 알기 쉽게 설명드리겠습니다.')
print(definition_gen)
if plus_info == ret_score:
    print(f'해당 단어의 정의는 {plus_info}의 저희 dictionary 상에서 높은 유사도를 보유합니다.')
elif plus_info == web_link:
    print(f'해당 단어의 추가 정보는 {plus_info} 링크에서 더욱 자세하게 확인가능합니다.')
print('\n 2. 예시 상황')
print('아래는 해단 단어가 직접 사용될 수 있는 예시 상황입니다.')
print(f'{exampling_gen}')