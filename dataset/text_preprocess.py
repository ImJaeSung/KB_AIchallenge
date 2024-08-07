#%%
import os
import sys
import json

from tqdm import tqdm
import pandas as pd
import numpy as np

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.utils import tab2text
from modules.Embedding import get_embedder

#%%
def main():
    data_dir = "../assets"
    cols = ["상품분류", "상품이름", "상품특징"]

    craw1 = pd.read_csv(f'{data_dir}/crawling/deposit.csv')[cols]
    craw2 = pd.read_csv(f'{data_dir}/crawling/foregin_deposit.csv')[cols]
    craw3 = pd.read_csv(f'{data_dir}/crawling/loan.csv')[cols]
    craw4 = pd.read_csv(f'{data_dir}/crawling/trust.csv')[cols]
    craw5 = pd.read_csv(f'{data_dir}/crawling/other_product.csv')[cols]

    products = pd.concat([craw1, craw2, craw3, craw4, craw5], axis=0).reset_index(drop=True)


    textual_data = []

    for idx in tqdm(range(len(products)), desc="textual encoding..."):
        text = tab2text(data=products, idx=idx)
        textual_data.append(text)

    # delete '판매중단'
    textual_data = [data for data in textual_data if "판매중단" not in data]
    textual_data = [data for data in textual_data if "신규중단" not in data]

    embedder = get_embedder(embedding_type="bert")
    textual_embedding = embedder.embed(textual_data)
    
    #%%
    with open(f'{data_dir}/textual_product.json', 'w', encoding='utf-8') as jsonfile:
        json.dump(textual_data, jsonfile, ensure_ascii=False, indent=4)
    
    np.save(f'{data_dir}/textual_product.npy', textual_embedding)
    
    return

# %%
if __name__ == "__main__":
    main()
