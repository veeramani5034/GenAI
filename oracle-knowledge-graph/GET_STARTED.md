# Get Started - Quick Guide

**Having installation issues? You're in the right place!**

## What Happened?

You got an error like:
```
error: subprocess-exited-with-error
× pip subprocess to install build dependencies did not run successfully.
```

This is common on Windows when packages need to compile C extensions.

## Quick Fix (3 Steps)

### 1. Use the Interactive Installer

```cmd
python install_dependencies.py
```

This will:
- Install packages one by one
- Skip problematic ones
- Tell you exactly what worked

### 2. Test Your Installation

```cmd
python test_install.py
```

This checks if everything is working.

### 3. Start Using It

```cmd
# Configure environment
copy .env.example .env
# Edit .env and add your OpenAI API key

# Start Neo4j
docker-compose up -d

# Generate sample data
python src/sample_metadata.py

# Build knowledge graph
python src/build_graph.py

# Query it!
python src/query_graph.py
```

## Alternative: Minimal Installation

If the interactive installer doesn't work:

```cmd
pip install -r requirements-minimal.txt
```

This installs only core packages without optional ones.

## What You Need vs What's Optional

### Required (Must Have):
- ✓ `neo4j` - Database driver
- ✓ `openai` - AI API
- ✓ `langchain` - AI framework
- ✓ `python-dotenv` - Config

### Optional (Nice to Have):
- `pandas` - Data manipulation
- `jupyter` - Notebooks
- `oracledb` - Oracle connector (only if using real Oracle)

**You can skip optional packages and still use the project!**

## Still Not Working?

### Option 1: Install Build Tools
Download and install: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Then try again:
```cmd
pip install -r requirements.txt
```

### Option 2: Skip Oracle Connector
The `oracledb` package often causes issues. You don't need it!

Use `sample_metadata.py` instead of `extract_metadata.py`.

### Option 3: Use Neo4j Browser Only
You can build the graph and query it directly in Neo4j Browser without Python queries:

1. Install minimal packages:
   ```cmd
   pip install neo4j python-dotenv
   ```

2. Build the graph:
   ```cmd
   python src/sample_metadata.py
   python src/build_graph.py
   ```

3. Query in browser:
   - Open http://localhost:7474
   - Use Cypher queries (see QUICK_REFERENCE.md)

## Documentation Guide

Depending on your issue, check:

| Problem | Read This |
|---------|-----------|
| Installation errors | [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) |
| General setup | [README.md](README.md) |
| Windows-specific | [WINDOWS_SETUP.md](WINDOWS_SETUP.md) |
| Any error | [TROUBLESHOOTING.md](TROUBLESHOOTING.md) |
| Quick commands | [QUICK_REFERENCE.md](QUICK_REFERENCE.md) |
| Understanding system | [ARCHITECTURE.md](ARCHITECTURE.md) |
| File locations | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) |

## Fastest Path to Success

1. **Don't worry about Oracle** - Use sample data
2. **Skip optional packages** - Install only what's needed
3. **Test as you go** - Run `test_install.py` after installing
4. **Use Neo4j Browser** - It's easier than Python queries at first

## Minimal Working Setup

Here's the absolute minimum to get started:

```cmd
# 1. Install only core packages
pip install neo4j python-dotenv

# 2. Create .env file
copy .env.example .env
# (You can skip OpenAI key for now)

# 3. Start Neo4j
docker-compose up -d

# 4. Generate and load data
python src/sample_metadata.py
python src/build_graph.py

# 5. Open Neo4j Browser
# Go to: http://localhost:7474
# Login: neo4j / password123

# 6. Try a query
# In Neo4j Browser, run:
MATCH (t:Table) RETURN t.name LIMIT 10
```

**That's it! You now have a working knowledge graph.**

You can add LangChain and OpenAI later when you want AI-powered queries.

## Next Steps After Basic Setup

Once you have the basic setup working:

1. **Add OpenAI for AI queries**:
   ```cmd
   pip install openai langchain langchain-openai langchain-community
   python src/query_graph.py
   ```

2. **Add Jupyter for exploration**:
   ```cmd
   pip install jupyter
   jupyter notebook
   # Open notebooks/explore_graph.ipynb
   ```

3. **Connect to real Oracle** (if needed):
   ```cmd
   pip install oracledb
   # Edit .env with Oracle credentials
   python src/extract_metadata.py
   ```

## Common Questions

**Q: Do I need Oracle database?**
A: No! Use `sample_metadata.py` to generate sample data.

**Q: Do I need all the packages?**
A: No! Core functionality needs only: neo4j, python-dotenv, openai, langchain.

**Q: Can I use this without Python?**
A: Partially. You can build the graph with Python, then query it in Neo4j Browser.

**Q: What if oracledb won't install?**
A: Skip it! Use `sample_metadata.py` instead.

**Q: Do I need Jupyter?**
A: No, it's optional for interactive exploration.

## Help Commands

```cmd
# Test what's installed
python test_install.py

# Install interactively
python install_dependencies.py

# Quick start everything
python quick_start.py

# Check if Neo4j is running
docker ps

# View Neo4j logs
docker-compose logs
```

## Success Checklist

- [ ] Python 3.9+ installed
- [ ] Docker Desktop installed and running
- [ ] Virtual environment created and activated
- [ ] Core packages installed (test with `test_install.py`)
- [ ] .env file created
- [ ] Neo4j started (`docker-compose up -d`)
- [ ] Sample data generated (`python src/sample_metadata.py`)
- [ ] Graph built (`python src/build_graph.py`)
- [ ] Can access Neo4j Browser (http://localhost:7474)

If you can check all these boxes, you're ready to go!

## Get Help

1. Run `python test_install.py` to diagnose issues
2. Check [INSTALL_WINDOWS.md](INSTALL_WINDOWS.md) for detailed fixes
3. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for specific errors
4. Use minimal installation if full installation fails

**Remember: You don't need everything to get started. Start minimal, add features later!**
