# 🏗️ System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Streamlit Frontend                       │
│  (User uploads PDFs, enters queries, views results)         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Research Orchestrator                       │
│  (Coordinates all agents and manages workflow)              │
└───────────────────────────┬─────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │   RAG System │ │    Agents     │ │  Groq LLM   │
    │   (FAISS)    │ │  (4 agents)   │ │  API        │
    └──────────────┘ └──────────────┘ └──────────────┘
```

## Component Details

### 1. Frontend Layer (app.py)
- **Framework**: Streamlit
- **Responsibilities**:
  - File upload interface
  - Query input
  - Progress tracking
  - Results display
  - Session state management

### 2. Orchestration Layer (orchestrator.py)
- **Responsibilities**:
  - Workflow coordination
  - Agent sequencing
  - Progress callbacks
  - Execution logging
  - Error handling

### 3. RAG System (rag_system.py)
- **Components**:
  - PDF text extraction (pypdf)
  - Text chunking (RecursiveCharacterTextSplitter)
  - Embeddings (Sentence Transformers)
  - Vector storage (FAISS)
  - Similarity search

### 4. Agent Layer (agents.py)
Four specialized agents:

#### 🧠 Planner Agent
- Input: User query + document count
- Output: List of prioritized tasks
- Method: LLM-based task decomposition

#### 🔍 Retriever Agent
- Input: Search query
- Output: Relevant document chunks
- Method: FAISS similarity search

#### 📊 Analyst Agent
- Input: Task + context chunks
- Output: Analysis results
- Methods:
  - Summarization
  - Insight extraction
  - Contradiction detection
  - Trend analysis

#### ✍️ Reviewer Agent
- Input: All analysis results
- Output: Polished final report
- Method: LLM-based synthesis and editing

### 5. LLM Layer
- **Provider**: Groq
- **Models**: Mixtral 8x7b, LLaMA 3 70B, Gemma 7B
- **Usage**: All agents use same LLM instance

## Data Flow

### Document Processing Flow
```
PDF Upload
    ↓
Extract Text (pypdf)
    ↓
Split into Chunks (1000 tokens, 200 overlap)
    ↓
Generate Embeddings (Sentence Transformers)
    ↓
Store in FAISS Vector DB
    ↓
Ready for Retrieval
```

### Analysis Flow
```
User Query
    ↓
Planner Agent → Creates Tasks [T1, T2, T3, T4]
    ↓
For each Task:
    ↓
    Retriever Agent → Fetch Relevant Chunks
    ↓
    Analyst Agent → Analyze Chunks
    ↓
    Store Result
    ↓
Reviewer Agent → Synthesize All Results
    ↓
Final Report
```

## Key Design Decisions

### 1. In-Memory Vector Store (FAISS)
**Why**: No database setup, fast, perfect for POC
**Trade-off**: Data lost between sessions
**Alternative**: ChromaDB/Pinecle for persistence

### 2. Sentence Transformers for Embeddings
**Model**: all-MiniLM-L6-v2
**Why**: 
- Fast (CPU-friendly)
- Good quality
- Small model size (80MB)
**Alternative**: OpenAI embeddings (costs $$$)

### 3. LangChain for Agents
**Why**: 
- Standard framework
- Easy LLM integration
- Extensible
**Trade-off**: Adds dependency
**Alternative**: Direct API calls

### 4. Four Separate Agents
**Why**: 
- Clear separation of concerns
- True multi-agent architecture
- Demonstrable workflow
**Alternative**: Single agent with complex prompt

### 5. Groq for LLM
**Why**:
- Fast inference
- Free tier available
- Multiple model choices
**Trade-off**: API dependency
**Alternative**: Local LLMs (Ollama)

## Scalability Considerations

### Current Limitations
- In-memory only (no persistence)
- Single-threaded execution
- Limited by Groq rate limits
- CPU-bound embeddings

### Future Enhancements
1. **Persistence**: Add ChromaDB/PostgreSQL
2. **Parallel Processing**: Process tasks concurrently
3. **Caching**: Cache embeddings and results
4. **GPU Support**: Faster embeddings
5. **Streaming**: Stream results as they arrive

## Security & Privacy

### Current Implementation
- ✅ API keys in environment variables
- ✅ Temporary PDF processing
- ✅ No data logging
- ✅ In-memory only (no disk persistence)

### Considerations
- PDFs never sent to third parties (except embedded via Groq)
- No user data stored
- Session state cleared on browser close
- API calls logged by Groq (their privacy policy applies)

## Performance Characteristics

### Typical Timing (5-page PDFs, 3 documents)
- Document processing: 10-30 seconds
- Planning: 2-5 seconds
- Retrieval: <1 second per query
- Analysis (per task): 5-15 seconds
- Review: 10-20 seconds
- **Total**: 30-90 seconds

### Bottlenecks
1. LLM inference (Groq API)
2. Embedding generation (first time)
3. PDF text extraction (large files)

### Optimization Tips
- Use smaller, focused documents
- Choose faster LLM models (Gemma 7B)
- Reduce chunk count (increase chunk_size)
- Limit number of tasks (modify Planner)

## Error Handling

### Implemented
- PDF extraction errors
- API connection failures
- Invalid API keys
- JSON parsing errors
- Empty document handling

### User Experience
- Clear error messages
- Graceful fallbacks
- Progress indicators
- Execution logs for debugging

## Code Organization

```
multi_agent_rag/
│
├── app.py              # Streamlit UI (frontend)
├── orchestrator.py     # Workflow coordinator
├── agents.py           # Four agent classes
├── rag_system.py       # FAISS + embeddings
│
├── requirements.txt    # Dependencies
├── .env               # API keys
├── .gitignore         # Git exclusions
│
├── README.md          # Full documentation
├── QUICKSTART.md      # Quick start guide
└── ARCHITECTURE.md    # This file
```

## Extension Points

### Easy to Add
1. New agent types (e.g., Citation Agent)
2. Different LLM providers
3. Additional file types (DOCX, TXT)
4. Custom analysis tasks
5. Export formats (PDF, DOCX)

### Requires Refactoring
1. Real-time streaming
2. Multi-user support
3. Database persistence
4. Authentication/authorization
5. API endpoint

---

**Architecture designed for clarity, demonstrability, and extensibility**