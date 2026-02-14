# 🚀 Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
Edit `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key at: https://console.groq.com/

### 3. Test Installation
```bash
python test_installation.py
```

### 4. Run Application
```bash
streamlit run app.py
```

## First Analysis (3 Steps)

### Step 1: Upload Documents
1. Go to "📤 Upload Documents" tab
2. Click "Browse files" and select PDF(s)
3. Click "🚀 Process Documents"
4. Wait for processing (usually 10-30 seconds)

### Step 2: Run Analysis
1. Switch to "🔍 Analyze" tab
2. Enter your query, for example:
   ```
   Summarize the key findings and provide strategic recommendations
   ```
3. Click "🔬 Start Analysis"
4. Watch the agents work (Planner → Retriever → Analyst → Reviewer)

### Step 3: View Results
1. Go to "📊 Results" tab
2. Review the executive report
3. Check execution details (expand "🔧 Execution Details")
4. Download report as Markdown

## Example Queries

### For Business Documents
```
What are the main competitive advantages and market opportunities?
```

### For Research Papers
```
Compare the methodologies and identify contradictions in findings
```

### For Multiple Sources
```
Cross-check facts and highlight inconsistencies across documents
```

### For Strategic Analysis
```
Extract trends, identify risks, and provide actionable recommendations
```

## Tips for Best Results

1. **Upload Quality PDFs**
   - Use text-based PDFs (not scanned images)
   - Ensure PDFs are readable and well-formatted
   - Smaller files (<10MB) process faster

2. **Write Clear Queries**
   - Be specific about what you want
   - Mention key topics or focus areas
   - Ask for actionable outputs (insights, recommendations, etc.)

3. **Use Multiple Documents**
   - The system excels at cross-referencing
   - Upload 2-5 documents for best results
   - More documents = better contradiction detection

4. **Review Execution Details**
   - Check which tasks the Planner created
   - See how agents processed your query
   - Learn from the workflow for future queries

## Troubleshooting

### "No module named X"
```bash
pip install -r requirements.txt
```

### "API key not found"
Check `.env` file has:
```
GROQ_API_KEY=gsk_...
```

### Documents not processing
- Ensure PDFs are text-based
- Check file size (<50MB recommended)
- Try with a single small PDF first

### Analysis taking too long
- Use shorter documents
- Switch to Gemma 7B model (faster)
- Process fewer files at once

## Need Help?

1. Check `README.md` for detailed documentation
2. Review execution logs in the app
3. Run `python test_installation.py` to verify setup

---

**You're all set! Happy analyzing! 🔬**