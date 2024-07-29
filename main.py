#%%
# langchain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain_community.vectorstores import Chroma, FAISS
from langchain.storage import LocalFileStore
from langchain.chains import RetrievalQA
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
#%%
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
#%%
# 기타
import openai
from openai import OpenAI
from typing import List, Optional
from pydantic import BaseModel
#%%
try:
  import os
  import elasticsearch
  from elasticsearch import Elasticsearch
  import numpy as np
  import pandas as pd
  import sys
  import json
  from ast import literal_eval
  from tqdm import tqdm 
  import datetime
  from elasticsearch import helpers
  
except Exception as e:
  print(f"error: {e}")
#%%
## preprocessing
def text_preprocess(text):
    cleaned_text = re.sub(
       r"(<span class='quot[0-9]'>|\n\r\n|</dl>|</dd>|<dl>|<dt>|</span>|<br/>|<br />|\[.*?\]|([^0-9가-힣A-Za-z.]))", "", text
    )
    return cleaned_text
#%%
# web crawling(fine_word_data)
def create_word_dict(num):

  global words_list, definitions_list

  word_address = 'https://fine.fss.or.kr/fine/fnctip/fncDicary/list.do?menuNo=900021&pageIndex=' + num + '&src=&kind=&searchCnd=1&searchStr='
  requested = requests.get(word_address, 'html.parser')
  soup = BeautifulSoup(requested.content)

  words = soup.select('#content > div.bd-list.result-list > dl > dt') # word
  definitions = soup.select('#content > div.bd-list.result-list > dl > dd') # defin

  words_list = []
  definitions_list = []

  for word, definition in zip(words, definitions):
    words_list.append(text_preprocess(word.get_text()))
    definitions_list.append(definition.get_text())

  return words_list, definitions_list
#%%
# dictionary
word_dict = []
definition_dict = []

for i in range(1, 55):
  word, definition = create_word_dict(str(i))
  word_dict.extend(word)
  definition_dict.extend(definition)
