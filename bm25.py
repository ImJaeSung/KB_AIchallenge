#%%
from tqdm import tqdm
import pandas as pd
import numpy as np

from rank_bm25 import BM25Okapi
from konlpy.tag import Okt

from modules.tab2text import tab2text
#%%
"""dataset"""
tokenizer = Okt()

textual_data = []
products = pd.read_csv('./assets/loan.csv', encoding='cp949')[["상품 이름", "상품 특징"]]
for idx in tqdm(range(len(products)), desc="textual encoding..."):
    text = tab2text(data=products, idx=idx)
    textual_data.append(text)
#TODO: mydata, another crawling data, 
#%%
tokenized = [tokenizer.morphs(text) for text in textual_data]
bm25 = BM25Okapi(tokenized)

# query
query = "직업은 학생이고 나이는 23세인데, 전세 대출이 뭐야?"
tokenized_query = tokenizer.morphs(query)
scores = bm25.get_scores(tokenized_query)

#%%
top_docs_indices = sorted(
    range(len(scores)), key=lambda i: scores[i], reverse=True
)[:3]
top_docs = [textual_data[i] for i in top_docs_indices]

print(top_docs)
# %%
