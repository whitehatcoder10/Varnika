#!/usr/bin/env python3
"""
Start Varnika Platform Script
This script starts both backend and frontend applications
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_cloud_sql_connection():
    """Check if Cloud SQL connection is working"""
    print("🔍 Checking Cloud SQL connection...")
    
    try:
        result = subprocess.run([sys.executable, "test_connection.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and "✅ Connected to Cloud SQL successfully!" in result.stdout:
            print("✅ Cloud SQL connection verified!")
            return True
        else:
            print("❌ Cloud SQL connection failed")
            print("Please update backend/.env with your Cloud SQL password")
            return False
    except Exception as e:
        print(f"❌ Error checking connection: {e}")
        return False

def start_backend():
    """Start the backend application"""
    print("\n🚀 Starting Backend...")
    print("=" * 50)
    
    try:
        os.chdir("backend")
        print("Starting Flask backend on http://localhost:5001")
        print("Press Ctrl+C to stop the backend")
        
        # Start the backend
        subprocess.run([sys.executable, "app.py"])
        
    except KeyboardInterrupt:
        print("\n⏹️  Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
    finally:
        os.chdir("..")

def start_frontend():
    """Start the frontend application"""
    print("\n🎨 Starting Frontend...")
    print("=" * 50)
    
    try:
        os.chdir("frontend")
        
        # Check if node_modules exists
        if not Path("node_modules").exists():
            print("📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        print("Starting React frontend on http://localhost:5173")
        print("Press Ctrl+C to stop the frontend")
        
        # Start the frontend
        subprocess.run(["npm", "run", "dev"])
        
    except KeyboardInterrupt:
        print("\n⏹️  Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")
    finally:
        os.chdir("..")

def main():
    """Main function"""
    print("🌩️  Varnika Platform Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("backend").exists() or not Path("frontend").exists():
        print("❌ Please run this script from the Varnika root directory")
        print("   The directory should contain 'backend' and 'frontend' folders")
        sys.exit(1)
    
    # Check Cloud SQL connection
    if not check_cloud_sql_connection():
        print("\n❌ Cannot start without a working Cloud SQL connection")
        print("Please:")
        print("1. Update backend/.env with your Cloud SQL password")
        print("2. Run: python test_connection.py")
        print("3. Try again")
        sys.exit(1)
    
    print("\n🎉 Cloud SQL connection verified!")
    print("\nChoose an option:")
    print("1. Start Backend only")
    print("2. Start Frontend only")
    print("3. Start Both (Backend + Frontend)")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        start_backend()
    elif choice == "2":
        start_frontend()
    elif choice == "3":
        print("\n🚀 Starting both applications...")
        print("Backend will start first, then frontend")
        print("You'll need to open two terminals for this")
        print("\nTerminal 1 (Backend):")
        print("cd backend && python app.py")
        print("\nTerminal 2 (Frontend):")
        print("cd frontend && npm run dev")
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
