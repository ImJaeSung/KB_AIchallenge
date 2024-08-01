#%%
import argparse
import json
import numpy as np
import pandas as pd

#%%
## kb_handler
from modules import Cosine_Similarity, Web_Research
from modules.Embedding import get_embedder
from modules.Openai_utils import exampling_definition, simplify_definition
#%%
# Initialize None
web_word = None
web_definition = None
web_link = None
ret_word = None
ret_definition = None
ret_score = None
#%%
api_key="sk-proj-5vrBpk9gQ4bYF8OljiDST3BlbkFJ5Gz2QGqHc2aW6CYKo8w0"
#%%
def get_args(debug):
    parser = argparse.ArgumentParser('parameters')
    
    parser.add_argument('--embedding_type', type=str, default='openai', 
                        help='embedding type (options: openai, huggingface)')    
    parser.add_argument('--threshold', type=float, default=0.9, 
                        help='consine similarity threshold between question and word')  

    if debug:
        return parser.parse_args(args=[])
    else:    
        return parser.parse_args()
#%%
def main():
    #%%
    config = vars(get_args(debug=True))
    #%%
    """dataset"""
    '''
    print("DB 데이터 저장 (따로 관리) -> dataframe 형태로 받아야함")
    # Function to get the appropriate embedder

    '''

    df = pd.read_csv('./assets/data.csv')
    df['embedding'] = df['embedding'].apply(json.loads)
#%%
    """question"""
    print("사용자가 질문하기\n")

    def get_random_word(df):
        # 'word' 열의 모든 단어를 리스트로 변환
        words = df['word'].tolist()

        # 랜덤으로 하나의 단어를 선택
        random_word = np.random.choice(words)

        return random_word

    # 함수 호출
    random_word = get_random_word(df)
    question = random_word + '의 정의가 뭐야?'
    print(question)

    #%%
    ### 3
    print("1차적 retriever 생성\n")

    # 3-1. question에 대한 embedding vector 생성
    embedder = get_embedder(embedding_type=config["embedding_type"], api_key=api_key)
    embedding_q = embedder.embed([question])

    # DB에서 코사인 유사도로 retriver -> result 추출

    # cosine class에서 함수 불러오기
    cosine = Cosine_Similarity.CosineSimilarityCalculator(threshold=config["threshold"])
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

    #%%
    ### 4
    # print("\n1차 retriver 생성\n")

    # 두개의 retriever 중 생성된 해답에 대한 최종 word, definition, plus_info 생성
    # DB 먼저 확인 -> 없음 WEB 결과

    word = ret_word if ret_word is not None else web_word
    definition = ret_definition if ret_definition is not None else web_definition
    plus_info = ret_score if ret_score is not None else web_link # EB에서는 유사도, WEB에서는 링크

    ### 5
    print("llm으로 재생성\n")
    definition_gen = simplify_definition(definition)
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
# %%
if __name__ == '__main__':
    main()