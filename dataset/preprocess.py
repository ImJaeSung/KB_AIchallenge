#%%
import os
import sys

os.chdir('..')
sys.path.append('..')
#%%
from tqdm import tqdm 
import pandas as pd
import re
from pypdf import PdfReader
#%%
def load_pdf_data():
    reader = PdfReader(f'./data/2023_경제금융용어 700선-게시(저용량).pdf')

    """index page"""
    matches = []
    for page in tqdm(range(3, 15), desc="generate index..."):
        text = reader.pages[page].extract_text()
        text = re.sub(" ", "", text) 
        text = re.sub("・", "", text)
        if page % 2 != 0: 
            text = re.sub("경제금융용어700선", "", text)
        else:
            text = re.sub("찾아보기", "", text)
        
        text = re.sub("\n", "", text)
        pattern = re.compile(r'([가-힣A-Za-z·\'\+\(\)\/&\s-]+)(\d+)')
        matches.append(pattern.findall(text))


    matches = sum(matches, [])
    delete = []
    for i, (term, page) in tqdm(enumerate(matches), desc="post-processing..."):
        if term == "사전적정책방향제시(forwardguidance)":
            matches[i] = (term, 142)
        elif term == '기본자본(Tier':
            matches[i] = ("기본자본(Tier1)", "66")
        elif term == 'C)지급결제시스템':
            matches[i] = ("기업・개인간(B2C) 지급결제시스템", "66")
        elif term == 'B)지급결제시스템':
            matches[i] = ("기업간(B2B) 지급결제시스템", "66")
        elif term == '기타기본자본(AdditionalTier':
            matches[i] = ("기타기본자본(Additional Tier 1)", "72")
        elif term == '동남아시아국가연합+한중일(ASEAN+':
            matches[i] = ("동남아시아국가연합+한・중・일(ASEAN+3)", "92")
        elif term == '보완자본(Tier':
            matches[i] = ("보완자본(Tier2)", "124")
        elif term == '보통주자본(CommonEquityTier':
            matches[i] = ("보통주자본(CommonEquityTier1)", 125)
        elif term == "산업혁명":
            matches[i] = ("4차산업혁명", page)
        elif term == "슈퍼":
            delete.append(i)
        elif term == "조":
            matches[i] = ('슈퍼301조', '166')
        elif term in ['제', '차통화조치']:
            delete.append(i)
        elif term in ['(GroupofSeven)', '(GroupofTwo)', '(Groupof', 'G']:
            delete.append(i)
        elif term == 'P':
            delete.append(i)
        elif term == 'P대출':
            delete.append(i)
        elif term == ")":
            delete.append(i)
        elif term == "vi금융EDI":
            matches[i] = ('금융EDI', page)
        elif term == "vii대체재":
            matches[i] = ('대체재', page)
        elif term == "v고정환율제도/자유변동환율제도":
            matches[i] = ('고정환율제도/자유변동환율제도', page)
        elif term == 'xi운영리스크':
            matches[i] = ('운영리스크', page)
        elif term == 'xii잠재GDP성장률':
            matches[i] = ('잠재GDP성장률', page)
        elif term == 'xiv통합발행제도':
            matches[i] = ('통합발행제도', page)
        elif term == 'xv환매조건부매매/RP/Repo':
            matches[i] = ('환매조건부매매/RP/Repo', page)
        elif term in ['기업개인간(B', '기업간(B']:
            delete.append(i)
        elif term == 'ix상장지수펀드(ETF)':
            matches[i] = ('상장지수펀드(ETF)', '147')
        elif term == 'xiii지급준비제도':
            matches[i] = ('지급준비제도', page)

    # eliminated by delete index list
    matches = [item for idx, item in enumerate(matches) if idx not in delete]

    # add drop (word, def) pair
    additional_items = [
        ('신흥시장국채권지수(EMBI+)', '178'),
        ('제1차통화조치', '255'),
        ('제2차통화조치', '255'),
        ('한은금융망(BOK-Wire+)', '323'),
        ('G2(GroupofTwo)', '341'),
        ('G20(Groupof20)', '342'),
        ('G7(GroupofSeven)', '342'),
        ('P2P대출', '349')
    ]

    matches.extend(additional_items)

    definitions = []

    for term, page in tqdm(matches, desc="generate dictionary..."):
        page_number = int(page) + 15 
        page_text = reader.pages[page_number].extract_text()
        page_text = re.sub("\n", "", page_text)
        if page_text:
            # pattern = re.compile(re.escape(term) + r'([^\.]+)\.')
            pattern = re.compile(re.escape(term) + r'([^.]+(?:\.[^.]+)*)\.')
            match = pattern.search(page_text)
        
            if match:
                definition = match.group(1).strip()
                definitions.append((term, definition))       
    return pd.DataFrame(definitions, columns = ['용어', '설명'])

#%%
def load_csv_data():
    csv = pd.read_csv(
        "./data/한국산업은행_금융 관련 용어_20151231.csv", encoding='cp949'
    )
    csv_data = csv[["용어", "설명"]]
    return csv_data
#%%
def load_data():
    pdf_data = load_pdf_data()
    csv_data = load_csv_data()

    data = pd.concat([pdf_data, csv_data], axis=0)
    
    # data_dir = './assets'
    # if not os.path.exists(data_dir):
    #     os.makedirs(data_dir)
    # data.to_csv(f'.{data_dir}/data.csv', index=False)    
    
    return data
# %%
if __name__ == '__main__':
    load_data()