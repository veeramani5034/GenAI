"""
Test which packages are installed correctly.
Run this after pip install to verify your setup.
"""

import sys

print("="*60)
print("Installation Test")
print("="*60)

print(f"\nPython Version: {sys.version}")
print(f"Python Path: {sys.executable}")

if sys.version_info < (3, 9):
    print("✗ Python 3.9+ required")
    sys.exit(1)
else:
    print("✓ Python version OK")

print("\n" + "="*60)
print("Testing Package Imports")
print("="*60)

required_packages = []
optional_packages = []

# Test required packages
print("\nRequired Packages:")

try:
    import neo4j
    print(f"  ✓ neo4j (version: {neo4j.__version__})")
    required_packages.append(True)
except ImportError as e:
    print(f"  ✗ neo4j - REQUIRED - {e}")
    required_packages.append(False)

try:
    import openai
    print(f"  ✓ openai (version: {openai.__version__})")
    required_packages.append(True)
except ImportError as e:
    print(f"  ✗ openai - REQUIRED - {e}")
    required_packages.append(False)

try:
    import langchain
    print(f"  ✓ langchain (version: {langchain.__version__})")
    required_packages.append(True)
except ImportError as e:
    print(f"  ✗ langchain - REQUIRED - {e}")
    required_packages.append(False)

try:
    from langchain_openai import ChatOpenAI
    print(f"  ✓ langchain-openai")
    required_packages.append(True)
except ImportError as e:
    print(f"  ✗ langchain-openai - REQUIRED - {e}")
    required_packages.append(False)

try:
    from langchain_community.graphs import Neo4jGraph
    print(f"  ✓ langchain-community")
    required_packages.append(True)
except ImportError as e:
    print(f"  ✗ langchain-community - REQUIRED - {e}")
    required_packages.append(False)

try:
    from dotenv import load_dotenv
    print(f"  ✓ python-dotenv")
    required_packages.append(True)
except ImportError as e:
    print(f"  ✗ python-dotenv - REQUIRED - {e}")
    required_packages.append(False)

# Test optional packages
print("\nOptional Packages:")

try:
    import pandas
    print(f"  ✓ pandas (version: {pandas.__version__})")
    optional_packages.append(True)
except ImportError:
    print(f"  ⚠ pandas - Optional (recommended)")
    optional_packages.append(False)

try:
    import jupyter
    print(f"  ✓ jupyter")
    optional_packages.append(True)
except ImportError:
    print(f"  ⚠ jupyter - Optional (for notebooks)")
    optional_packages.append(False)

try:
    import oracledb
    print(f"  ✓ oracledb (version: {oracledb.__version__})")
    optional_packages.append(True)
except ImportError:
    print(f"  ⚠ oracledb - Optional (use sample_metadata.py instead)")
    optional_packages.append(False)

# Summary
print("\n" + "="*60)
print("Summary")
print("="*60)

all_required = all(required_packages)
some_optional = any(optional_packages)

if all_required:
    print("\n✓ All required packages installed successfully!")
    print("\nYou can now:")
    print("  1. Configure .env: copy .env.example .env")
    print("  2. Edit .env and add your OpenAI API key")
    print("  3. Start Neo4j: docker-compose up -d")
    print("  4. Generate data: python src/sample_metadata.py")
    print("  5. Build graph: python src/build_graph.py")
    print("  6. Query graph: python src/query_graph.py")
else:
    print("\n✗ Some required packages are missing!")
    print("\nTo fix:")
    print("  1. Make sure virtual environment is activated")
    print("  2. Try: pip install -r requirements-minimal.txt")
    print("  3. Or: python install_dependencies.py")
    print("  4. See INSTALL_WINDOWS.md for detailed help")

if not some_optional:
    print("\n⚠ No optional packages installed")
    print("  This is OK for basic functionality")
    print("  Install later if needed: pip install pandas jupyter")

print("\n" + "="*60)

# Test environment file
import os
print("\nEnvironment Configuration:")
if os.path.exists('.env'):
    print("  ✓ .env file exists")
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.getenv('OPENAI_API_KEY'):
        key = os.getenv('OPENAI_API_KEY')
        if key.startswith('sk-'):
            print(f"  ✓ OpenAI API key configured (starts with: {key[:10]}...)")
        else:
            print("  ⚠ OpenAI API key format looks wrong (should start with 'sk-')")
    else:
        print("  ⚠ OpenAI API key not set in .env")
    
    if os.getenv('NEO4J_URI'):
        print(f"  ✓ Neo4j URI: {os.getenv('NEO4J_URI')}")
    else:
        print("  ⚠ Neo4j URI not set (will use default)")
else:
    print("  ⚠ .env file not found")
    print("    Run: copy .env.example .env")
    print("    Then edit .env and add your OpenAI API key")

# Test Docker
print("\nDocker Status:")
try:
    import subprocess
    result = subprocess.run(['docker', 'ps'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print("  ✓ Docker is running")
        if 'neo4j' in result.stdout.lower():
            print("  ✓ Neo4j container is running")
        else:
            print("  ⚠ Neo4j container not running")
            print("    Run: docker-compose up -d")
    else:
        print("  ✗ Docker command failed")
except FileNotFoundError:
    print("  ✗ Docker not found")
    print("    Install Docker Desktop: https://www.docker.com/products/docker-desktop/")
except subprocess.TimeoutExpired:
    print("  ⚠ Docker command timed out")
except Exception as e:
    print(f"  ⚠ Could not check Docker: {e}")

print("\n" + "="*60)
print("Test Complete")
print("="*60)
