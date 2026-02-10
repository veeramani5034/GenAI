# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Oracle Metadata Knowledge Graph              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  Oracle Database │         │  Sample Metadata │
│                  │         │   Generator      │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         │ extract_metadata.py        │ sample_metadata.py
         │                            │
         └────────────┬───────────────┘
                      │
                      ▼
         ┌────────────────────────┐
         │  oracle_metadata.json  │
         │  (Intermediate Format) │
         └────────────┬───────────┘
                      │
                      │ build_graph.py
                      │
                      ▼
         ┌────────────────────────┐
         │      Neo4j Database    │
         │   (Knowledge Graph)    │
         │                        │
         │  Nodes:                │
         │  - Tables              │
         │  - Columns             │
         │  - Indexes             │
         │  - Constraints         │
         │                        │
         │  Relationships:        │
         │  - HAS_COLUMN          │
         │  - HAS_INDEX           │
         │  - HAS_CONSTRAINT      │
         │  - HAS_FOREIGN_KEY     │
         └────────────┬───────────┘
                      │
         ┌────────────┴───────────┐
         │                        │
         ▼                        ▼
┌─────────────────┐    ┌──────────────────┐
│  Neo4j Browser  │    │   query_graph.py │
│  (Cypher Query) │    │   + LangChain    │
│                 │    │   + OpenAI       │
└─────────────────┘    └──────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │ Natural Language│
                       │     Queries     │
                       └─────────────────┘
```

## Data Flow

### 1. Metadata Extraction

```
Oracle DB → SQL Queries → Python Objects → JSON File
```

**Files involved:**
- `src/extract_metadata.py` - Queries Oracle system tables
- `src/sample_metadata.py` - Generates sample data
- `data/oracle_metadata.json` - Output file

### 2. Graph Building

```
JSON File → Python Parser → Neo4j Cypher → Graph Database
```

**Files involved:**
- `src/build_graph.py` - Reads JSON and creates graph
- Neo4j database - Stores the knowledge graph

### 3. Querying

```
Natural Language → OpenAI → Cypher Query → Neo4j → Results
```

**Files involved:**
- `src/query_graph.py` - LangChain integration
- OpenAI API - Converts NL to Cypher
- Neo4j database - Executes queries

## Neo4j Graph Schema

```
┌─────────────┐
│    Table    │
│─────────────│
│ name        │
│ owner       │
│ tablespace  │
│ num_rows    │
└──────┬──────┘
       │
       │ HAS_COLUMN
       │
       ▼
┌─────────────┐
│   Column    │
│─────────────│
│ name        │
│ data_type   │
│ nullable    │
│ data_length │
│ position    │
└─────────────┘

┌─────────────┐
│    Table    │
└──────┬──────┘
       │
       │ HAS_INDEX
       │
       ▼
┌─────────────┐
│    Index    │
│─────────────│
│ name        │
│ type        │
│ uniqueness  │
│ columns[]   │
└─────────────┘

┌─────────────┐
│    Table    │
└──────┬──────┘
       │
       │ HAS_CONSTRAINT
       │
       ▼
┌─────────────┐
│ Constraint  │
│─────────────│
│ name        │
│ type        │
│ columns[]   │
└─────────────┘

┌─────────────┐         ┌─────────────┐
│   Table A   │────────▶│   Table B   │
└─────────────┘         └─────────────┘
     HAS_FOREIGN_KEY
     (constraint_name, columns[])
```

## Component Details

### 1. Metadata Extraction Layer

**Purpose**: Extract schema information from Oracle

**Components**:
- `extract_metadata.py`: Connects to Oracle and queries system tables
- `sample_metadata.py`: Generates realistic sample data for testing

**Output**: JSON file with structured metadata

### 2. Graph Building Layer

**Purpose**: Transform metadata into graph structure

**Components**:
- `build_graph.py`: Reads JSON and creates Neo4j nodes/relationships

**Process**:
1. Clear existing graph
2. Create Table nodes
3. Create Column nodes and link to tables
4. Create Index nodes and link to tables/columns
5. Create Constraint nodes and link to tables
6. Create foreign key relationships between tables
7. Create Neo4j indexes for performance

### 3. Query Layer

**Purpose**: Enable natural language queries

**Components**:
- `query_graph.py`: LangChain + OpenAI integration
- Neo4j Browser: Direct Cypher queries

**Process**:
1. User asks question in natural language
2. OpenAI converts to Cypher query
3. Neo4j executes Cypher query
4. Results returned to user

### 4. Exploration Layer

**Purpose**: Interactive data exploration

**Components**:
- Jupyter notebook: `notebooks/explore_graph.ipynb`
- Pandas for data manipulation
- Matplotlib/NetworkX for visualization

## Technology Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Database | Neo4j 5.15 | Graph database storage |
| Language | Python 3.9+ | Application logic |
| AI | OpenAI GPT-4 | Natural language processing |
| Framework | LangChain | LLM orchestration |
| Container | Docker | Neo4j deployment |

### Python Libraries

| Library | Purpose |
|---------|---------|
| neo4j | Neo4j driver |
| langchain | LLM framework |
| langchain-openai | OpenAI integration |
| oracledb | Oracle database connector |
| pandas | Data manipulation |
| python-dotenv | Environment variables |
| jupyter | Interactive notebooks |

## Deployment Architecture

```
┌─────────────────────────────────────────┐
│           Local Machine                  │
│                                          │
│  ┌────────────────────────────────┐     │
│  │     Python Application         │     │
│  │  - extract_metadata.py         │     │
│  │  - build_graph.py              │     │
│  │  - query_graph.py              │     │
│  └────────────┬───────────────────┘     │
│               │                          │
│               │ Neo4j Driver             │
│               │                          │
│  ┌────────────▼───────────────────┐     │
│  │      Docker Container          │     │
│  │                                │     │
│  │  ┌──────────────────────────┐ │     │
│  │  │   Neo4j Database         │ │     │
│  │  │   Port: 7474 (HTTP)      │ │     │
│  │  │   Port: 7687 (Bolt)      │ │     │
│  │  └──────────────────────────┘ │     │
│  └────────────────────────────────┘     │
│                                          │
│  ┌────────────────────────────────┐     │
│  │      Web Browser               │     │
│  │  - Neo4j Browser (localhost)   │     │
│  │  - Jupyter Notebook            │     │
│  └────────────────────────────────┘     │
└─────────────────────────────────────────┘
         │
         │ HTTPS
         │
         ▼
┌─────────────────┐
│  OpenAI API     │
│  (Cloud)        │
└─────────────────┘
```

## Security Considerations

1. **API Keys**: Stored in `.env` file (not committed to git)
2. **Neo4j Authentication**: Username/password authentication
3. **Network**: All services run locally by default
4. **Data**: No sensitive data sent to OpenAI (only schema metadata)

## Scalability

### Current Setup (Development)
- Single Neo4j instance
- Local Docker container
- Suitable for: 100s of tables, 1000s of columns

### Production Considerations
- Neo4j Enterprise for clustering
- Separate Neo4j server
- Connection pooling
- Caching layer
- API gateway for queries

## Extension Points

1. **Additional Metadata**:
   - Views, procedures, triggers
   - Partitions, materialized views
   - Statistics, execution plans

2. **Enhanced Queries**:
   - Semantic search with embeddings
   - Query optimization suggestions
   - Impact analysis

3. **Visualization**:
   - Custom graph visualizations
   - ER diagrams
   - Dependency graphs

4. **Integration**:
   - CI/CD pipeline integration
   - Schema change tracking
   - Documentation generation
