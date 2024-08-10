# KB_AIchallenge
The repository for KB 6th Future Finance A.I. Challenge.
## Dataset Preparation

- Download and add the datasets into `data` folder to reproduce our experimental results.\\
Data info :\\
(1) 공공데이터포털 한국산업은행 금융관련 용어: https://www.data.go.kr/data/15044350/fileData.do \\
(2) 한국은행 경제금융용어 700선: https://www.bok.or.kr/portal/bbs/B0000249/view.do?nttId=235017&menuNo=200765 \\
(3) 금융감독원 금융용어사전: https://fine.fss.or.kr/fine/fnctip/fncDicary/list.do?menuNo=900021 \\
(4) https://www.kaggle.com/code/janiobachmann/bank-marketing-campaign-opening-a-term-deposit \\

### 1. Preprocessing 

#### Data preparing: 
- directory: ./dataset/

```
python preprocess.py  
```
- directory: ./dataset/

#### Data Crawling:
directory: ./crawling/

```
python deposit_crawling.py
```   
```
python foreign_deposit_crawling.py
```
```
python loan_crawling.py
```
```
python other_crawling.py
```
```
python trust_crawling.py
```

#### Crawled data: Textual encoding and embedding
- directory: ./dataset/
  
```
python text_preprocess.py
```

### 2. Usage 

#### Arguments

- `--gpt_ver` : ChatGPT version that you can use (default: `gpt4`)
- `--question` : Financial terms you may not know the definition of (ex. "기회비용의 정의가 뭐야?") 

#### Using in Python 

```
python main.py --gpt_ver <gpt_ver> --question <question> 
```
- If you want to use it on the web, contact (@SongJSeop)
 
## Directory and codes

```
.
+-- data
+-- assets
+-- crawling
|       +-- deposit_crawling.py
|       +-- foreign_deposit_crawling.py
|       +-- loan_crawling.py
|       +-- other_crawling.py
|       +-- trust_crawling.py
+-- dataset
|       +-- mydata_preprocess.py
|       +-- preprocess.py
|       +-- text_preprocess.py
+-- modules 
|       +-- Cosine_Similarity.py
|       +-- Embedding.py
|       +-- Openai_utils.py
|       +-- recommender.py
|       +-- utils.py
|       +-- Web_Research.py
+-- kb_backend
+-- kb_frontend
+-- main.py
+-- LICENSE
+-- README.md
```




