#!/usr/bin/env python3
"""
Setup script for Facebook Pages dbt Transformation Models
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False

def check_database_file():
    """Check if the database file exists"""
    db_file = "facebook_pages_pipeline.duckdb"
    profiles_file = Path(".dbt/profiles.yml")
    
    if profiles_file.exists():
        # Try to read the database path from profiles.yml
        try:
            with open(profiles_file, 'r') as f:
                content = f.read()
                if 'path:' in content:
                    # Extract the path (simple parsing)
                    for line in content.split('\n'):
                        if 'path:' in line and '.duckdb' in line:
                            db_path = line.split('path:')[1].strip().strip("'\"")
                            db_file = db_path
                            break
        except Exception:
            pass
    
    if os.path.exists(db_file):
        print(f"✅ Database file found: {db_file}")
        return True
    else:
        print(f"⚠️  Database file not found: {db_file}")
        print("   Make sure to run the DLT extraction pipeline first!")
        print("   See: https://github.com/your-org/dlt-facebook-pages")
        return False

def check_dbt_connection():
    """Test dbt database connection"""
    print("\n🔄 Testing dbt database connection...")
    try:
        result = subprocess.run(["dbt", "debug"], capture_output=True, text=True)
        if "All checks passed!" in result.stdout:
            print("✅ dbt connection test passed")
            return True
        else:
            print("❌ dbt connection test failed:")
            print(result.stdout)
            print(result.stderr)
            return False
    except FileNotFoundError:
        print("❌ dbt command not found. Please install dbt-core and dbt-duckdb")
        return False
    except Exception as e:
        print(f"❌ Error testing dbt connection: {e}")
        return False

def main():
    print_header("Facebook Pages dbt Setup")
    
    print("🚀 Setting up Facebook Pages dbt transformation models...")
    print("   This will install dependencies and validate your setup.")
    
    success_count = 0
    total_steps = 6
    
    # Step 1: Check Python version
    print_header("Step 1: Environment Check")
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    if python_version >= (3, 8):
        print("✅ Python version is compatible")
        success_count += 1
    else:
        print("❌ Python 3.8+ required")
    
    # Step 2: Install Python dependencies
    print_header("Step 2: Install Dependencies")
    if run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        success_count += 1
    
    # Step 3: Install dbt dependencies
    print_header("Step 3: Install dbt Dependencies")
    if run_command("dbt deps", "Installing dbt package dependencies"):
        success_count += 1
    
    # Step 4: Check for database file
    print_header("Step 4: Database Check")
    if check_database_file():
        success_count += 1
    
    # Step 5: Test dbt connection
    print_header("Step 5: Database Connection Test")
    if check_dbt_connection():
        success_count += 1
    
    # Step 6: Compile models
    print_header("Step 6: Compile Models")
    if run_command("dbt compile", "Compiling dbt models"):
        success_count += 1
    
    # Final status
    print_header("Setup Complete")
    print(f"✅ {success_count}/{total_steps} steps completed successfully")
    
    if success_count == total_steps:
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Run 'make pipeline' to execute all models")
        print("   2. Run 'make test' to validate data quality")
        print("   3. Run 'make docs' to view documentation")
        print("\n💡 Useful commands:")
        print("   • make run          - Run all models")
        print("   • make test         - Run data quality tests")
        print("   • make docs         - Generate documentation")
        print("   • make help         - See all available commands")
    else:
        print(f"\n⚠️  Setup completed with {total_steps - success_count} warnings/errors")
        print("   Please review the output above and resolve any issues")
        
        if success_count < 4:
            print("\n🚨 Critical issues detected:")
            print("   • Make sure you have Python 3.8+ installed")
            print("   • Install required dependencies")
            print("   • Run the DLT extraction pipeline first")
            print("   • Check your database connection settings")
    
    print(f"\n📚 Documentation: README.md")
    print(f"🔗 DLT Pipeline: https://github.com/your-org/dlt-facebook-pages")

if __name__ == "__main__":
    main()