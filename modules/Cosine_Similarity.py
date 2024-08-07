#%%
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

#%%
class CosineSimilarityCalculator:
    def __init__(self, threshold=0.8):
        self.threshold = threshold

    def calculate_similarity(self, embedding_q, df):
        embedding_q = np.array(embedding_q[0]).reshape(1, -1) # Ensure embedding_q is a numpy array 
        embeddings = np.vstack(df['embedding'].values) # Extract embeddings from the dataframe and ensure they are numpy arrays
        
        # Calculate cosine similarities
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
