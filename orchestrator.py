"""
Multi-Agent Orchestrator
Coordinates all agents in the research analysis pipeline
"""

from typing import List, Dict, Any
from agents import PlannerAgent, RetrieverAgent, AnalystAgent, ReviewerAgent
from rag_system import RAGSystem
from langchain_groq import ChatGroq
import time


class ResearchOrchestrator:
    """
    Orchestrates the multi-agent workflow:
    1. Planner creates tasks
    2. Retriever fetches relevant content
    3. Analyst performs analysis
    4. Reviewer polishes the output
    """
    
    def __init__(self, groq_api_key: str, model_name: str = "llama-3.3-70b-versatile"):
        # Initialize LLM
        self.llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name,
            temperature=0.3
        )
        
        # Initialize RAG system
        self.rag_system = RAGSystem()
        
        # Initialize agents
        self.planner = PlannerAgent(self.llm)
        self.retriever = None  # Will be set after documents are loaded
        self.analyst = AnalystAgent(self.llm)
        self.reviewer = ReviewerAgent(self.llm)
        
        # Workflow state
        self.execution_log = []
    
    def load_documents(self, uploaded_files) -> Dict[str, Any]:
        """Load and process documents"""
        start_time = time.time()
        
        num_chunks = self.rag_system.process_documents(uploaded_files)
        
        # Initialize retriever with vector store
        self.retriever = RetrieverAgent(self.rag_system.get_vector_store())
        
        processing_time = time.time() - start_time
        
        return {
            "num_files": len(uploaded_files),
            "num_chunks": num_chunks,
            "sources": self.rag_system.get_source_files(),
            "processing_time": processing_time
        }
    
    def analyze(self, user_query: str, progress_callback=None) -> Dict[str, Any]:
        """
        Execute full multi-agent analysis pipeline
        """
        
        if self.retriever is None:
            raise ValueError("No documents loaded. Please upload documents first.")
        
        self.execution_log = []
        start_time = time.time()
        
        # Step 1: Planning
        if progress_callback:
            progress_callback("🧠 Planner Agent: Creating analysis plan...")
        
        self._log("Planning Phase Started")
        tasks = self.planner.plan(user_query, self.rag_system.get_document_count())
        self._log(f"Generated {len(tasks)} tasks: {[t.description for t in tasks]}")
        
        # Step 2: Retrieval + Analysis
        if progress_callback:
            progress_callback("🔍 Retriever Agent: Fetching relevant content...")
        
        analysis_results = []
        
        for i, task in enumerate(tasks):
            if progress_callback:
                progress_callback(f"📊 Analyst Agent: Executing task {i+1}/{len(tasks)} - {task.description}")
            
            self._log(f"Task {task.task_id}: {task.description}")
            
            # Retrieve relevant chunks for this task
            if task.task_type == "summarize":
                # For summaries, get broader context
                context_chunks = self.retriever.retrieve(user_query, k=10)
            else:
                # For specific analysis, use targeted retrieval
                context_chunks = self.retriever.retrieve(task.description, k=5)
            
            # Perform analysis
            result = self.analyst.analyze(task, context_chunks, user_query)
            analysis_results.append(result)
            
            self._log(f"Task {task.task_id} completed")
        
        # Step 3: Review and Synthesis
        if progress_callback:
            progress_callback("✍️ Reviewer Agent: Polishing final report...")
        
        self._log("Review Phase Started")
        final_report = self.reviewer.review(analysis_results, user_query)
        self._log("Review Phase Completed")
        
        total_time = time.time() - start_time
        
        return {
            "query": user_query,
            "tasks_executed": len(tasks),
            "task_list": [{"id": t.task_id, "desc": t.description, "type": t.task_type} for t in tasks],
            "final_report": final_report,
            "execution_time": total_time,
            "execution_log": self.execution_log,
            "sources_used": self.rag_system.get_source_files()
        }
    
    def _log(self, message: str):
        """Add to execution log"""
        timestamp = time.strftime("%H:%M:%S")
        self.execution_log.append(f"[{timestamp}] {message}")
    
    def clear(self):
        """Clear all data"""
        self.rag_system.clear()
        self.retriever = None
        self.execution_log = []