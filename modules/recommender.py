#%%
import os
import sys

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from rank_bm25 import BM25Okapi
from konlpy.tag import Okt    
'''
JVMNotFoundException: No JVM shared library file (jvm.dll) found. Try setting up the JAVA_HOME environment variable properly.
'''
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-21\bin\server' 
# os.environ['JAVA_HOME'] = r'/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home'

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.Embedding import get_embedder
#%%
def topK_product_rec(full_query, textual_data, textual_embedding, k=5):
    embedder = get_embedder(embedding_type="bert")
    embedding_q = embedder.embed(full_query)
    embedding_q = np.array(embedding_q[0]).reshape(1, -1)

    similarities = cosine_similarity(
        embedding_q, textual_embedding
    ).flatten()
    assert similarities.shape[0] == textual_embedding.shape[0]

    topk_idx = np.argsort(similarities)[-k:][::-1]
    topk_score = [similarities[i] for i in topk_idx]

    assert len(textual_data) == similarities.shape[0]
    topk_product = [textual_data[i] for i in topk_idx]
    assert len(topk_product) == k

    return topk_product, topk_score
#%%    
def best_product_rec(topk_product, full_query):
    tokenizer = Okt()

    tokenized = [tokenizer.morphs(text) for text in topk_product]
    bm25 = BM25Okapi(tokenized)

    # query
    tokenized_query = tokenizer.morphs(full_query)
    scores = bm25.get_scores(tokenized_query)

    #%%
    best_idx = max(range(len(scores)), key=lambda i: scores[i])
    best_product = [topk_product[best_idx]]
    best_score = [scores[best_idx]]

    return best_product, best_score