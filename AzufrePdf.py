 
from llama_index import ServiceContext, StorageContext, download_loader, GPTVectorStoreIndex, SimpleDirectoryReader

from llama_index.vector_stores import ChromaVectorStore
# from llama_index.storage.storage_context import StorageContext
from llama_index.embeddings import HuggingFaceEmbedding  
 
from pathlib import Path
 
import chromadb  
 
from typing import Any  
 
chroma_client = chromadb.PersistentClient(path="./storage/vector_storage/chromadb/")
 
chroma_collection = chroma_client.get_or_create_collection("quickstart")
 
# -------------------------------------------------------------------------------------
 
from llama_index.llms import AzureOpenAI

llm = AzureOpenAI(
    engine="gpt-35-turbo-16k",
    model="gpt-35-turbo-16k",
    temperature=0.0,
    azure_endpoint="https://genai-interns.openai.azure.com/",
    api_key="2dd4400d079a4fd49ddd2e864802522a",
    api_version="2023-07-01-preview",
)
       
 
# ----------------------------------------------------------------------------------------------------------------
 
PDFReader = download_loader("PDFReader")
 
loader = PDFReader()
 
documents = loader.load_data(file=Path('FAQJuly23.pdf'))  
 
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
 
storage_context = StorageContext.from_defaults(vector_store=vector_store)
 
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
 
service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)  
 
index = GPTVectorStoreIndex.from_documents(
    documents, storage_context=storage_context, service_context=service_context  
)
 
query_engine = index.as_query_engine()  
 
for document in documents:
    index.update(document)
   
response = query_engine.query("give me 5 points that are important")
 
print(response)