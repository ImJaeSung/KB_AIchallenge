#%%
import re
import random
import pandas as pd
import numpy as np

import torch
#%%
import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
#%%
def postprocessing(text):
    period_index = text.find('.')
    
    if period_index != -1:
        return text[:period_index + 1]
    else:
        return text 

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
    return text

#%%
"""for reproducibility"""
def set_random_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # seed fix for gpu
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    # seed fix for NumPy 
    np.random.seed(seed)
    random.seed(seed)   