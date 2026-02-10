# Oracle Metadata to Neo4j Knowledge Graph

Convert Oracle database metadata into a Neo4j graph database using Python, LangChain, and OpenAI for intelligent querying.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.9+** installed
   - Check: `python --version`
   - Download from: https://www.python.org/downloads/

2. **Docker Desktop** installed and running
   - Download from: https://www.docker.com/products/docker-desktop/
   - Verify: `docker --version`

3. **OpenAI API Key**
   - Get one from: https://platform.openai.com/api-keys
   - You'll need billing enabled on your OpenAI account

4. **Oracle Database Access** (optional for testing)
   - Connection details: host, port, service name, username, password
   - Or use the sample metadata provided

## Project Structure

```
oracle-metadata-knowledge-graph/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── docker-compose.yml           # Neo4j setup
├── src/
│   ├── extract_metadata.py     # Extract Oracle metadata
│   ├── build_graph.py          # Build Neo4j knowledge graph
│   ├── query_graph.py          # Query using LangChain + OpenAI
│   └── sample_metadata.py      # Sample data for testing
└── notebooks/
    └── explore_graph.ipynb     # Jupyter notebook for exploration
```

## Step-by-Step Setup

### Step 1: Clone/Create Project Directory

```bash
mkdir oracle-metadata-knowledge-graph
cd oracle-metadata-knowledge-graph
```

### Step 2: Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

**Option A: Standard Installation**
```bash
pip install -r requirements.txt
```

**Option B: If you get errors (Windows)**
```bash
# Try minimal requirements first
pip install -r requirements-minimal.txt

# Or use interactive installer
python install_dependencies.py
```

**Option C: Test your installation**
```bash
python test_install.py
```

See [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) if you encounter installation errors.

### Step 4: Configure Environment Variables

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your credentials:
# - OPENAI_API_KEY
# - Oracle connection details (if using real database)
```

### Step 5: Start Neo4j with Docker

```bash
# Start Neo4j container
docker-compose up -d

# Wait 30 seconds for Neo4j to start
# Access Neo4j Browser at: http://localhost:7474
# Default credentials: neo4j / password123
```

### Step 6: Extract Oracle Metadata

```bash
# Option A: Use sample metadata (no Oracle needed)
python src/sample_metadata.py

# Option B: Extract from real Oracle database
python src/extract_metadata.py
```

### Step 7: Build the Knowledge Graph

```bash
python src/build_graph.py
```

This will create nodes and relationships in Neo4j:
- Tables → Columns
- Tables → Indexes
- Tables → Constraints
- Tables → Foreign Keys
- Columns → Data Types

### Step 8: Query the Knowledge Graph

```bash
# Interactive query mode
python src/query_graph.py

# Example queries:
# - "Show me all tables with more than 10 columns"
# - "What are the foreign key relationships for the EMPLOYEES table?"
# - "Find all indexes on date columns"
```

### Step 9: Explore with Neo4j Browser

1. Open http://localhost:7474
2. Login with: neo4j / password123
3. Try Cypher queries:

```cypher
// View all tables
MATCH (t:Table) RETURN t LIMIT 25

// View table relationships
MATCH (t:Table)-[r]->(c:Column)
WHERE t.name = 'EMPLOYEES'
RETURN t, r, c

// Find all foreign keys
MATCH (t1:Table)-[fk:HAS_FOREIGN_KEY]->(t2:Table)
RETURN t1.name, fk.constraint_name, t2.name
```

## Troubleshooting

### Neo4j won't start
```bash
# Check if port 7474 or 7687 is already in use
docker ps
docker-compose down
docker-compose up -d
```

### Python import errors
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### OpenAI API errors
- Verify your API key in .env
- Check you have credits: https://platform.openai.com/usage
- Ensure no extra spaces in the API key

### Oracle connection issues
- Use sample metadata first to test the pipeline
- Verify Oracle connection details
- Check firewall/network access

## Next Steps

1. **Enhance the Graph**: Add more metadata (views, procedures, triggers)
2. **Add Embeddings**: Use OpenAI embeddings for semantic search
3. **Build RAG Pipeline**: Create a chatbot that answers questions about your schema
4. **Visualize**: Create custom visualizations of your database architecture
5. **Monitor Changes**: Track schema changes over time

## Useful Commands

```bash
# Stop Neo4j
docker-compose down

# View Neo4j logs
docker-compose logs -f

# Reset everything (deletes all data)
docker-compose down -v
docker-compose up -d

# Deactivate Python environment
deactivate
```

## Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [Cypher Query Language](https://neo4j.com/docs/cypher-manual/current/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

## License

MIT License - Feel free to modify and use for your projects.
