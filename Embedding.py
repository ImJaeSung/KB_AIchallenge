# langchain_openaiembedding
from langchain_openai import OpenAIEmbeddings

# Transformers 
from transformers import AutoModel, AutoTokenizer



# OpenAI embedding
class OpenAIEmbedder_toDB():
    def __init__(self, api_key, model='text-embedding-ada-002'):
        self.api_key = api_key
        self.model = model
    
    def embed(self, data):
        embedding_model = OpenAIEmbeddings(api_key = self.api_key, model = self.model)
        embeddings = embedding_model.embed_documents(data)
        return embeddings

# Huggingface embedding
class HuggingfaceEmbedder_toDB():
    def __init__(self, model_name):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
    
    def embed(self, data):
        inputs = self.tokenizer(data, return_tensors='pt', padding=True, truncation=True)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
        return embeddings.tolist()

# Function to get the appropriate embedder
def get_embedder(embedding_type, **kwargs):
    if embedding_type == "openai":
        return OpenAIEmbedder_toDB(api_key=kwargs.get("api_key"), model=kwargs.get("model", "text-embedding-ada-002"))
    elif embedding_type == "huggingface":
        return HuggingfaceEmbedder_toDB(model_name=kwargs.get("model_name"))
    else:
        raise ValueError("Unsupported embedding type")

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