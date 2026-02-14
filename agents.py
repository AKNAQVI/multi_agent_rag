"""
Multi-Agent System for Research Analysis
Implements Planner, Retriever, Analyst, and Reviewer agents
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json


@dataclass
class Task:
    """Represents a sub-task from the Planner"""
    task_id: int
    description: str
    task_type: str  # 'summarize', 'extract_insights', 'find_contradictions', etc.
    priority: int


@dataclass
class AnalysisResult:
    """Result from the Analyst agent"""
    summary: str
    key_insights: List[str]
    risks: List[str]
    trends: List[str]
    contradictions: List[str]
    recommendations: List[str]


class PlannerAgent:
    """
    Breaks down user queries into structured sub-tasks
    """
    
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.system_prompt = """You are a strategic planning agent. Your role is to decompose complex research queries into clear, actionable sub-tasks.

Given a user query and available documents, create a structured plan with:
1. Task identification (summarize, extract insights, find contradictions, compare sources)
2. Priority ordering (1=highest, 5=lowest)
3. Clear task descriptions

Return your plan as a JSON array of tasks:
[
  {
    "task_id": 1,
    "description": "Brief description",
    "task_type": "summarize|extract_insights|find_contradictions|compare|analyze_trends",
    "priority": 1
  }
]

Be strategic - prioritize tasks that provide maximum value."""

    def plan(self, user_query: str, num_documents: int) -> List[Task]:
        """Generate a plan of sub-tasks"""
        
        prompt = f"""User Query: {user_query}

Number of documents available: {num_documents}

Create a strategic plan to answer this query comprehensively."""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            # Parse JSON response
            tasks_data = json.loads(response.content)
            tasks = [Task(**task) for task in tasks_data]
            return sorted(tasks, key=lambda x: x.priority)
        except json.JSONDecodeError:
            # Fallback to default tasks
            return [
                Task(1, "Summarize all documents", "summarize", 1),
                Task(2, "Extract key insights", "extract_insights", 2),
                Task(3, "Identify trends and patterns", "analyze_trends", 3),
                Task(4, "Find contradictions between sources", "find_contradictions", 4)
            ]


class RetrieverAgent:
    """
    Handles RAG - retrieves relevant chunks from vector store
    """
    
    def __init__(self, vector_store):
        self.vector_store = vector_store
    
    def retrieve(self, query: str, k: int = 5) -> List[str]:
        """Retrieve top-k relevant chunks"""
        if self.vector_store is None:
            return []
        
        results = self.vector_store.similarity_search(query, k=k)
        return [doc.page_content for doc in results]
    
    def retrieve_all(self) -> List[str]:
        """Retrieve all document chunks"""
        if self.vector_store is None:
            return []
        
        # Get all documents from the vector store
        all_docs = self.vector_store.similarity_search("", k=100)
        return [doc.page_content for doc in all_docs]


class AnalystAgent:
    """
    Performs deep analysis on retrieved content
    Generates insights, identifies risks, trends, and contradictions
    """
    
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.system_prompt = """You are an expert research analyst with expertise in business strategy, market analysis, and critical thinking.

Your role is to:
1. Analyze documents deeply and extract actionable insights
2. Identify key trends, patterns, and themes
3. Highlight risks, challenges, and red flags
4. Find contradictions or inconsistencies between sources
5. Generate strategic recommendations

Provide business-ready analysis that executives can act on."""

    def analyze(self, task: Task, context_chunks: List[str], user_query: str) -> Dict[str, Any]:
        """Perform analysis based on task type"""
        
        context = "\n\n---\n\n".join(context_chunks[:10])  # Limit context size
        
        if task.task_type == "summarize":
            return self._summarize(context, user_query)
        elif task.task_type == "extract_insights":
            return self._extract_insights(context, user_query)
        elif task.task_type == "find_contradictions":
            return self._find_contradictions(context)
        elif task.task_type == "analyze_trends":
            return self._analyze_trends(context, user_query)
        else:
            return self._general_analysis(context, user_query)
    
    def _summarize(self, context: str, query: str) -> Dict[str, Any]:
        """Generate executive summary"""
        
        prompt = f"""Based on the following documents, create a concise executive summary addressing: {query}

Documents:
{context}

Provide:
1. A 2-3 paragraph executive summary
2. 3-5 key takeaways (bullet points)"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return {"type": "summary", "content": response.content}
    
    def _extract_insights(self, context: str, query: str) -> Dict[str, Any]:
        """Extract key insights"""
        
        prompt = f"""Analyze these documents and extract strategic insights related to: {query}

Documents:
{context}

Provide:
1. Key Insights (5-7 strategic findings)
2. Opportunities (what can be leveraged)
3. Challenges (what needs attention)
4. Recommendations (3-5 action items)"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return {"type": "insights", "content": response.content}
    
    def _find_contradictions(self, context: str) -> Dict[str, Any]:
        """Identify contradictions between sources"""
        
        prompt = f"""Analyze these documents for contradictions, inconsistencies, or conflicting information.

Documents:
{context}

Identify:
1. Direct contradictions (where sources disagree)
2. Inconsistent data or claims
3. Different perspectives on the same topic
4. Potential biases or limitations in each source"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return {"type": "contradictions", "content": response.content}
    
    def _analyze_trends(self, context: str, query: str) -> Dict[str, Any]:
        """Identify trends and patterns"""
        
        prompt = f"""Analyze these documents for trends, patterns, and emerging themes related to: {query}

Documents:
{context}

Identify:
1. Major trends (what's changing or evolving)
2. Patterns (recurring themes or connections)
3. Future implications (where things are heading)
4. Strategic considerations"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return {"type": "trends", "content": response.content}
    
    def _general_analysis(self, context: str, query: str) -> Dict[str, Any]:
        """General comprehensive analysis"""
        
        prompt = f"""Perform a comprehensive analysis of these documents to address: {query}

Documents:
{context}

Provide a thorough analysis covering all relevant aspects."""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return {"type": "general", "content": response.content}


class ReviewerAgent:
    """
    Reviews and improves the quality of analysis
    Ensures clarity, coherence, and business-readiness
    """
    
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.system_prompt = """You are a senior editorial reviewer specializing in business communications.

Your role is to:
1. Improve clarity and readability
2. Ensure logical flow and coherence
3. Make content executive-ready (professional tone)
4. Remove redundancy and improve conciseness
5. Enhance structure and formatting

Maintain all key insights and facts while improving presentation."""

    def review(self, analysis_results: List[Dict[str, Any]], user_query: str) -> str:
        """Review and synthesize all analysis results into a polished report"""
        
        # Combine all analysis results
        combined_analysis = "\n\n".join([
            f"=== {result['type'].upper()} ===\n{result['content']}"
            for result in analysis_results
        ])
        
        prompt = f"""Original Query: {user_query}

Analysis Results:
{combined_analysis}

Review and synthesize this analysis into a polished, executive-ready report.

Structure your report as:
1. Executive Summary (key findings in 2-3 paragraphs)
2. Detailed Analysis (organized by themes)
3. Key Insights & Recommendations (actionable items)
4. Follow-up Questions (3-5 strategic questions for deeper investigation)

Ensure the report is:
- Clear and concise
- Logically organized
- Professional in tone
- Actionable for decision-makers"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=prompt)
        ]
        
        response = self.llm.invoke(messages)
        return response.content