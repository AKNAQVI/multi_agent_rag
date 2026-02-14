# 🔬 Multi_Agent_RAG

A multi-agent AI research analysis system that uses **Retrieval-Augmented Generation (RAG)** and **task decomposition** to analyze research documents and generate structured executive insights.

The system simulates a team of AI analysts working collaboratively to summarize documents, detect contradictions, extract trends, and produce business-ready reports.

---

## 📌 Features

- Upload and analyze multiple research PDFs
- Multi-agent task decomposition workflow
- Retrieval-Augmented Generation (RAG) pipeline
- Cross-document fact validation
- Contradiction and inconsistency detection
- Executive-style summaries and insights
- Trend and risk identification
- Follow-up research question generation
- Real-time analysis tracking

---

## 🤖 Multi-Agent Architecture

### 🧠 Planner Agent
- Breaks complex queries into structured sub-tasks  
- Creates an analysis execution plan  
- Prioritizes research objectives  

### 🔍 Retriever Agent (RAG)
- Generates embeddings using Sentence Transformers  
- Stores vectors in FAISS (in-memory)  
- Retrieves relevant document chunks via similarity search  

### 📊 Analyst Agent
- Performs deep contextual analysis  
- Extracts insights, risks, and patterns  
- Produces structured analytical outputs  

### ✍️ Reviewer Agent
- Refines and validates analysis  
- Improves clarity and coherence  
- Produces final executive report  

---

## 🛠️ Technologies & Tools

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LLM](https://img.shields.io/badge/LLM-8A2BE2?style=flat-square)](https://en.wikipedia.org/wiki/Large_language_model)
[![Faiss](https://img.shields.io/badge/Faiss-150458?style=flat-square)](https://faiss.ai/)
[![LangChain](https://img.shields.io/badge/LangChain-FF6F00?style=flat-square&logo=langchain&logoColor=white)](https://www.langchain.com/)
[![pypdf](https://img.shields.io/badge/pypdf-11557C?style=flat-square&logo=pypdf&logoColor=white)](https://pypi.org/project/pypdf/)

---

## 🏗️ System Workflow

User Query
↓
Planner Agent
↓
Retriever Agent (RAG + FAISS)
↓
Analyst Agent
↓
Reviewer Agent
↓
Executive Report 


---

## 📄 License

MIT License

---

## 🎯 Learning Outcomes

This project demonstrates:

- Multi-Agent AI Systems
- RAG Pipeline Design
- FAISS Vector Retrieval
- Agent Orchestration with LangChain
- Production-style Streamlit Applications

---
