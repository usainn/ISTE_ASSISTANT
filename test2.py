import sys
import os
import time

sys.path.append(".")
from src.config import GROQ_API_KEY

print("1. Loading embeddings...")
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("1. Done.")

print("2. Loading LLM...")
from langchain_groq import ChatGroq
llm = ChatGroq(model_name="llama-3.1-8b-instant", api_key=GROQ_API_KEY, temperature=0.1)
print("2. Done.")

print("3. Loading Chroma...")
from langchain_community.vectorstores import Chroma
VECTOR_DB_DIR = os.path.join("vector_db")
vector_db = Chroma(persist_directory=VECTOR_DB_DIR, embedding_function=embeddings)
print("3. Done.")
