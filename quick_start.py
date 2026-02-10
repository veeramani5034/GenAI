"""
Quick start script to set up and run the entire pipeline.
"""

import os
import subprocess
import sys
import time


def print_step(step_num, title):
    print("\n" + "="*60)
    print(f"STEP {step_num}: {title}")
    print("="*60 + "\n")


def check_docker():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_env_file():
    """Check if .env file exists"""
    return os.path.exists('.env')


def main():
    print("\n" + "="*60)
    print("Oracle Metadata Knowledge Graph - Quick Start")
    print("="*60)
    
    # Step 1: Check prerequisites
    print_step(1, "Checking Prerequisites")
    
    if not check_docker():
        print("✗ Docker is not running or not installed")
        print("  Please install Docker Desktop and start it")
        print("  Download: https://www.docker.com/products/docker-desktop/")
        return
    print("✓ Docker is running")
    
    if not check_env_file():
        print("✗ .env file not found")
        print("  Please copy .env.example to .env and add your OpenAI API key")
        print("  Run: copy .env.example .env")
        return
    print("✓ .env file exists")
    
    # Step 2: Start Neo4j
    print_step(2, "Starting Neo4j")
    print("Starting Neo4j container...")
    subprocess.run(['docker-compose', 'up', '-d'])
    print("\nWaiting 30 seconds for Neo4j to start...")
    time.sleep(30)
    print("✓ Neo4j should be running at http://localhost:7474")
    
    # Step 3: Generate sample metadata
    print_step(3, "Generating Sample Metadata")
    subprocess.run([sys.executable, 'src/sample_metadata.py'])
    
    # Step 4: Build knowledge graph
    print_step(4, "Building Knowledge Graph")
    subprocess.run([sys.executable, 'src/build_graph.py'])
    
    # Step 5: Done
    print_step(5, "Setup Complete!")
    print("✓ Neo4j is running at: http://localhost:7474")
    print("  Username: neo4j")
    print("  Password: password123")
    print("\n✓ Knowledge graph has been built")
    print("\nNext steps:")
    print("  1. Open Neo4j Browser: http://localhost:7474")
    print("  2. Run queries: python src/query_graph.py")
    print("  3. Try example: python src/query_graph.py --examples")
    print("\nTo stop Neo4j: docker-compose down")


if __name__ == "__main__":
    main()
