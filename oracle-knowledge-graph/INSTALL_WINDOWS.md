# Windows Installation Fix Guide

If you're getting installation errors, follow these steps.

## Common Error

```
error: subprocess-exited-with-error
× pip subprocess to install build dependencies did not run successfully.
```

This usually means packages need to compile C extensions and you're missing build tools.

## Solution 1: Use Minimal Requirements (Recommended)

Try installing with the minimal requirements file first:

```cmd
pip install -r requirements-minimal.txt
```

This excludes problematic packages and installs only what's needed for core functionality.

## Solution 2: Interactive Installer

Use the interactive installer that handles errors gracefully:

```cmd
python install_dependencies.py
```

This will:
- Install packages one by one
- Skip optional packages if they fail
- Give you a clear summary of what worked

## Solution 3: Install Build Tools

If you need all packages, install Microsoft C++ Build Tools:

### Step 1: Download Build Tools

Go to: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Download "Build Tools for Visual Studio 2022"

### Step 2: Install with C++ Tools

1. Run the installer
2. Select "Desktop development with C++"
3. Install (this takes 5-10 minutes)
4. Restart your computer

### Step 3: Try Again

```cmd
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Solution 4: Install Packages Individually

Try installing packages one at a time to find the problem:

```cmd
# Upgrade pip first
python -m pip install --upgrade pip

# Core packages
pip install python-dotenv
pip install neo4j
pip install openai
pip install pandas

# LangChain
pip install langchain
pip install langchain-openai
pip install langchain-community

# Optional - Jupyter
pip install jupyter

# Optional - Oracle (often fails)
pip install oracledb
```

If `oracledb` fails, skip it and use `sample_metadata.py` instead.

## Solution 5: Use Pre-built Wheels

Some packages have pre-built wheels that don't need compilation:

```cmd
pip install --only-binary :all: pandas
pip install --only-binary :all: neo4j
```

## Verify Installation

Check what's installed:

```cmd
pip list
```

Test imports:

```cmd
python -c "import neo4j; print('neo4j OK')"
python -c "import openai; print('openai OK')"
python -c "import langchain; print('langchain OK')"
python -c "from dotenv import load_dotenv; print('dotenv OK')"
```

## What You Actually Need

### Minimum to run the project:
- `neo4j` - Connect to Neo4j database
- `python-dotenv` - Load environment variables
- `openai` - OpenAI API
- `langchain` + `langchain-openai` + `langchain-community` - AI queries

### Optional:
- `pandas` - Data manipulation (nice to have)
- `jupyter` - Notebooks (only if you want to use notebooks)
- `oracledb` - Oracle connector (only if using real Oracle database)

### Not needed if using sample data:
- `oracledb` - Skip this if you're using `sample_metadata.py`

## Alternative: Use Conda

If pip keeps failing, try Conda:

```cmd
# Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html

# Create environment
conda create -n oracle-graph python=3.11

# Activate
conda activate oracle-graph

# Install packages
conda install -c conda-forge neo4j-python-driver
conda install -c conda-forge pandas
pip install python-dotenv
pip install openai
pip install langchain langchain-openai langchain-community
```

## Still Having Issues?

### Check Python Version
```cmd
python --version
```
Must be 3.9 or higher.

### Check Virtual Environment
Make sure you're in a virtual environment:
```cmd
# You should see (venv) in your prompt
venv\Scripts\activate
```

### Check Disk Space
Make sure you have at least 1GB free space.

### Check Antivirus
Some antivirus software blocks pip installations. Try temporarily disabling it.

### Use Python from Microsoft Store
If you installed Python from python.org, try the Microsoft Store version instead:
1. Open Microsoft Store
2. Search "Python 3.11"
3. Install
4. Try again

## Quick Start Without Full Installation

If you just want to test the concept:

```cmd
# Install only what's absolutely needed
pip install neo4j python-dotenv

# Start Neo4j
docker-compose up -d

# Generate sample data
python src/sample_metadata.py

# Build graph (without LangChain)
python src/build_graph.py

# Use Neo4j Browser for queries
# Open: http://localhost:7474
```

You can add LangChain/OpenAI later when you need AI queries.

## Working Configuration

Here's a configuration that works on most Windows systems:

```cmd
# Upgrade pip
python -m pip install --upgrade pip

# Install in this order
pip install python-dotenv
pip install neo4j>=5.14.0
pip install openai>=1.12.0
pip install langchain>=0.1.0
pip install langchain-openai>=0.0.5
pip install langchain-community>=0.0.20
pip install pandas>=2.0.0

# Skip these if they fail
pip install jupyter  # Optional
pip install oracledb  # Optional
```

## Test Your Installation

Run this test script:

```python
# test_install.py
import sys
print(f"Python: {sys.version}")

try:
    import neo4j
    print("✓ neo4j")
except ImportError:
    print("✗ neo4j - REQUIRED")

try:
    import openai
    print("✓ openai")
except ImportError:
    print("✗ openai - REQUIRED")

try:
    import langchain
    print("✓ langchain")
except ImportError:
    print("✗ langchain - REQUIRED")

try:
    from dotenv import load_dotenv
    print("✓ python-dotenv")
except ImportError:
    print("✗ python-dotenv - REQUIRED")

try:
    import pandas
    print("✓ pandas")
except ImportError:
    print("⚠ pandas - Optional")

try:
    import oracledb
    print("✓ oracledb")
except ImportError:
    print("⚠ oracledb - Optional (use sample_metadata.py)")

try:
    import jupyter
    print("✓ jupyter")
except ImportError:
    print("⚠ jupyter - Optional")

print("\nIf all REQUIRED packages show ✓, you're good to go!")
```

Save as `test_install.py` and run:
```cmd
python test_install.py
```

## Get Help

If nothing works:
1. Check TROUBLESHOOTING.md
2. Make sure Docker Desktop is installed and running
3. Try the minimal installation approach
4. You can always use Neo4j Browser directly without Python queries
