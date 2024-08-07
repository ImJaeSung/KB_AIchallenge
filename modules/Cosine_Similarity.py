import pandas as pd
import numpy as np
import json
from tqdm import tqdm

from sklearn.metrics.pairwise import cosine_similarity
from modules.Embedding import get_embedder
from modules.tab2text import tab2text


class CosineSimilarityCalculator:
    def __init__(self, threshold=0.8):
        self.threshold = threshold


    def cosine_similarity(self, vec1, vec2):

        vec1 = np.squeeze(vec1)
        vec2 = np.squeeze(vec2)

        vec1 = vec1.astype(float)
        vec2 = vec2.astype(float)

        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)


    def calculate_similarity(self, embedding_q, df):
        # Ensure embedding_q is a numpy array
        embedding_q = np.array(embedding_q[0]).reshape(1, -1)
        # Extract embeddings from the dataframe and ensure they are numpy arrays
        embeddings = np.vstack(df['embedding'].values)
        # Calculate cosine similarities
        # similarities = np.array([self.cosine_similarity(embedding_q, emb) for emb in embeddings])
        similarities = cosine_similarity(embedding_q, embeddings).flatten()
        assert similarities.shape[0] == embeddings.shape[0]
        
        # Add similarity scores to the dataframe
        df['score'] = similarities

        # Find the row with the highest similarity score
        max_score = similarities.max()
        best_match = df.loc[similarities.argmax()]

        # Check if the highest score is above the threshold
        if max_score >= self.threshold:
            return {
                'word': best_match['word'],
                'definition': best_match['definition'],
                'score': max_score
            }
        else:
            return "해당 단어에 대한 정의가 사전에 정의되어있지 않습니다. 외부 검색 결과로 알려드리겠습니다."
        
#%%
def topK_product(full_query, textual_data, textual_embedding, k=5):
    embedder = get_embedder(embedding_type="bert")
    embedding_q = embedder.embed(full_query)
    embedding_q = np.array(embedding_q[0]).reshape(1, -1)

    # scores = {}
    # textual_embedding = embedder.embed(textual_data)
    # textual_embedding = np.vstack(textual_embedding)

    similarities = cosine_similarity(
        embedding_q, textual_embedding
    ).flatten()
    assert similarities.shape[0] == textual_embedding.shape[0]

    topk_idx = np.argsort(similarities)[-k:][::-1]
    topk_score = [similarities[i] for i in topk_idx]

    # top_sentence = textual_data[best_idx]
    # score = similarities[best_idx]
    print(len(textual_data))
    print(topk_idx)

    assert len(textual_data) == similarities.shape[0]
    topk_product = [textual_data[i] for i in topk_idx]
    assert len(topk_product) == k

    # for sentence in tqdm(doc_sentences, desc="Calculating similarities..."):
    #     sentence_embedding = embedder.embed(sentence)
    #     similarity_score = cosine_similarity(query_embedding, sentence_embedding).item()
    #     scores[sentence] = similarity_score
    
    # top_k_sentences = sorted(scores, key=scores.get, reverse=True)[:k]
    
    # return top_k_sentences, [scores[sentence] for sentence in top_k_sentences]
    return topk_product, topk_score
#%%
def postprocessing(text):
    # 첫 번째 온점의 위치를 찾음
    period_index = text.find('.')
    
    # 첫 번째 온점이 발견되면 그 위치까지의 문자열을 반환
    if period_index != -1:
        return text[:period_index + 1]
    else:
        return text  # 온점이 없는 경우, 원본 텍스트 반환