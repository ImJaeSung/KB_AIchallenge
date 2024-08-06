#%%
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm
from modules.tab2text import tab2text
import pandas as pd
from konlpy.tag import Kkma
#%%
"""load tokenizer and model"""
tokenizer = BertTokenizer.from_pretrained('snunlp/KR-FinBert')
model = BertModel.from_pretrained('snunlp/KR-FinBert')
#%%
"""utils"""
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():  
        outputs = model(**inputs)
    cls_embedding = outputs.last_hidden_state[:, 0, :] # [CLS] token embedding
    return cls_embedding

def calculate_similarity(query_embedding, doc_embedding):
    similarity = cosine_similarity(query_embedding, doc_embedding)
    return similarity.item()

def find_top_k_similar_sentences(query, doc_sentences, k=3):
    query_embedding = get_embedding(query)
    scores = {}
    
    for sentence in tqdm(doc_sentences, desc="Calculating similarities..."):
        sentence_embedding = get_embedding(sentence)
        similarity_score = calculate_similarity(query_embedding, sentence_embedding)
        scores[sentence] = similarity_score
    
    top_k_sentences = sorted(scores, key=scores.get, reverse=True)[:k]
    
    return top_k_sentences, [scores[sentence] for sentence in top_k_sentences]

#%%
def postprocessing(text):
    # 첫 번째 온점의 위치를 찾음
    period_index = text.find('.')
    
    # 첫 번째 온점이 발견되면 그 위치까지의 문자열을 반환
    if period_index != -1:
        return text[:period_index + 1]
    else:
        return text  # 온점이 없는 경우, 원본 텍스트 반환
#%%
"""dataset"""
data_dir = "./assets"
dictionary = pd.read_csv(f'{data_dir}/data.csv')

cols = ["상품분류", "상품이름", "상품특징"]

craw1 = pd.read_csv(f'{data_dir}/crawling/deposit.csv')[cols]
craw2 = pd.read_csv(f'{data_dir}/crawling/foregin_deposit.csv')[cols]
craw3 = pd.read_csv(f'{data_dir}/crawling/loan.csv')[cols]
craw4 = pd.read_csv(f'{data_dir}/crawling/trust.csv')[cols]
craw5 = pd.read_csv(f'{data_dir}/crawling/other_product.csv')[cols]

products = pd.concat([craw1, craw2, craw3, craw4, craw5], axis=0).reset_index(drop=True)

textual_data = []

for idx in tqdm(range(len(products)), desc="textual encoding..."):
    text = tab2text(data=products, idx=idx)
    textual_data.append(text)
print(textual_data)

# 상위 3개의 유사한 문장을 찾음
query = input('Enter your question:')
# query = "저는 28살 남성이고 직업은 공무원입니다. 소득은 월 280만원입니다. 통화옵션의 정의가 뭐야?"
top_k_sentences, top_k_scores = find_top_k_similar_sentences(query, textual_data, k=3)

# 결과 출력
for i, (sentence, score) in enumerate(zip(top_k_sentences, top_k_scores)):
    print(f"Top-{i+1} 유사한 문장: {sentence} - 유사성 점수: {score:.4f}")
# %%


query_word = "통화옵션"
definition = data[data['word'] == query_word]['definition'].values[0]
#%%
definition = postprocessing(definition)
query = query + " " + definition