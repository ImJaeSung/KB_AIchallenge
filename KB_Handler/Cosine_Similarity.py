import pandas as pd
import numpy as np

class CosineSimilarityCalculator:
    def __init__(self, threshold=0.8):
        self.threshold = threshold


    def cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)


    def calculate_similarity(self, input_vector, df):
        # Ensure input_vector is a numpy array
        input_vector = np.array(input_vector[0])

        # Extract embeddings from the dataframe and ensure they are numpy arrays
        embeddings = np.vstack(df['embedding'].values)

        # Calculate cosine similarities
        similarities = np.array([self.cosine_similarity(input_vector, emb) for emb in embeddings])

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