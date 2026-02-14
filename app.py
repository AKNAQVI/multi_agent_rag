"""
Multi-Agent AI Research Analyst
Streamlit Interface
"""

import streamlit as st
from orchestrator import ResearchOrchestrator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="AI Research Analyst",
    page_icon="🔬",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .stat-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    api_key = os.getenv('GROQ_API_KEY')
    st.session_state.orchestrator = ResearchOrchestrator(api_key)
    st.session_state.docs_loaded = False
    st.session_state.analysis_complete = False
    st.session_state.results = None

# Header
st.markdown('<div class="main-header">Multi-Agent AI Research Analyst</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload PDFs • Cross-check Facts • Generate Executive Insights</div>', unsafe_allow_html=True)

# Agent badges
st.markdown("""
<div style="text-align: center; margin: 1rem 0;">
    <span class="agent-badge"> Planner</span>
    <span class="agent-badge"> Retriever</span>
    <span class="agent-badge"> Analyst</span>
    <span class="agent-badge"> Reviewer</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# Sidebar
with st.sidebar:
    st.header("Configuration")
    
    # Model selection
    model_options = {
        "LLaMA 3.3 70B (Recommended)": "llama-3.3-70b-versatile",
        "LLaMA 3.1 70B": "llama-3.1-70b-versatile",
        "LLaMA 3.1 8B": "llama-3.1-8b-instant",
        "Gemma 2 9B": "gemma2-9b-it"
    }
    selected_model = st.selectbox(
        "LLM Model",
        options=list(model_options.keys()),
        index=0
    )
    
    # Update model if changed
    if st.button("Update Model"):
        api_key = os.getenv('GROQ_API_KEY')
        st.session_state.orchestrator = ResearchOrchestrator(
            api_key,
            model_name=model_options[selected_model]
        )
        st.session_state.docs_loaded = False
        st.success(f"Switched to {selected_model}")
    
    st.divider()
    
    st.header("About")
    st.markdown("""
    **Multi-Agent Architecture:**
    
    1. **Planner Agent**  
       Breaks queries into sub-tasks
    
    2. **Retriever Agent**  
       Fetches relevant content (RAG)
    
    3. **Analyst Agent**  
       Generates insights & analysis
    
    4. **Reviewer Agent**  
       Polishes final output
    """)
    
    st.divider()
    
    if st.session_state.docs_loaded:
        st.success(f" {st.session_state.doc_stats['num_files']} documents loaded")
        st.info(f" {st.session_state.doc_stats['num_chunks']} chunks indexed")
        
        if st.button("Clear Documents"):
            st.session_state.orchestrator.clear()
            st.session_state.docs_loaded = False
            st.session_state.analysis_complete = False
            st.session_state.results = None
            st.rerun()

# Main content area
tab1, tab2, tab3 = st.tabs(["Upload Documents", "Analyze", "Results"])

# Tab 1: Upload
with tab1:
    st.header("Upload Research Documents")
    
    uploaded_files = st.file_uploader(
        "Upload PDF files",
        type=['pdf'],
        accept_multiple_files=True,
        help="Upload one or more PDF documents for analysis"
    )
    
    if uploaded_files:
        if st.button("Process Documents", type="primary", use_container_width=True):
            with st.spinner("Processing documents..."):
                try:
                    stats = st.session_state.orchestrator.load_documents(uploaded_files)
                    st.session_state.docs_loaded = True
                    st.session_state.doc_stats = stats
                    
                    # Show stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-value">{stats['num_files']}</div>
                            <div class="stat-label">Documents</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-value">{stats['num_chunks']}</div>
                            <div class="stat-label">Chunks</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col3:
                        st.markdown(f"""
                        <div class="stat-box">
                            <div class="stat-value">{stats['processing_time']:.1f}s</div>
                            <div class="stat-label">Processing Time</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.success("Documents processed successfully!")
                    
                    with st.expander("Loaded Files"):
                        for source in stats['sources']:
                            st.write(f"• {source}")
                    
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

# Tab 2: Analyze
with tab2:
    st.header("Research Analysis")
    
    if not st.session_state.docs_loaded:
        st.warning(" Please upload and process documents first (Upload Documents tab)")
    else:
        st.success(" Documents loaded and ready for analysis")
        
        # Query input
        user_query = st.text_area(
            "Research Query",
            placeholder="Example: Analyze the competitive landscape and identify key market trends...",
            height=100,
            help="Enter your research question or analysis request"
        )
        
        # Example queries
        with st.expander("Example Queries"):
            examples = [
                "Summarize the key findings and provide strategic recommendations",
                "What are the main trends and how do they impact our market position?",
                "Identify contradictions or inconsistencies between the sources",
                "Extract actionable insights and highlight potential risks",
                "Compare different perspectives and provide a balanced analysis"
            ]
            for example in examples:
                if st.button(example, key=example):
                    user_query = example
                    st.rerun()
        
        if user_query:
            if st.button("Start Analysis", type="primary", use_container_width=True):
                # Progress tracking
                progress_text = st.empty()
                progress_bar = st.progress(0)
                
                def update_progress(message):
                    progress_text.write(message)
                
                try:
                    # Execute analysis
                    progress_bar.progress(10)
                    results = st.session_state.orchestrator.analyze(
                        user_query,
                        progress_callback=update_progress
                    )
                    progress_bar.progress(100)
                    
                    st.session_state.results = results
                    st.session_state.analysis_complete = True
                    
                    progress_text.empty()
                    progress_bar.empty()
                    st.success("Analysis complete! View results in the Results tab.")
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    progress_bar.empty()

# Tab 3: Results
with tab3:
    st.header("Analysis Results")
    
    if not st.session_state.analysis_complete:
        st.info("Complete an analysis to view results here")
    else:
        results = st.session_state.results
        
        # Execution stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{results['tasks_executed']}</div>
                <div class="stat-label">Tasks Executed</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{results['execution_time']:.1f}s</div>
                <div class="stat-label">Analysis Time</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-value">{len(results['sources_used'])}</div>
                <div class="stat-label">Sources Used</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Query
        st.subheader("Query")
        st.info(results['query'])
        
        # Final Report
        st.subheader("Executive Report")
        st.markdown(results['final_report'])
        
        # Download button
        st.download_button(
            label="Download Report",
            data=results['final_report'],
            file_name="research_analysis.md",
            mime="text/markdown",
            use_container_width=True
        )
        
        # Execution details
        with st.expander(" Execution Details"):
            st.write("**Tasks Executed:**")
            for task in results['task_list']:
                st.write(f"• Task {task['id']}: {task['desc']} (Type: {task['type']})")
            
            st.write("\n**Execution Log:**")
            for log_entry in results['execution_log']:
                st.code(log_entry)
        
        # Sources
        with st.expander("Sources Referenced"):
            for source in results['sources_used']:
                st.write(f"• {source}")

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>Built with Streamlit • LangChain • Groq • FAISS</p>
    <p>Multi-Agent AI Research Analyst v1.0</p>
</div>
""", unsafe_allow_html=True)