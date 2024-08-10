#%%
import torch

from langchain_openai import OpenAIEmbeddings
from transformers import AutoModel, AutoTokenizer
from transformers import BertTokenizer, BertModel

#%%
import logging
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)
#%%
# OpenAI embedding
class OpenAIEmbedder_toDB():
    def __init__(self, api_key):
        self.api_key = api_key
    
    def embed(self, data):
        embedding_model = OpenAIEmbeddings(api_key = self.api_key)
        embeddings = embedding_model.embed_documents(data)
        return embeddings

# Huggingface embedding
class HuggingfaceEmbedder_toDB():
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    def embed(self, data):
        inputs = self.tokenizer(
            data, return_tensors='pt', padding=True, truncation=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        return embeddings.tolist()
    
class BERT_Embedder():
    def __init__(self, model_name='snunlp/KR-FinBert'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
    
    def embed(self, text):
        inputs = self.tokenizer(
            text, return_tensors='pt', padding=True, truncation=True, max_length=512
        )
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :] # [CLS] token embedding
        return cls_embedding
    
# Function to get the appropriate embedder
def get_embedder(embedding_type, **kwargs):
    if embedding_type == "openai":
        return OpenAIEmbedder_toDB(api_key=kwargs.get("api_key"))
    elif embedding_type == "huggingface":
        return HuggingfaceEmbedder_toDB(model_name=kwargs.get("model_name"))
    elif embedding_type =="bert":
        return BERT_Embedder()
    else:
        raise ValueError("Unsupported embedding type")


#%%
'''
from Embedding import OpenAIEmbedder_toDB, HuggingfaceEmbedder_toDB, get_embedder

# openai version

OPENAI_API_KEY = 'api_key'  # api_key
DATA = word_dict # word_dictionary  ex. ['a','b','c', ...]

embedding_type = "openai"
embedder = get_embedder(embedding_type, api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
embedding_dict = embedder.embed(DATA)
    
print("Embeddings:")
print(DATA)


# kr-finbert version

MODEL_NAME = 'snunlp/KR-FinBert'
DATA = word_dict

embedding_type = "huggingface"
embedder = get_embedder(embedding_type, model_name=MODEL_NAME)
embedding_dict = embedder.embed(DATA)

'''