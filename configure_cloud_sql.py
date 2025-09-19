#!/usr/bin/env python3
"""
Quick Cloud SQL Configuration Script
This script helps you configure the .env file for Cloud SQL
"""

import os
import shutil
from pathlib import Path

def configure_cloud_sql():
    """Configure Cloud SQL environment"""
    print("🌩️  Varnika Cloud SQL Configuration")
    print("=" * 50)
    
    # Get Cloud SQL details
    host = "104.197.43.172"  # Your Cloud SQL IP
    user = "root"
    database = "artisan_platform"
    port = "3306"
    
    print(f"Cloud SQL Host: {host}")
    print(f"Database: {database}")
    print(f"Port: {port}")
    print()
    
    # Get password from user
    password = input("Enter your Cloud SQL root password: ").strip()
    
    if not password:
        print("❌ Password is required")
        return False
    
    # Create .env content
    env_content = f"""# Varnika Platform Environment Configuration

# ===========================================
# DATABASE CONFIGURATION
# ===========================================

# Google Cloud SQL Configuration
CLOUD_SQL_HOST={host}
CLOUD_SQL_USER={user}
CLOUD_SQL_PASSWORD={password}
CLOUD_SQL_DATABASE={database}
CLOUD_SQL_PORT={port}

# Local MySQL Fallback (for development)
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
    
    # Create backend directory if it doesn't exist
    backend_dir = Path("backend")
    backend_dir.mkdir(exist_ok=True)
    
    # Write .env file
    env_file = backend_dir / ".env"
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ .env file created at: {env_file}")
        print("✅ Cloud SQL configuration completed!")
        
        # Test the connection
        print("\n🧪 Testing Cloud SQL connection...")
        test_connection(host, user, password, database, port)
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def test_connection(host, user, password, database, port):
    """Test the Cloud SQL connection"""
    try:
        import mysql.connector
        
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=int(port),
            autocommit=True,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True,
            connect_timeout=60,
            sql_mode='TRADITIONAL'
        )
        
        print("✅ Cloud SQL connection successful!")
        
        # Test basic queries
        cursor = connection.cursor()
        
        # Check MySQL version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL version: {version[0]}")
        
        # Check tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        print(f"✅ Tables found: {table_names}")
        
        # Check if required tables exist
        required_tables = ['categories', 'artisans', 'products', 'generatedcontent']
        missing_tables = [table for table in required_tables if table not in table_names]
        
        if missing_tables:
            print(f"⚠️  Missing tables: {missing_tables}")
            print("Please ensure all required tables are created in your Cloud SQL instance")
        else:
            print("✅ All required tables are present!")
        
        # Test data queries
        if 'categories' in table_names:
            cursor.execute("SELECT COUNT(*) FROM categories")
            categories_count = cursor.fetchone()[0]
            print(f"✅ Categories count: {categories_count}")
        
        if 'products' in table_names:
            cursor.execute("SELECT COUNT(*) FROM products")
            products_count = cursor.fetchone()[0]
            print(f"✅ Products count: {products_count}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Cloud SQL is ready for the Varnika platform!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Cloud SQL connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if the Cloud SQL instance is running")
        print("2. Verify the password is correct")
        print("3. Check if your IP is authorized")
        print("4. Ensure the database exists")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    configure_cloud_sql()
