#%%
import re
import pandas as pd

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
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
class TextProcessor:
    def __init__(self):
        self.split_pattern = re.compile(r'(의|이|가|은|는|을|를|에|에서|에게)\b')
        self.clean_pattern = re.compile(
            r'\\n|\\u[a-zA-Z0-9]{4}|\\u200b|\\|http[^\s]*|\'|\"|<br/>|</p>'
        )

    # extract word from query
    def extract_first_noun_phrase(self, query):
        parts = self.split_pattern.split(query, maxsplit=1)

        if parts:
            return parts[0].strip()
        else:
            return None


    # text cleaning
    def clean_text(self, text):
        cleaned_text = re.sub(self.clean_pattern, ' ', text)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

        return cleaned_text.strip()
    

#%%
def tab2text(data: pd.DataFrame, idx):

    if isinstance(idx, int):
        row = data.iloc[idx]
    else:
        row = data.loc[idx]
    

    key = list(range(len(row)))

    text = ", ".join(
        [
            "%s은 %s" % (row.index[i], str(row[i]).strip())
            for i in key
        ]
    )
    # tokenized_text = tokenizer(shuffled_text, padding=True, return_tensors="pt")
    # return tokenized_text
    return text