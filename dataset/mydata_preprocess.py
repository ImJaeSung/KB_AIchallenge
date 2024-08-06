"""
Data source: https://www.kaggle.com/datasets/janiobachmann/bank-marketing-dataset?resource=download&select=bank.csv
"""
#%%
import os
import sys
import json

from tqdm import tqdm
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from modules.tab2text import tab2text
#%%
def main():
    """data import"""
    data_dir = "../data"
    mydata = pd.read_csv(f'{data_dir}/bank.csv')[
        ['age', 'job', 'marital', 'education', 
        'default', 'balance', 'housing', 'loan', 'deposit']
    ]
    mydata.columns = [
        '나이', '직업', '결혼 상태', '교육 수준', 
        '디폴트 여부', '잔고', '주택 대출', '개인 대출', '예금 여부'
    ]

    # %%
    """mapping in korean"""
    job_mapping = {
        "admin.": "행정직",
        "technician": "기술자",
        "services": "서비스직",
        "management": "경영진",
        "retired": "은퇴",
        "blue-collar": "육체노동직",
        "unemployed": "실업자",
        "entrepreneur": "기업가",
        "housemaid": "가사도우미",
        "self-employed": "자영업자",
        "student": "학생",
        "unknown": "알 수 없음"
    }

    marital_mapping = {
        "married": "기혼",
        "single": "미혼",
        "divorced": "이혼",
        "unknown": "알 수 없음"
    }

    education_mapping = {
        "secondary": "중등교육",
        "tertiary": "고등교육",
        "primary": "초등교육",
        "unknown": "알 수 없음"
    }

    default_mapping = {"no": "아니요", "yes": "예", "unknown": "알 수 없음"}
    housing_mapping = {"no": "아니요", "yes": "예", "unknown": "알 수 없음"}
    loan_mapping = {"no": "아니요", "yes": "예", "unknown": "알 수 없음"}

    deposit_mapping = {"no": "아니요", "yes": "예"}

    mydata['직업'] = mydata['직업'].map(job_mapping)
    mydata['결혼 상태'] = mydata['결혼 상태'].map(marital_mapping)
    mydata['교육 수준'] = mydata['교육 수준'].map(education_mapping)
    mydata['디폴트 여부'] = mydata['디폴트 여부'].map(default_mapping)
    mydata['주택 대출'] = mydata['주택 대출'].map(housing_mapping)
    mydata['개인 대출'] = mydata['개인 대출'].map(loan_mapping)
    mydata['예금 여부'] = mydata['예금 여부'].map(deposit_mapping)
    #%%
    """textual encoding"""
    textual_data = []

    for idx in tqdm(range(len(mydata)), desc="textual encoding..."):
        text = tab2text(data=mydata, idx=idx)
        textual_data.append(text)
    #%%
    """data save"""
    mydata.to_csv("../assets/mydata.csv", index=False)

    with open(f'../assets/textual_mydata.json', 'w', encoding='utf-8') as jsonfile:
            json.dump(textual_data, jsonfile, ensure_ascii=False, indent=4)
#%%
if __name__ == "__main__":
    main()
