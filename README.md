# KB_AIchallenge
The repository for KB 6th Future Finance A.I. Challenge.

> **_NOTE:_** This repository supports [OpenAI API](https://openai.com/index/openai-api/).
> - Please your OpenAI API key into  `main.py` file.

## Proposal
1. We created a glossary of financial terms to make complex language easier to understand.
2. Generative AI and RAG to easily recreate financial terms and deliver personalized financial content.

### 1. Framework
![image](https://github.com/user-attachments/assets/b2f5a6cc-06fc-4072-ac43-8cf0a26cd70c)

### 2. Demonstration
![시연영상](https://github.com/user-attachments/assets/b4e66521-ff17-40da-8456-f7e042e34560)

## Dataset Preparation

- Download and add the datasets into `data` folder to reproduce our experimental results.
- Data info :
  - [공공데이터포털 한국산업은행 금융관련 용어](https://www.data.go.kr/data/15044350/fileData.do)
  - [한국은행 경제금융용어 700선](https://www.bok.or.kr/portal/bbs/B0000249/view.do?nttId=235017&menuNo=200765)
  - [금융감독원 금융용어사전](https://fine.fss.or.kr/fine/fnctip/fncDicary/list.do?menuNo=900021)
  - [Bank Marketing](https://www.kaggle.com/datasets/janiobachmann/bank-marketing-dataset?resource=download&select=bank.csv)

## Usage
### 1. Preprocessing 

#### Data preparing: 
- Directory: `./crawling/`

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

#### Data preprocess:
- Directory: `./dataset/`

```
python preprocess.py  
```
```
python text_preprocess.py
```

### 2. QnA Task

#### Arguments

- `--gpt_ver` : ChatGPT version that you can use (default: `gpt4`)
- `--question` : Financial terms you may not know the definition of (ex. "기회비용의 정의가 뭐야?") 

#### Using in Python 

```
python main.py --gpt_ver <gpt_ver> --question <question> 
```
- If you want to use it on the web, contact @SongJSeop.
 
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




