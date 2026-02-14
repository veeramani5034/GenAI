# AWS DynamoDB Document Explorer

A Streamlit-based RAG (Retrieval Augmented Generation) application for exploring AWS DynamoDB documentation with multimodal support for images.

## Features

- **PDF Document Processing**: Automatically loads and processes PDF documents
- **Vector Search**: Uses Chroma DB for efficient semantic search
- **Multimodal Support**: Extracts and indexes images from PDFs using GPT-4 Vision
- **Hybrid Retrieval**: Combines BM25 (keyword) and vector (semantic) search
- **Corrective RAG**: Falls back to web search when information isn't in the document
- **Image Display**: Shows relevant diagrams, charts, and figures from the PDF
- **Chat Interface**: Interactive Q&A about DynamoDB

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

4. Run the application:
```bash
streamlit run app.py
```

## How It Works

1. **Document Processing**: PDF is split into chunks and embedded using sentence-transformers
2. **Image Extraction**: PyMuPDF extracts images from the PDF
3. **Image Description**: GPT-4 Vision generates detailed descriptions of each image
4. **Vector Storage**: Both text chunks and image descriptions are stored in Chroma DB
5. **Retrieval**: User queries retrieve relevant text and images
6. **Response Generation**: GPT-3.5-turbo generates answers based on retrieved context

## Technologies Used

- **Streamlit**: Web interface
- **LangChain**: RAG framework
- **Chroma DB**: Vector database
- **OpenAI GPT-4o-mini**: Image analysis
- **OpenAI GPT-3.5-turbo**: Text generation
- **PyMuPDF**: PDF image extraction
- **Sentence Transformers**: Text embeddings
- **Tavily**: Web search fallback

## Usage

1. Enter your OpenAI API key in the sidebar
2. The PDF document will be automatically processed
3. Ask questions about DynamoDB in the chat
4. Request images by asking "show me [topic]"

## Example Queries

- "What is PutItem in DynamoDB API?"
- "Show me DynamoDB architecture"
- "Explain DynamoDB timeline"
- "Show me log replica on a log node"
