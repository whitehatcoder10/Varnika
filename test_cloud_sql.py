#!/usr/bin/env python3
"""
Test script for Google Cloud SQL connection
Run this to verify your Cloud SQL setup
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_cloud_sql_connection():
    """Test connection to Google Cloud SQL"""
    print("🌩️  Testing Google Cloud SQL Connection")
    print("=" * 50)
    
    # Get connection parameters
    host = os.getenv('CLOUD_SQL_HOST', 'YOUR_INSTANCE_IP')
    user = os.getenv('CLOUD_SQL_USER', 'root')
    password = os.getenv('CLOUD_SQL_PASSWORD', 'YOUR_PASSWORD')
    database = os.getenv('CLOUD_SQL_DATABASE', 'artisan_platform')
    port = int(os.getenv('CLOUD_SQL_PORT', '3306'))
    
    print(f"Host: {host}")
    print(f"User: {user}")
    print(f"Database: {database}")
    print(f"Port: {port}")
    print()
    
    if host == 'YOUR_INSTANCE_IP' or password == 'YOUR_PASSWORD':
        print("❌ Please configure your .env file with actual Cloud SQL credentials")
        print("\nRequired .env variables:")
        print("CLOUD_SQL_HOST=your_instance_ip")
        print("CLOUD_SQL_USER=root")
        print("CLOUD_SQL_PASSWORD=your_password")
        print("CLOUD_SQL_DATABASE=artisan_platform")
        print("CLOUD_SQL_PORT=3306")
        return False
    
    try:
        # Attempt connection
        print("🔄 Connecting to Cloud SQL...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            autocommit=True,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci',
            use_unicode=True,
            connect_timeout=60,
            sql_mode='TRADITIONAL'
        )
        
        print("✅ Connected to Cloud SQL successfully!")
        
        # Test basic queries
        cursor = connection.cursor()
        
        # Check MySQL version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ MySQL version: {version[0]}")
        
        # Check databases
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        print(f"✅ Available databases: {[db[0] for db in databases]}")
        
        # Check current database tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"✅ Tables in {database}: {[table[0] for table in tables]}")
        
        # Test data queries if tables exist
        if 'categories' in [table[0] for table in tables]:
            cursor.execute("SELECT COUNT(*) FROM categories")
            categories_count = cursor.fetchone()[0]
            print(f"✅ Categories count: {categories_count}")
        
        if 'products' in [table[0] for table in tables]:
            cursor.execute("SELECT COUNT(*) FROM products")
            products_count = cursor.fetchone()[0]
            print(f"✅ Products count: {products_count}")
        
        # Test a sample query
        try:
            cursor.execute("SELECT name, price FROM products LIMIT 3")
            sample_products = cursor.fetchall()
            print(f"✅ Sample products: {sample_products}")
        except Exception as e:
            print(f"⚠️  Sample query failed: {e}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Cloud SQL connection test successful!")
        print("✅ Your Varnika platform is ready to use with Cloud SQL!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Cloud SQL connection failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Check if the Cloud SQL instance is running")
        print("2. Verify the IP address and port")
        print("3. Ensure the database exists")
        print("4. Check firewall rules allow your IP")
        print("5. Verify username and password")
        print("6. Run: gcloud sql instances describe varnika-instance-final")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_local_fallback():
    """Test local MySQL fallback"""
    print("\n🏠 Testing Local MySQL Fallback")
    print("=" * 50)
    
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "artisan_platform")
        )
        
        print("✅ Local MySQL connection successful!")
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Local MySQL connection failed: {e}")
        return False

if __name__ == "__main__":
    # Test Cloud SQL connection
    cloud_sql_success = test_cloud_sql_connection()
    
    # Test local fallback
    local_success = test_local_fallback()
    
    print("\n" + "=" * 50)
    print("📊 Connection Test Results:")
    print(f"Cloud SQL: {'✅ Success' if cloud_sql_success else '❌ Failed'}")
    print(f"Local MySQL: {'✅ Success' if local_success else '❌ Failed'}")
    
    if cloud_sql_success:
        print("\n🚀 You can now start the Varnika platform!")
        print("Backend: cd backend && python app.py")
        print("Frontend: cd frontend && npm run dev")
    elif local_success:
        print("\n⚠️  Using local MySQL as fallback")
        print("Consider setting up Cloud SQL for production")
    else:
        print("\n❌ No database connection available")
        print("Please check your configuration and try again")


