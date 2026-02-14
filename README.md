# PDF RAG Assistant 📚

A Retrieval-Augmented Generation (RAG) application built with Streamlit that allows you to ask questions based on your PDF document (dms-ug.pdf).

## Features

- 📄 PDF document loading and processing
- 🔍 Recursive character text splitting for optimal chunking
- 🤖 HuggingFace embeddings (text-embedding-ada-002 equivalent)
- 💾 ChromaDB vector database storage
- 🎯 BM25 reranking for improved retrieval
- 🔄 Corrective RAG with Tavily web search fallback
- 💬 Interactive chat interface

## Architecture

### RAG Pipeline

1. **Document Loading**: PDF is loaded using PyPDFLoader
2. **Text Splitting**: Recursive character splitting with 1000 chunk size and 200 overlap
3. **Embeddings**: Uses HuggingFace sentence-transformers model (text-embedding-ada-002 equivalent)
4. **Vector Store**: ChromaDB for efficient similarity search
5. **Retrieval**: Ensemble retriever combining BM25 and vector search (BM25 reranking)
6. **LLM**: OpenAI GPT-3.5-turbo for answer generation

### Corrective RAG Flow

```
User Query → Document Search → Answer Found? 
    ↓ No
Alternative Retrieval (Corrective RAG) → Answer Found?
    ↓ No
Tavily Web Search → Answer Found?
    ↓ No
"It is yet to be enhanced for your query"
```

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

2. Configure your API keys in `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

## Getting API Keys

### OpenAI API Key (Required)
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Create a new API key
4. Copy and paste into `.env` file

### Tavily API Key (Optional - for web search)
1. Go to https://tavily.com
2. Sign up for a free account
3. Get your API key from the dashboard
4. Copy and paste into `.env` file

## Usage

1. Run the Streamlit application:
```bash
streamlit run app.py
```

2. Enter your OpenAI API Key in the sidebar

3. (Optional) Enter your Tavily API Key for web search capability

4. Click "Load PDF Document" to process dms-ug.pdf

5. Start asking questions in the chat interface!

## How It Works

### Document Processing
- The PDF is loaded and split into manageable chunks
- Each chunk is embedded using HuggingFace models
- Embeddings are stored in ChromaDB for fast retrieval

### Query Processing
1. User submits a question
2. System searches the document using BM25 + vector search ensemble
3. If answer found: Returns answer from document
4. If not found: Tries alternative retrieval strategy (corrective RAG)
5. If still not found: Performs Tavily web search with user notification
6. If web search fails: Returns "yet to be enhanced" message

### Web Search Fallback
When the answer is not available in the PDF:
- System displays: "Answer is not available in uploaded document, let me search it in web and see if I can help"
- Performs Tavily web search (requires API key)
- Returns web results with sources or "yet to be enhanced" message

## File Structure

```
.
├── app.py              # Main Streamlit application
├── .env                # Environment variables (API keys)
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── dms-ug.pdf         # Your PDF document
└── chroma_db/         # ChromaDB storage (created automatically)
```

## Requirements

- Python 3.8+
- OpenAI API key (required)
- Tavily API key (optional, for web search)

## Notes

- The application uses HuggingFace's sentence-transformers as text-embedding-ada-002 equivalent
- BM25 reranking improves retrieval accuracy by combining keyword and semantic search
- Web search is optional and requires Tavily API key
- All data is processed locally except for LLM and web search API calls
- Tavily is easier to set up than Google Search API and works great on Windows

## Troubleshooting

**Issue**: PDF not loading
- Ensure `dms-ug.pdf` is in the same directory as `app.py`

**Issue**: Installation errors on Windows
- Run: `python.exe -m pip install --upgrade pip`
- Then: `pip install -r requirements.txt`
- The packages will install pre-built wheels (no compilation needed)

**Issue**: Web search not working
- Configure `TAVILY_API_KEY` in `.env` file
- Web search is optional; the app works without it

**Issue**: Embedding errors
- First run downloads the HuggingFace model (may take time)
- Ensure stable internet connection for initial setup

## License

This project is provided as-is for educational and commercial use.
