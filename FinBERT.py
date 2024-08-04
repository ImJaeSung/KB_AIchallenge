#%%
from tqdm import tqdm
import pandas as pd

from transformers import BertTokenizer, BertForSequenceClassification
import torch

from modules.tab2text import tab2text
#%%
tokenizer = BertTokenizer.from_pretrained('snunlp/KR-FinBert-SC')
model = BertForSequenceClassification.from_pretrained('snunlp/KR-FinBert-SC')
#%%
textual_data = []

products = pd.read_csv('./assets/loan.csv', encoding='cp949')[["상품이름", "상품특징"]]
for idx in tqdm(range(len(products)), desc="textual encoding..."):
    text = tab2text(data=products, idx=idx)
    textual_data.append(text)
# %%
def get_similarity(query, doc):
    inputs = tokenizer(
        query, doc, return_tensors='pt', padding=True, truncation=True
    )
    outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    return probabilities[:, 1].item()  # '1'은 유사 클래스

#%%
data = pd.read_csv("./assets/data.csv")
query = "저는 28살 남성이고 직업은 공무원입니다. 소득은 월 280만원입니다. 통화옵션의 정의가 뭐야?"
query_word = "통화옵션"
definition = data[data['word'] == query_word]['definition'].values[0]
print(definition)
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
definition = postprocessing(definition)
query = query + " " + definition
#%%
scores = {
    text: get_similarity(query, text) 
    for text in tqdm(textual_data, desc="searching...")
}

k = 3
top_k_documents = sorted(scores, key=scores.get, reverse=True)[:k]

print("Top-{} 유사한 문장:".format(k))
for doc in top_k_documents:
    print(f"{doc} - 유사성 점수: {scores[doc]:.4f}")

# %%
