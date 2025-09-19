#!/usr/bin/env python3
"""
Complete Varnika Platform Setup Script
Handles both Google Cloud SQL and local MySQL setup
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🚀 {title}")
    print("=" * 60)

def check_requirements():
    """Check if required tools are installed"""
    print_header("Checking Requirements")
    
    requirements = {
        "Python": "python --version",
        "Node.js": "node --version",
        "npm": "npm --version",
        "MySQL": "mysql --version"
    }
    
    missing = []
    for tool, command in requirements.items():
        try:
            result = subprocess.run(command.split(), capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ {tool}: {version}")
            else:
                print(f"❌ {tool}: Not found")
                missing.append(tool)
        except FileNotFoundError:
            print(f"❌ {tool}: Not found")
            missing.append(tool)
    
    if missing:
        print(f"\n⚠️  Missing requirements: {', '.join(missing)}")
        print("Please install the missing tools and try again.")
        return False
    
    return True

def setup_environment():
    """Setup environment configuration"""
    print_header("Environment Configuration")
    
    env_file = Path("backend/.env")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    print("📝 Creating .env file...")
    
    env_content = """# Varnika Platform Environment Configuration

# ===========================================
# DATABASE CONFIGURATION
# ===========================================

# Option 1: Google Cloud SQL (Recommended for production)
# Uncomment and configure these for Cloud SQL
# CLOUD_SQL_HOST=your_instance_ip_address
# CLOUD_SQL_USER=root
# CLOUD_SQL_PASSWORD=your_root_password
# CLOUD_SQL_DATABASE=artisan_platform
# CLOUD_SQL_PORT=3306

# Option 2: Local MySQL (For development)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_local_mysql_password
MYSQL_DATABASE=artisan_platform

# ===========================================
# GOOGLE CLOUD CONFIGURATION
# ===========================================

# Google Cloud Project Configuration
GCLOUD_PROJECT_ID=your_project_id
REGION=us-central1
GCS_BUCKET_NAME=your_bucket_name

# ===========================================
# APPLICATION CONFIGURATION
# ===========================================

# Backend Configuration
FLASK_ENV=development
FLASK_DEBUG=True
BACKEND_PORT=5001

# Frontend Configuration
FRONTEND_PORT=5173
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Please update the .env file with your actual credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def install_backend_dependencies():
    """Install Python dependencies"""
    print_header("Installing Backend Dependencies")
    
    try:
        os.chdir("backend")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Backend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install backend dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing backend dependencies: {e}")
        return False
    finally:
        os.chdir("..")

def install_frontend_dependencies():
    """Install Node.js dependencies"""
    print_header("Installing Frontend Dependencies")
    
    try:
        os.chdir("frontend")
        result = subprocess.run(["npm", "install"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Frontend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install frontend dependencies: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error installing frontend dependencies: {e}")
        return False
    finally:
        os.chdir("..")

def setup_database():
    """Setup database (Cloud SQL or local)"""
    print_header("Database Setup")
    
    # Check if Cloud SQL is configured
    from dotenv import load_dotenv
    load_dotenv("backend/.env")
    
    cloud_sql_host = os.getenv("CLOUD_SQL_HOST")
    cloud_sql_user = os.getenv("CLOUD_SQL_USER")
    cloud_sql_password = os.getenv("CLOUD_SQL_PASSWORD")
    
    if cloud_sql_host and cloud_sql_user and cloud_sql_password and cloud_sql_host != "your_instance_ip_address":
        print("🌩️  Cloud SQL configuration detected")
        print("Testing Cloud SQL connection...")
        
        try:
            result = subprocess.run([sys.executable, "test_cloud_sql.py"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Cloud SQL connection successful")
                return True
            else:
                print("❌ Cloud SQL connection failed")
                print("Falling back to local MySQL setup...")
        except Exception as e:
            print(f"❌ Error testing Cloud SQL: {e}")
            print("Falling back to local MySQL setup...")
    
    # Fallback to local MySQL
    print("🏠 Setting up local MySQL database...")
    
    try:
        result = subprocess.run([sys.executable, "setup_database.py"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Local database setup successful")
            return True
        else:
            print("❌ Local database setup failed")
            print("Please check your MySQL installation and configuration")
            return False
    except Exception as e:
        print(f"❌ Error setting up local database: {e}")
        return False

def test_application():
    """Test the application setup"""
    print_header("Testing Application")
    
    print("🧪 Testing backend connection...")
    try:
        result = subprocess.run([sys.executable, "test_integration.py"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("✅ Backend API test successful")
        else:
            print("⚠️  Backend API test failed (this is normal if backend is not running)")
    except subprocess.TimeoutExpired:
        print("⚠️  Backend API test timed out")
    except Exception as e:
        print(f"⚠️  Backend API test error: {e}")
    
    print("\n✅ Application setup completed!")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print_header("Next Steps")
    
    print("🎉 Varnika platform setup completed!")
    print("\n📋 To start the application:")
    print("\n1. Backend (Terminal 1):")
    print("   cd backend")
    print("   python app.py")
    print("\n2. Frontend (Terminal 2):")
    print("   cd frontend")
    print("   npm run dev")
    print("\n3. Open your browser:")
    print("   http://localhost:5173")
    
    print("\n🔧 Configuration:")
    print("• Update backend/.env with your database credentials")
    print("• For Cloud SQL: Configure CLOUD_SQL_* variables")
    print("• For local MySQL: Configure MYSQL_* variables")
    
    print("\n📚 Documentation:")
    print("• Cloud SQL Setup: CLOUD_SQL_SETUP.md")
    print("• Database Setup: DATABASE_SETUP.md")
    print("• Main README: README.md")
    
    print("\n🧪 Testing:")
    print("• Test Cloud SQL: python test_cloud_sql.py")
    print("• Test API: python test_integration.py")
    print("• Test Database: python setup_database.py")

def main():
    """Main setup function"""
    print_header("Varnika Platform Setup")
    print("This script will set up the complete Varnika handicraft platform")
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the Varnika root directory")
        print("   The directory should contain 'backend' and 'frontend' folders")
        sys.exit(1)
    
    steps = [
        ("Checking Requirements", check_requirements),
        ("Environment Configuration", setup_environment),
        ("Backend Dependencies", install_backend_dependencies),
        ("Frontend Dependencies", install_frontend_dependencies),
        ("Database Setup", setup_database),
        ("Application Testing", test_application)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at step: {step_name}")
            print("Please fix the issue and run the script again")
            sys.exit(1)
    
    print_next_steps()

if __name__ == "__main__":
    main()


