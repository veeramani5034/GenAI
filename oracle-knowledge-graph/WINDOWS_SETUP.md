# Windows Setup Guide

Complete step-by-step guide for setting up the Oracle Metadata Knowledge Graph on Windows.

## Prerequisites Installation

### 1. Install Python 3.9+

1. Download Python from: https://www.python.org/downloads/
2. Run the installer
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

### 2. Install Docker Desktop

1. Download from: https://www.docker.com/products/docker-desktop/
2. Run the installer
3. Restart your computer if prompted
4. Start Docker Desktop
5. Verify installation:
   ```cmd
   docker --version
   ```

### 3. Get OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (you'll need it later)
5. Add billing information at: https://platform.openai.com/account/billing

## Project Setup

### Step 1: Create Project Directory

```cmd
mkdir oracle-metadata-knowledge-graph
cd oracle-metadata-knowledge-graph
```

### Step 2: Download/Clone Project Files

Place all project files in the directory you just created.

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

### Step 4: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Python Dependencies

```cmd
pip install -r requirements.txt
```

This will take a few minutes. Wait for it to complete.

### Step 6: Configure Environment Variables

```cmd
copy .env.example .env
```

Now edit the `.env` file:
1. Open `.env` in Notepad or any text editor
2. Replace `your_openai_api_key_here` with your actual OpenAI API key
3. Save the file

Example `.env` file:
```
OPENAI_API_KEY=sk-proj-abc123xyz...
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
USE_SAMPLE_DATA=true
```

### Step 7: Start Neo4j

Make sure Docker Desktop is running, then:

```cmd
docker-compose up -d
```

Wait 30 seconds for Neo4j to start.

### Step 8: Verify Neo4j is Running

Open your browser and go to: http://localhost:7474

Login with:
- Username: `neo4j`
- Password: `password123`

## Running the Pipeline

### Option A: Quick Start (Automated)

```cmd
python quick_start.py
```

This will automatically:
1. Check prerequisites
2. Start Neo4j
3. Generate sample metadata
4. Build the knowledge graph

### Option B: Manual Steps

#### 1. Generate Sample Metadata

```cmd
python src/sample_metadata.py
```

This creates a `data/oracle_metadata.json` file with sample HR schema.

#### 2. Build Knowledge Graph

```cmd
python src/build_graph.py
```

This loads the metadata into Neo4j.

#### 3. Query the Graph

Interactive mode:
```cmd
python src/query_graph.py
```

Run example queries:
```cmd
python src/query_graph.py --examples
```

Single query:
```cmd
python src/query_graph.py --query "Show me all tables"
```

## Using Real Oracle Database (Optional)

If you have access to an Oracle database:

1. Edit `.env` file and add Oracle connection details:
   ```
   ORACLE_HOST=your-oracle-host
   ORACLE_PORT=1521
   ORACLE_SERVICE_NAME=ORCL
   ORACLE_USER=your_username
   ORACLE_PASSWORD=your_password
   USE_SAMPLE_DATA=false
   ```

2. Extract metadata:
   ```cmd
   python src/extract_metadata.py
   ```

3. Build graph:
   ```cmd
   python src/build_graph.py
   ```

## Using Jupyter Notebook

### Start Jupyter

```cmd
jupyter notebook
```

This will open Jupyter in your browser.

### Open the Exploration Notebook

Navigate to `notebooks/explore_graph.ipynb` and open it.

Run cells one by one to explore the graph.

## Common Issues and Solutions

### Issue: "python is not recognized"

**Solution**: Python is not in your PATH. Reinstall Python and check "Add Python to PATH".

### Issue: "docker is not recognized"

**Solution**: Docker Desktop is not installed or not in PATH. Restart your computer after installing Docker Desktop.

### Issue: Neo4j won't start

**Solution**:
```cmd
docker-compose down
docker-compose up -d
```

Check if ports 7474 or 7687 are already in use:
```cmd
netstat -ano | findstr :7474
netstat -ano | findstr :7687
```

### Issue: "Cannot connect to Neo4j"

**Solution**: 
1. Make sure Docker Desktop is running
2. Wait 30 seconds after starting Neo4j
3. Check Neo4j logs:
   ```cmd
   docker-compose logs
   ```

### Issue: OpenAI API errors

**Solutions**:
- Verify your API key in `.env` (no extra spaces)
- Check you have credits: https://platform.openai.com/usage
- Ensure billing is set up

### Issue: Module not found errors

**Solution**:
```cmd
pip install -r requirements.txt --force-reinstall
```

Make sure virtual environment is activated (you should see `(venv)` in prompt).

## Useful Commands

### Stop Neo4j
```cmd
docker-compose down
```

### Restart Neo4j
```cmd
docker-compose restart
```

### View Neo4j logs
```cmd
docker-compose logs -f
```

### Reset everything (deletes all data)
```cmd
docker-compose down -v
docker-compose up -d
```

### Deactivate virtual environment
```cmd
deactivate
```

### Activate virtual environment (if closed terminal)
```cmd
cd oracle-metadata-knowledge-graph
venv\Scripts\activate
```

## Next Steps

1. **Explore Neo4j Browser**: http://localhost:7474
   - Try Cypher queries
   - Visualize relationships
   - Browse the schema

2. **Run Natural Language Queries**:
   ```cmd
   python src/query_graph.py
   ```

3. **Explore with Jupyter**:
   ```cmd
   jupyter notebook
   ```
   Open `notebooks/explore_graph.ipynb`

4. **Connect to Real Oracle Database**:
   - Update `.env` with Oracle credentials
   - Run `python src/extract_metadata.py`

5. **Customize**:
   - Modify queries in `src/query_graph.py`
   - Add more metadata extraction in `src/extract_metadata.py`
   - Create custom visualizations in Jupyter

## Example Cypher Queries

Try these in Neo4j Browser (http://localhost:7474):

```cypher
// View all tables
MATCH (t:Table) RETURN t LIMIT 25

// View table with columns
MATCH (t:Table {name: 'EMPLOYEES'})-[:HAS_COLUMN]->(c:Column)
RETURN t, c

// Find foreign key relationships
MATCH (t1:Table)-[fk:HAS_FOREIGN_KEY]->(t2:Table)
RETURN t1.name, fk.constraint_name, t2.name

// Tables with most columns
MATCH (t:Table)-[:HAS_COLUMN]->(c:Column)
WITH t, count(c) as col_count
RETURN t.name, col_count
ORDER BY col_count DESC

// Find all indexes
MATCH (t:Table)-[:HAS_INDEX]->(i:Index)
RETURN t.name, i.name, i.uniqueness, i.columns
```

## Support

If you encounter issues:
1. Check this guide's troubleshooting section
2. Review the main README.md
3. Check Docker Desktop is running
4. Verify all prerequisites are installed
5. Ensure `.env` file is configured correctly

## Resources

- [Neo4j Documentation](https://neo4j.com/docs/)
- [Python Documentation](https://docs.python.org/3/)
- [Docker Documentation](https://docs.docker.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
