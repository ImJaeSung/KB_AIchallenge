#%%
import json
from tqdm import tqdm

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

from modules.Embedding import get_embedder
from modules.tab2text import tab2text
#%%
def top_K(query, doc_sentences, k=3):
    embedder = get_embedder(embedding_type="bert")
    query_embedding = embedder.embed(query)
    scores = {}
    
    for sentence in tqdm(doc_sentences, desc="Calculating similarities..."):
        sentence_embedding = embedder.embed(sentence)
        similarity_score = cosine_similarity(query_embedding, sentence_embedding).item()
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
def main():
    """dataset"""
    data_dir = "./assets"
    dictionary = pd.read_csv(f'{data_dir}/data.csv')

    with open(f'{data_dir}/textual_product.json', 'r', encoding='utf-8') as jsonfile:
        textual_data = json.load(jsonfile)

    #%%
    # 상위 3개의 유사한 문장을 찾음
    # my_data = pd.read_csv()
    # my_textual_data = tab2text(my_data)
    my_textual_data = "나이는 28살, 성별은 남성, 직업은 공무원, 소득은 월 280만원,"

    # query = input('Enter your question:')
    query = "통화옵션의 정의가 뭐야?"

    query_word = "통화옵션"

    definition = dictionary[dictionary['word'] == query_word]['definition'].values[0]
    definition = postprocessing(definition)

    full_query = my_textual_data + query + " " + definition
    #%%
    top_k_sentences, top_k_scores = top_K(full_query, textual_data, k=3)

    for i, (sentence, score) in enumerate(zip(top_k_sentences, top_k_scores)):
        print(f"Top-{i+1} 유사한 문장: {sentence} - 유사성 점수: {score:.4f}")
#%%
if __name__ == "__main__":
    main()

