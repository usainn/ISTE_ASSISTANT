# ChromaDB ve Grok LangChain bağlantısı
import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
try:
    from langchain.chains import create_retrieval_chain
    from langchain.chains.combine_documents import create_stuff_documents_chain
except ImportError:
    from langchain_classic.chains.retrieval import create_retrieval_chain
    from langchain_classic.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEmbeddings # Yerel embedding en iyisi
from src.config import DATA_DIR, VECTOR_DB_DIR, GROQ_API_KEY
from src.prompt import SYSTEM_PROMPT

class RagEngine:
    def __init__(self):
        # Config'den API anahtarını alıyoruz
        self.api_key = GROQ_API_KEY
        
        if not self.api_key:
             raise ValueError("GROQ_API_KEY bulunamadı! .env veya config dosyasını kontrol edin.")
            
        # Embedding modeli yerel kalsın (all-MiniLM-L6-v2), hem ücretsiz hem çok hızlı.
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # LLM Modeli olarak Groq yapılandırması
        self.llm = ChatGroq(
            model_name="llama-3.1-8b-instant", 
            api_key=self.api_key,
            temperature=0.1
        )
        
        self.vector_db = None
        self._init_vector_db()

    def _init_vector_db(self):
        if os.path.exists(VECTOR_DB_DIR) and os.listdir(VECTOR_DB_DIR):
             self.vector_db = Chroma(
                 persist_directory=VECTOR_DB_DIR, 
                 embedding_function=self.embeddings
             )
        else:
             self.vector_db = None

    def ingest_documents(self):
        documents = []
        
        # PDF Dosyalarını oku
        if os.path.exists(DATA_DIR):
            pdf_loader = DirectoryLoader(DATA_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
            documents.extend(pdf_loader.load())
            
            # Markdown Dosyalarını oku
            md_loader = DirectoryLoader(DATA_DIR, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'autodetect_encoding': True})
            documents.extend(md_loader.load())

            # TXT Dosyalarını oku
            txt_loader = DirectoryLoader(DATA_DIR, glob="**/*.txt", loader_cls=TextLoader, loader_kwargs={'autodetect_encoding': True})
            documents.extend(txt_loader.load())
        
        if not documents:
            return 0
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(documents)
        
        self.vector_db = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings, 
            persist_directory=VECTOR_DB_DIR
        )
        return len(chunks)

    def query(self, user_question: str) -> dict:
        if not self.vector_db:
            return {"answer": "Sistemde henüz yüklenmiş bir mevzuat belgesi bulunmuyor. Lütfen önce belge yükleyin.", "sources": []}
            
        # k=6 yaparak daha fazla belgeden parça alıyoruz, böylece farklı dosyalara odaklanabiliyor.
        retriever = self.vector_db.as_retriever(search_kwargs={"k": 6})
        
        prompt = PromptTemplate.from_template(SYSTEM_PROMPT)
        
        document_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        response = retrieval_chain.invoke({"input": user_question})
        
        answer = response.get("answer", "Yanıt oluşturulamadı.")
        sources = []
        seen_files = set()
        
        if "context" in response and response["context"]:
            for doc in response["context"]:
                source_path = doc.metadata.get("source", "")
                if source_path:
                    file_name = os.path.basename(source_path)
                    page = doc.metadata.get("page", None)
                    if page is not None:
                        page = int(page) + 1
                    
                    # Aynı dosyayı tekrar ekleme (farklı sayfalar olabilir ama biz dosya bazlı gösteriyoruz şimdilik)
                    if file_name not in seen_files:
                        sources.append({
                            "file": file_name,
                            "page": page
                        })
                        seen_files.add(file_name)
                
        return {"answer": answer, "sources": sources}
