"""
Interactive dependency installer with error handling.
Installs packages one by one to identify problematic packages.
"""

import subprocess
import sys

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def install_package(package):
    """Install a single package"""
    print(f"\nInstalling {package}...", end=" ")
    success, stdout, stderr = run_command(f"pip install {package}")
    
    if success:
        print("✓ Success")
        return True
    else:
        print("✗ Failed")
        print(f"Error: {stderr[:200]}")
        return False

def main():
    print("="*60)
    print("Oracle Metadata Knowledge Graph - Dependency Installer")
    print("="*60)
    
    # Check Python version
    print(f"\nPython version: {sys.version}")
    if sys.version_info < (3, 9):
        print("✗ Python 3.9 or higher is required")
        return
    print("✓ Python version OK")
    
    # Upgrade pip first
    print("\nUpgrading pip...")
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # Core packages (required)
    core_packages = [
        "python-dotenv>=1.0.0",
        "neo4j>=5.14.0",
        "openai>=1.12.0",
        "pandas>=2.0.0",
    ]
    
    # LangChain packages
    langchain_packages = [
        "langchain>=0.1.0",
        "langchain-openai>=0.0.5",
        "langchain-community>=0.0.20",
    ]
    
    # Optional packages
    optional_packages = [
        ("jupyter", "For Jupyter notebooks"),
        ("ipykernel", "For Jupyter kernel"),
        ("matplotlib", "For visualizations"),
        ("networkx", "For network graphs"),
    ]
    
    print("\n" + "="*60)
    print("Installing CORE packages (required)")
    print("="*60)
    
    failed_core = []
    for package in core_packages:
        if not install_package(package):
            failed_core.append(package)
    
    print("\n" + "="*60)
    print("Installing LANGCHAIN packages (required for AI queries)")
    print("="*60)
    
    failed_langchain = []
    for package in langchain_packages:
        if not install_package(package):
            failed_langchain.append(package)
    
    print("\n" + "="*60)
    print("Installing OPTIONAL packages")
    print("="*60)
    
    failed_optional = []
    for package, description in optional_packages:
        print(f"\n{description}")
        response = input(f"Install {package}? (y/n, default=y): ").strip().lower()
        
        if response in ['', 'y', 'yes']:
            if not install_package(package):
                failed_optional.append(package)
        else:
            print(f"Skipped {package}")
    
    # Oracle connector (often problematic)
    print("\n" + "="*60)
    print("Oracle Database Connector (OPTIONAL)")
    print("="*60)
    print("\nNote: This is only needed if extracting from a real Oracle database.")
    print("You can use sample_metadata.py without this package.")
    
    response = input("\nInstall oracledb? (y/n, default=n): ").strip().lower()
    
    failed_oracle = False
    if response in ['y', 'yes']:
        if not install_package("oracledb>=2.0.0"):
            failed_oracle = True
            print("\n⚠ Oracle connector failed to install")
            print("You can still use the project with sample_metadata.py")
    
    # Summary
    print("\n" + "="*60)
    print("Installation Summary")
    print("="*60)
    
    if not failed_core and not failed_langchain:
        print("\n✓ All required packages installed successfully!")
        print("\nYou can now:")
        print("  1. Configure .env file: copy .env.example .env")
        print("  2. Start Neo4j: docker-compose up -d")
        print("  3. Generate data: python src/sample_metadata.py")
        print("  4. Build graph: python src/build_graph.py")
        print("  5. Query graph: python src/query_graph.py")
    else:
        print("\n✗ Some required packages failed to install:")
        if failed_core:
            print("\nCore packages:")
            for pkg in failed_core:
                print(f"  - {pkg}")
        if failed_langchain:
            print("\nLangChain packages:")
            for pkg in failed_langchain:
                print(f"  - {pkg}")
        
        print("\nTroubleshooting:")
        print("  1. Make sure you're in a virtual environment")
        print("  2. Try: pip install --upgrade pip setuptools wheel")
        print("  3. Install Visual C++ Build Tools (for Windows)")
        print("     Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("  4. Try installing packages individually")
        print("  5. Check TROUBLESHOOTING.md for more help")
    
    if failed_optional:
        print("\n⚠ Optional packages that failed:")
        for pkg in failed_optional:
            print(f"  - {pkg}")
        print("These are not required for core functionality")
    
    if failed_oracle:
        print("\n⚠ Oracle connector not installed")
        print("Use sample_metadata.py instead of extract_metadata.py")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()
