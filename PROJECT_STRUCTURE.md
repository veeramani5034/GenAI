# Project Structure

Complete overview of all files and directories in the Oracle Metadata Knowledge Graph project.

## Directory Tree

```
oracle-metadata-knowledge-graph/
│
├── README.md                          # Main documentation
├── WINDOWS_SETUP.md                   # Windows-specific setup guide
├── ARCHITECTURE.md                    # System architecture documentation
├── TROUBLESHOOTING.md                 # Common issues and solutions
├── PROJECT_STRUCTURE.md               # This file
│
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .env                              # Your environment variables (create this)
├── .gitignore                        # Git ignore rules
│
├── docker-compose.yml                # Neo4j Docker configuration
├── quick_start.py                    # Automated setup script
│
├── src/                              # Source code directory
│   ├── sample_metadata.py            # Generate sample Oracle metadata
│   ├── extract_metadata.py           # Extract from real Oracle database
│   ├── build_graph.py                # Build Neo4j knowledge graph
│   └── query_graph.py                # Query graph with LangChain + OpenAI
│
├── notebooks/                        # Jupyter notebooks
│   └── explore_graph.ipynb           # Interactive graph exploration
│
├── data/                             # Data directory (created automatically)
│   └── oracle_metadata.json          # Extracted metadata (generated)
│
└── files/                            # Additional files
    └── aurora_postgresql_cover_letter.txt  # Cover letter (from earlier)
```

## File Descriptions

### Root Level Files

#### README.md
- **Purpose**: Main project documentation
- **Contains**:
  - Project overview
  - Prerequisites
  - Step-by-step setup instructions
  - Usage examples
  - Troubleshooting basics
  - Resources and links

#### WINDOWS_SETUP.md
- **Purpose**: Detailed Windows-specific setup guide
- **Contains**:
  - Windows command syntax
  - Installation instructions for Windows
  - Common Windows-specific issues
  - PowerShell vs CMD differences

#### ARCHITECTURE.md
- **Purpose**: Technical architecture documentation
- **Contains**:
  - System architecture diagrams
  - Data flow explanations
  - Neo4j graph schema
  - Component details
  - Technology stack
  - Deployment architecture

#### TROUBLESHOOTING.md
- **Purpose**: Comprehensive troubleshooting guide
- **Contains**:
  - Common errors and solutions
  - Installation issues
  - Docker problems
  - Neo4j connection issues
  - Python errors
  - OpenAI API problems
  - Debugging tips

#### PROJECT_STRUCTURE.md
- **Purpose**: Project organization reference
- **Contains**:
  - Directory tree
  - File descriptions
  - Purpose of each component

### Configuration Files

#### requirements.txt
- **Purpose**: Python package dependencies
- **Contains**:
  ```
  neo4j==5.16.0
  langchain==0.1.0
  langchain-openai==0.0.2
  langchain-community==0.0.10
  python-dotenv==1.0.0
  oracledb==2.0.0
  pandas==2.1.4
  openai==1.7.2
  jupyter==1.0.0
  ipykernel==6.28.0
  ```

#### .env.example
- **Purpose**: Template for environment variables
- **Contains**:
  - OpenAI API key placeholder
  - Neo4j connection settings
  - Oracle database settings
  - Application configuration

#### .env
- **Purpose**: Your actual environment variables
- **Note**: Create this from .env.example
- **Contains**: Your actual API keys and passwords
- **Security**: Never commit to git (in .gitignore)

#### docker-compose.yml
- **Purpose**: Neo4j Docker container configuration
- **Contains**:
  - Neo4j image version
  - Port mappings (7474, 7687)
  - Environment variables
  - Volume mounts
  - Memory settings

#### .gitignore
- **Purpose**: Files to exclude from git
- **Contains**:
  - Python cache files
  - Virtual environment
  - .env file
  - Data files
  - IDE settings

### Source Code (src/)

#### src/sample_metadata.py
- **Purpose**: Generate sample Oracle metadata
- **Use Case**: Testing without Oracle database
- **Output**: data/oracle_metadata.json
- **Contains**:
  - Sample HR schema (6 tables)
  - Employees, Departments, Jobs, etc.
  - Realistic relationships and constraints

#### src/extract_metadata.py
- **Purpose**: Extract metadata from real Oracle database
- **Use Case**: Production use with actual Oracle
- **Output**: data/oracle_metadata.json
- **Queries**:
  - ALL_TABLES
  - ALL_TAB_COLUMNS
  - ALL_INDEXES
  - ALL_CONSTRAINTS
  - ALL_CONS_COLUMNS

#### src/build_graph.py
- **Purpose**: Build Neo4j knowledge graph
- **Input**: data/oracle_metadata.json
- **Output**: Neo4j graph database
- **Creates**:
  - Table nodes
  - Column nodes
  - Index nodes
  - Constraint nodes
  - Relationships between all nodes

#### src/query_graph.py
- **Purpose**: Query graph with natural language
- **Uses**:
  - LangChain for orchestration
  - OpenAI for NL to Cypher conversion
  - Neo4j for query execution
- **Modes**:
  - Interactive mode
  - Single query mode
  - Example queries mode

### Notebooks (notebooks/)

#### notebooks/explore_graph.ipynb
- **Purpose**: Interactive graph exploration
- **Contains**:
  - Setup and connection code
  - Example queries
  - Data visualization
  - Network graphs
  - Statistical analysis
  - LangChain integration examples

### Utility Scripts

#### quick_start.py
- **Purpose**: Automated setup and execution
- **Does**:
  1. Checks prerequisites
  2. Starts Neo4j
  3. Generates sample metadata
  4. Builds knowledge graph
  5. Provides next steps

### Data Directory (data/)

#### data/oracle_metadata.json
- **Purpose**: Intermediate metadata storage
- **Format**: JSON
- **Structure**:
  ```json
  {
    "tables": [
      {
        "table_name": "...",
        "owner": "...",
        "columns": [...],
        "indexes": [...],
        "constraints": [...]
      }
    ]
  }
  ```
- **Note**: Auto-generated, not in git

## File Dependencies

### Execution Order

1. **Setup Phase**:
   ```
   .env.example → .env (manual copy)
   requirements.txt → pip install
   docker-compose.yml → docker-compose up
   ```

2. **Data Extraction Phase**:
   ```
   sample_metadata.py → data/oracle_metadata.json
   OR
   extract_metadata.py → data/oracle_metadata.json
   ```

3. **Graph Building Phase**:
   ```
   data/oracle_metadata.json → build_graph.py → Neo4j
   ```

4. **Query Phase**:
   ```
   Neo4j + .env → query_graph.py → Results
   ```

### Import Dependencies

```
query_graph.py
├── neo4j
├── langchain
├── langchain_openai
└── python-dotenv

build_graph.py
├── neo4j
├── python-dotenv
└── json

extract_metadata.py
├── oracledb
├── python-dotenv
└── json

sample_metadata.py
└── json
```

## Size Estimates

| File/Directory | Approximate Size |
|---------------|------------------|
| README.md | 8 KB |
| WINDOWS_SETUP.md | 6 KB |
| ARCHITECTURE.md | 10 KB |
| TROUBLESHOOTING.md | 12 KB |
| requirements.txt | 1 KB |
| docker-compose.yml | 1 KB |
| src/*.py | 5-10 KB each |
| notebooks/*.ipynb | 15 KB |
| data/oracle_metadata.json | 10-100 KB (varies) |
| **Total (without data)** | ~100 KB |

## Key Paths

### Configuration
- Environment: `.env`
- Docker: `docker-compose.yml`
- Python deps: `requirements.txt`

### Source Code
- Metadata extraction: `src/extract_metadata.py` or `src/sample_metadata.py`
- Graph building: `src/build_graph.py`
- Querying: `src/query_graph.py`

### Data
- Metadata: `data/oracle_metadata.json`
- Neo4j data: Docker volume (managed by Docker)

### Documentation
- Main: `README.md`
- Windows: `WINDOWS_SETUP.md`
- Architecture: `ARCHITECTURE.md`
- Troubleshooting: `TROUBLESHOOTING.md`

## Adding New Files

### To add new metadata extractors:
1. Create `src/extract_[source].py`
2. Output to `data/[source]_metadata.json`
3. Update `build_graph.py` to handle new format

### To add new query types:
1. Extend `src/query_graph.py`
2. Add new prompt templates
3. Document in README.md

### To add new visualizations:
1. Create new notebook in `notebooks/`
2. Use existing connection code
3. Add visualization libraries to requirements.txt

## Maintenance

### Regular Updates
- Python packages: `pip install --upgrade -r requirements.txt`
- Docker images: `docker-compose pull`
- Neo4j: Update version in docker-compose.yml

### Cleanup
- Remove data: `rm -rf data/`
- Reset Neo4j: `docker-compose down -v`
- Clean Python: `rm -rf __pycache__ *.pyc`

### Backup
- Export graph: Use Neo4j dump
- Save metadata: Copy `data/` directory
- Save config: Backup `.env` file
