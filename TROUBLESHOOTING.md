# Troubleshooting Guide

Common issues and their solutions when working with the Oracle Metadata Knowledge Graph.

## Table of Contents
1. [Installation Issues](#installation-issues)
2. [Docker Issues](#docker-issues)
3. [Neo4j Issues](#neo4j-issues)
4. [Python Issues](#python-issues)
5. [OpenAI API Issues](#openai-api-issues)
6. [Oracle Connection Issues](#oracle-connection-issues)
7. [Query Issues](#query-issues)

---

## Installation Issues

### Python not found

**Error**: `'python' is not recognized as an internal or external command`

**Solution**:
1. Reinstall Python from https://www.python.org/downloads/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

### pip not working

**Error**: `'pip' is not recognized`

**Solution**:
```cmd
python -m pip --version
```

If that works, use `python -m pip install` instead of `pip install`.

### Virtual environment activation fails

**Error**: Script execution disabled

**Solution** (Windows PowerShell):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:
```cmd
venv\Scripts\activate
```

---

## Docker Issues

### Docker not found

**Error**: `'docker' is not recognized`

**Solution**:
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop/
2. Restart your computer
3. Start Docker Desktop
4. Verify: `docker --version`

### Docker daemon not running

**Error**: `Cannot connect to the Docker daemon`

**Solution**:
1. Open Docker Desktop application
2. Wait for it to fully start (whale icon in system tray)
3. Try command again

### Port already in use

**Error**: `Bind for 0.0.0.0:7474 failed: port is already allocated`

**Solution**:

Check what's using the port:
```cmd
netstat -ano | findstr :7474
netstat -ano | findstr :7687
```

Stop the conflicting service or change ports in `docker-compose.yml`:
```yaml
ports:
  - "7475:7474"  # Changed from 7474
  - "7688:7687"  # Changed from 7687
```

Then update `.env`:
```
NEO4J_URI=bolt://localhost:7688
```

### Docker compose not found

**Error**: `docker-compose: command not found`

**Solution**:

Try with hyphen:
```cmd
docker compose up -d
```

Or install docker-compose separately.

---

## Neo4j Issues

### Cannot connect to Neo4j

**Error**: `ServiceUnavailable: Unable to connect to localhost:7687`

**Solutions**:

1. **Wait longer**: Neo4j takes 20-30 seconds to start
   ```cmd
   docker-compose logs -f
   ```
   Wait for "Started" message

2. **Check container is running**:
   ```cmd
   docker ps
   ```
   Should see `oracle-metadata-neo4j` container

3. **Restart Neo4j**:
   ```cmd
   docker-compose down
   docker-compose up -d
   ```

4. **Check logs for errors**:
   ```cmd
   docker-compose logs
   ```

### Authentication failed

**Error**: `AuthError: The client is unauthorized`

**Solution**:

Check credentials in `.env`:
```
NEO4J_USER=neo4j
NEO4J_PASSWORD=password123
```

These must match `docker-compose.yml`:
```yaml
NEO4J_AUTH=neo4j/password123
```

### Neo4j Browser won't load

**Error**: Browser shows "Unable to connect"

**Solutions**:

1. **Check Neo4j is running**:
   ```cmd
   docker ps
   ```

2. **Try different browser**: Chrome, Firefox, Edge

3. **Clear browser cache**

4. **Check firewall**: Allow port 7474

5. **Restart Neo4j**:
   ```cmd
   docker-compose restart
   ```

### Database is empty

**Error**: No nodes found in Neo4j Browser

**Solution**:

Run the build script:
```cmd
python src/build_graph.py
```

Verify data exists:
```cypher
MATCH (n) RETURN count(n)
```

---

## Python Issues

### Module not found

**Error**: `ModuleNotFoundError: No module named 'neo4j'`

**Solutions**:

1. **Activate virtual environment**:
   ```cmd
   venv\Scripts\activate
   ```
   You should see `(venv)` in prompt

2. **Install dependencies**:
   ```cmd
   pip install -r requirements.txt
   ```

3. **Force reinstall**:
   ```cmd
   pip install -r requirements.txt --force-reinstall
   ```

### Import errors

**Error**: `ImportError: cannot import name 'ChatOpenAI'`

**Solution**:

Update packages:
```cmd
pip install --upgrade langchain langchain-openai langchain-community
```

### Python version too old

**Error**: `SyntaxError` or version warnings

**Solution**:

Check Python version:
```cmd
python --version
```

Must be 3.9 or higher. If not, install newer Python.

---

## OpenAI API Issues

### Invalid API key

**Error**: `AuthenticationError: Incorrect API key`

**Solutions**:

1. **Check `.env` file**:
   - No extra spaces around the key
   - Key starts with `sk-`
   - File is named `.env` not `.env.txt`

2. **Verify key is valid**:
   - Go to https://platform.openai.com/api-keys
   - Check key is active
   - Create new key if needed

3. **Check environment variable loaded**:
   ```python
   import os
   from dotenv import load_dotenv
   load_dotenv()
   print(os.getenv('OPENAI_API_KEY'))
   ```

### Rate limit exceeded

**Error**: `RateLimitError: Rate limit reached`

**Solution**:

1. Wait a few minutes
2. Check usage: https://platform.openai.com/usage
3. Upgrade plan if needed
4. Reduce query frequency

### Insufficient credits

**Error**: `InsufficientQuotaError: You exceeded your current quota`

**Solution**:

1. Add billing: https://platform.openai.com/account/billing
2. Add payment method
3. Purchase credits
4. Wait a few minutes for activation

### Model not found

**Error**: `InvalidRequestError: The model 'gpt-4' does not exist`

**Solution**:

Change model in `src/query_graph.py`:
```python
llm = ChatOpenAI(
    temperature=0,
    model="gpt-3.5-turbo",  # Changed from gpt-4
    openai_api_key=os.getenv('OPENAI_API_KEY')
)
```

---

## Oracle Connection Issues

### Cannot connect to Oracle

**Error**: `DatabaseError: ORA-12541: TNS:no listener`

**Solutions**:

1. **Check Oracle is running**

2. **Verify connection details in `.env`**:
   ```
   ORACLE_HOST=localhost
   ORACLE_PORT=1521
   ORACLE_SERVICE_NAME=ORCL
   ORACLE_USER=your_username
   ORACLE_PASSWORD=your_password
   ```

3. **Test connection**:
   ```python
   import oracledb
   conn = oracledb.connect(
       user="username",
       password="password",
       host="localhost",
       port=1521,
       service_name="ORCL"
   )
   print("Connected!")
   conn.close()
   ```

4. **Use sample data instead**:
   ```cmd
   python src/sample_metadata.py
   ```

### Oracle client not installed

**Error**: `DPI-1047: Cannot locate a 64-bit Oracle Client library`

**Solution**:

The `oracledb` package in thin mode doesn't need Oracle Client. Ensure you're using:
```python
import oracledb
# Don't call oracledb.init_oracle_client()
```

If you need thick mode, install Oracle Instant Client.

### Permission denied

**Error**: `ORA-01031: insufficient privileges`

**Solution**:

User needs SELECT privileges on system tables:
```sql
GRANT SELECT ANY DICTIONARY TO your_user;
```

Or use a user with DBA role.

---

## Query Issues

### Cypher syntax error

**Error**: `Invalid input 'X': expected...`

**Solution**:

1. **Check Cypher syntax**: https://neo4j.com/docs/cypher-manual/

2. **Use Neo4j Browser** to test queries first

3. **Common mistakes**:
   - Missing quotes around strings
   - Wrong relationship direction
   - Typo in node labels or properties

### No results returned

**Error**: Query runs but returns empty

**Solutions**:

1. **Verify data exists**:
   ```cypher
   MATCH (n) RETURN count(n)
   ```

2. **Check node labels**:
   ```cypher
   CALL db.labels()
   ```

3. **Check property names**:
   ```cypher
   MATCH (t:Table) RETURN keys(t) LIMIT 1
   ```

4. **Simplify query**:
   ```cypher
   MATCH (t:Table) RETURN t LIMIT 5
   ```

### LangChain query fails

**Error**: Query doesn't generate correct Cypher

**Solutions**:

1. **Be more specific** in your question

2. **Use direct Cypher** instead:
   ```python
   agent.run_cypher("MATCH (t:Table) RETURN t.name")
   ```

3. **Check schema is loaded**:
   ```python
   print(agent.graph.schema)
   ```

4. **Adjust prompt** in `src/query_graph.py`

### Timeout errors

**Error**: Query takes too long

**Solutions**:

1. **Add LIMIT** to queries:
   ```cypher
   MATCH (t:Table) RETURN t LIMIT 25
   ```

2. **Create indexes**:
   ```cypher
   CREATE INDEX table_name_idx FOR (t:Table) ON (t.name)
   ```

3. **Optimize query**:
   - Use specific node labels
   - Filter early in the query
   - Avoid Cartesian products

---

## General Debugging Tips

### Enable verbose logging

Add to your Python scripts:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check all services are running

```cmd
# Docker
docker ps

# Neo4j
# Open http://localhost:7474

# Python environment
python --version
pip list
```

### Reset everything

```cmd
# Stop and remove Neo4j
docker-compose down -v

# Deactivate Python environment
deactivate

# Start fresh
venv\Scripts\activate
docker-compose up -d
python src/sample_metadata.py
python src/build_graph.py
```

### Get help

1. Check logs:
   ```cmd
   docker-compose logs
   ```

2. Check Neo4j Browser console (F12)

3. Run with verbose mode:
   ```cmd
   python src/query_graph.py --verbose
   ```

4. Test components individually:
   - Test Neo4j connection
   - Test OpenAI API
   - Test metadata extraction
   - Test graph building

---

## Still Having Issues?

1. **Check Prerequisites**:
   - Python 3.9+ installed
   - Docker Desktop running
   - OpenAI API key valid
   - `.env` file configured

2. **Review Documentation**:
   - README.md
   - WINDOWS_SETUP.md
   - ARCHITECTURE.md

3. **Test with Sample Data**:
   - Use `sample_metadata.py` instead of real Oracle
   - Eliminates Oracle connection issues

4. **Simplify**:
   - Test one component at a time
   - Use Neo4j Browser for direct queries
   - Run example queries first

5. **Check Versions**:
   ```cmd
   python --version
   docker --version
   pip list
   ```
