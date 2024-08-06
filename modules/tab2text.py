import pandas as pd

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)
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