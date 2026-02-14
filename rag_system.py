"""
RAG System with FAISS vector store
Handles document processing, embedding, and retrieval
"""

from typing import List, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from pypdf import PdfReader
import tempfile
import os


class RAGSystem:
    """
    Manages document ingestion, embedding, and vector storage
    """
    
    def __init__(self):
        self.embeddings = None
        self.vector_store = None
        self.documents = []
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def initialize_embeddings(self):
        """Initialize embedding model (lazy loading)"""
        if self.embeddings is None:
            # Use a lightweight but effective model
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},
                encode_kwargs={'normalize_embeddings': True}
            )
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from uploaded PDF file"""
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_file.getvalue())
                tmp_path = tmp_file.name
            
            # Extract text
            reader = PdfReader(tmp_path)
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
            
            # Clean up
            os.unlink(tmp_path)
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting PDF: {str(e)}")
    
    def process_documents(self, uploaded_files) -> int:
        """Process uploaded PDFs and create vector store"""
        
        self.initialize_embeddings()
        all_texts = []
        
        for uploaded_file in uploaded_files:
            # Extract text from PDF
            text = self.extract_text_from_pdf(uploaded_file)
            
            # Create document with metadata
            doc = Document(
                page_content=text,
                metadata={
                    "source": uploaded_file.name,
                    "file_type": "pdf"
                }
            )
            all_texts.append(doc)
        
        # Split documents into chunks
        self.documents = self.text_splitter.split_documents(all_texts)
        
        # Create FAISS vector store
        if len(self.documents) > 0:
            self.vector_store = FAISS.from_documents(
                self.documents,
                self.embeddings
            )
        
        return len(self.documents)
    
    def add_text_document(self, text: str, source_name: str = "pasted_text"):
        """Add text content directly (from pasted links/text)"""
        
        self.initialize_embeddings()
        
        doc = Document(
            page_content=text,
            metadata={
                "source": source_name,
                "file_type": "text"
            }
        )
        
        # Split into chunks
        chunks = self.text_splitter.split_documents([doc])
        self.documents.extend(chunks)
        
        # Update or create vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(
                chunks,
                self.embeddings
            )
        else:
            # Add to existing vector store
            new_store = FAISS.from_documents(chunks, self.embeddings)
            self.vector_store.merge_from(new_store)
        
        return len(chunks)
    
    def get_vector_store(self):
        """Get the vector store for retrieval"""
        return self.vector_store
    
    def get_document_count(self) -> int:
        """Get total number of document chunks"""
        return len(self.documents)
    
    def get_source_files(self) -> List[str]:
        """Get list of source file names"""
        sources = set()
        for doc in self.documents:
            sources.add(doc.metadata.get("source", "unknown"))
        return list(sources)
    
    def clear(self):
        """Clear all documents and vector store"""
        self.documents = []
        self.vector_store = None