# Quick Reference Card

Fast reference for common commands and queries.

## Setup Commands

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your API key

# Start Neo4j
docker-compose up -d

# Quick start (automated)
python quick_start.py
```

## Data Pipeline Commands

```cmd
# Generate sample metadata
python src/sample_metadata.py

# Extract from Oracle (if available)
python src/extract_metadata.py

# Build knowledge graph
python src/build_graph.py

# Query interactively
python src/query_graph.py

# Run example queries
python src/query_graph.py --examples

# Single query
python src/query_graph.py --query "Show me all tables"
```

## Docker Commands

```cmd
# Start Neo4j
docker-compose up -d

# Stop Neo4j
docker-compose down

# Restart Neo4j
docker-compose restart

# View logs
docker-compose logs -f

# Check status
docker ps

# Reset everything (deletes data!)
docker-compose down -v
docker-compose up -d
```

## Neo4j Browser

**URL**: http://localhost:7474

**Login**:
- Username: `neo4j`
- Password: `password123`

## Common Cypher Queries

```cypher
// Count all nodes
MATCH (n) RETURN count(n)

// List all tables
MATCH (t:Table) 
RETURN t.name, t.num_rows 
ORDER BY t.name

// Show table with columns
MATCH (t:Table {name: 'EMPLOYEES'})-[:HAS_COLUMN]->(c:Column)
RETURN t.name, c.name, c.data_type, c.nullable
ORDER BY c.position

// Find foreign keys
MATCH (t1:Table)-[fk:HAS_FOREIGN_KEY]->(t2:Table)
RETURN t1.name as FromTable, 
       fk.constraint_name as Constraint,
       t2.name as ToTable

// Tables with most columns
MATCH (t:Table)-[:HAS_COLUMN]->(c:Column)
WITH t, count(c) as col_count
RETURN t.name, col_count
ORDER BY col_count DESC
LIMIT 10

// Find all indexes
MATCH (t:Table)-[:HAS_INDEX]->(i:Index)
RETURN t.name, i.name, i.uniqueness, i.columns

// Find tables with no foreign keys
MATCH (t:Table)
WHERE NOT (t)-[:HAS_FOREIGN_KEY]->()
RETURN t.name

// Find nullable columns
MATCH (t:Table)-[:HAS_COLUMN]->(c:Column)
WHERE c.nullable = 'Y'
RETURN t.name, c.name, c.data_type

// Find primary keys
MATCH (t:Table)-[:HAS_CONSTRAINT]->(con:Constraint)
WHERE con.type = 'PRIMARY_KEY'
RETURN t.name, con.name, con.columns

// Show full schema for a table
MATCH (t:Table {name: 'EMPLOYEES'})
OPTIONAL MATCH (t)-[:HAS_COLUMN]->(c:Column)
OPTIONAL MATCH (t)-[:HAS_INDEX]->(i:Index)
OPTIONAL MATCH (t)-[:HAS_CONSTRAINT]->(con:Constraint)
OPTIONAL MATCH (t)-[fk:HAS_FOREIGN_KEY]->(t2:Table)
RETURN t, c, i, con, fk, t2

// Find circular foreign key relationships
MATCH path = (t1:Table)-[:HAS_FOREIGN_KEY*2..5]->(t1)
RETURN path
LIMIT 10
```

## Python Quick Examples

### Connect to Neo4j
```python
from neo4j import GraphDatabase
import os
from dotenv import load_dotenv

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv('NEO4J_URI'),
    auth=(os.getenv('NEO4J_USER'), os.getenv('NEO4J_PASSWORD'))
)

with driver.session() as session:
    result = session.run("MATCH (t:Table) RETURN t.name LIMIT 5")
    for record in result:
        print(record['t.name'])

driver.close()
```

### Query with LangChain
```python
from langchain_openai import ChatOpenAI
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
import os
from dotenv import load_dotenv

load_dotenv()

graph = Neo4jGraph(
    url=os.getenv('NEO4J_URI'),
    username=os.getenv('NEO4J_USER'),
    password=os.getenv('NEO4J_PASSWORD')
)

llm = ChatOpenAI(
    temperature=0,
    model="gpt-4",
    openai_api_key=os.getenv('OPENAI_API_KEY')
)

chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph, verbose=True)

result = chain.invoke({"query": "What tables are in the database?"})
print(result['result'])
```

## Natural Language Query Examples

```
"Show me all tables"
"What columns does the EMPLOYEES table have?"
"Which tables have foreign keys?"
"Find all indexes on the EMPLOYEES table"
"What tables have more than 5 columns?"
"Show me the relationships between EMPLOYEES and DEPARTMENTS"
"What are the primary keys in the database?"
"Find all VARCHAR2 columns"
"Which tables have the most foreign key relationships?"
"Show me all unique constraints"
```

## Jupyter Notebook

```cmd
# Start Jupyter
jupyter notebook

# Open notebook
# Navigate to notebooks/explore_graph.ipynb
```

## Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...

# Neo4j (defaults shown)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123

# Oracle (optional)
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=ORCL
ORACLE_USER=username
ORACLE_PASSWORD=password
```

## File Locations

| What | Where |
|------|-------|
| Environment config | `.env` |
| Python source | `src/*.py` |
| Metadata output | `data/oracle_metadata.json` |
| Jupyter notebooks | `notebooks/*.ipynb` |
| Documentation | `*.md` files |

## Troubleshooting Quick Fixes

```cmd
# Can't connect to Neo4j
docker-compose restart

# Module not found
pip install -r requirements.txt --force-reinstall

# Neo4j authentication failed
# Check .env matches docker-compose.yml

# OpenAI API error
# Verify OPENAI_API_KEY in .env

# Port already in use
docker-compose down
# Change ports in docker-compose.yml

# Reset everything
docker-compose down -v
deactivate
venv\Scripts\activate
docker-compose up -d
python src/sample_metadata.py
python src/build_graph.py
```

## Useful URLs

| Service | URL |
|---------|-----|
| Neo4j Browser | http://localhost:7474 |
| Jupyter | http://localhost:8888 |
| OpenAI Platform | https://platform.openai.com |
| Neo4j Docs | https://neo4j.com/docs/ |
| LangChain Docs | https://python.langchain.com/ |

## Graph Statistics Query

```cypher
// Get overview of graph
CALL {
    MATCH (t:Table) RETURN count(t) as tables
}
CALL {
    MATCH (c:Column) RETURN count(c) as columns
}
CALL {
    MATCH (i:Index) RETURN count(i) as indexes
}
CALL {
    MATCH ()-[fk:HAS_FOREIGN_KEY]->() RETURN count(fk) as foreign_keys
}
RETURN tables, columns, indexes, foreign_keys
```

## Performance Tips

1. **Add LIMIT** to queries during development
2. **Use indexes** on frequently queried properties
3. **Filter early** in Cypher queries
4. **Use specific labels** instead of MATCH (n)
5. **Profile queries** with PROFILE or EXPLAIN

## Common Patterns

### Find related tables
```cypher
MATCH (t1:Table {name: 'EMPLOYEES'})-[r]-(t2:Table)
RETURN t1, type(r), t2
```

### Find columns by data type
```cypher
MATCH (c:Column)
WHERE c.data_type = 'DATE'
RETURN c.name, c.data_type
```

### Find tables without indexes
```cypher
MATCH (t:Table)
WHERE NOT (t)-[:HAS_INDEX]->()
RETURN t.name
```

### Export results to CSV (Neo4j Browser)
```cypher
// Run query, then click download icon
MATCH (t:Table)
RETURN t.name, t.num_rows
```

## Keyboard Shortcuts (Neo4j Browser)

| Action | Shortcut |
|--------|----------|
| Run query | Ctrl + Enter |
| Clear editor | Ctrl + K |
| Toggle fullscreen | Ctrl + Shift + F |
| Previous query | Ctrl + Up |
| Next query | Ctrl + Down |

## Next Steps Checklist

- [ ] Install prerequisites (Python, Docker, OpenAI key)
- [ ] Clone/create project directory
- [ ] Set up virtual environment
- [ ] Install dependencies
- [ ] Configure .env file
- [ ] Start Neo4j
- [ ] Generate sample metadata
- [ ] Build knowledge graph
- [ ] Test queries in Neo4j Browser
- [ ] Try natural language queries
- [ ] Explore with Jupyter notebook
- [ ] Connect to real Oracle (optional)

## Getting Help

1. Check TROUBLESHOOTING.md
2. Review WINDOWS_SETUP.md
3. Read ARCHITECTURE.md
4. Check Neo4j logs: `docker-compose logs`
5. Enable verbose mode in Python scripts
