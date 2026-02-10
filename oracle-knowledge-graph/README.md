# Oracle Metadata to Neo4j Knowledge Graph

Convert Oracle database metadata into a Neo4j graph database using Python, LangChain, and OpenAI for intelligent querying.

## 🚀 Quick Start

**No Oracle database required!** This project includes sample data generation.

### Prerequisites

- Python 3.9+
- Docker Desktop (for Neo4j)
- OpenAI API Key

### Installation

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Install dependencies
pip install -r requirements.txt
# Or for minimal install: pip install -r requirements-minimal.txt

# 3. Configure environment
copy .env.example .env
# Edit .env and add your OpenAI API key

# 4. Start Neo4j
docker-compose up -d

# 5. Generate sample data (no Oracle needed!)
python src/sample_metadata.py

# 6. Build knowledge graph
python src/build_graph.py

# 7. Query with AI
python src/query_graph.py
```

## 📚 Documentation

- **[GET_STARTED.md](GET_STARTED.md)** - Quick start guide with troubleshooting
- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Detailed Windows setup
- **[INSTALL_WINDOWS.md](INSTALL_WINDOWS.md)** - Installation troubleshooting
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues

## 🎯 Features

- ✅ **No Oracle Required** - Uses sample HR schema data
- ✅ **Neo4j Knowledge Graph** - Visual database relationships
- ✅ **AI-Powered Queries** - Natural language questions via LangChain + OpenAI
- ✅ **Docker Setup** - Easy Neo4j deployment
- ✅ **Jupyter Notebooks** - Interactive exploration
- ✅ **Complete Documentation** - Step-by-step guides

## 📁 Project Structure

```
oracle-knowledge-graph/
├── src/
│   ├── sample_metadata.py      # Generate sample data
│   ├── extract_metadata.py     # Extract from real Oracle
│   ├── build_graph.py          # Build Neo4j graph
│   └── query_graph.py          # AI-powered queries
├── notebooks/
│   └── explore_graph.ipynb     # Jupyter exploration
├── docker-compose.yml          # Neo4j setup
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🔍 Example Queries

Once set up, ask questions like:
- "Show me all tables"
- "What columns does the EMPLOYEES table have?"
- "Which tables have foreign keys?"
- "Find all indexes on date columns"

## 🌐 Access Points

- **Neo4j Browser**: http://localhost:7474 (neo4j / password123)
- **Python Queries**: `python src/query_graph.py`
- **Jupyter**: `jupyter notebook` → `notebooks/explore_graph.ipynb`

## 🛠️ Troubleshooting

Having issues? Check:
1. [GET_STARTED.md](GET_STARTED.md) - Quick fixes
2. [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) - Installation help
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Detailed solutions
