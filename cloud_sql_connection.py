#!/usr/bin/env python3
"""
Google Cloud SQL connection configuration for Varnika platform
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_cloud_sql_connection():
    """Get connection to Google Cloud SQL instance"""
    try:
        # Cloud SQL connection parameters
        config = {
            'host': os.getenv('CLOUD_SQL_HOST', 'YOUR_INSTANCE_IP'),
            'user': os.getenv('CLOUD_SQL_USER', 'root'),
            'password': os.getenv('CLOUD_SQL_PASSWORD', 'YOUR_PASSWORD'),
            'database': os.getenv('CLOUD_SQL_DATABASE', 'artisan_platform'),
            'port': int(os.getenv('CLOUD_SQL_PORT', '3306')),
            'autocommit': True,
            'charset': 'utf8mb4',
            'collation': 'utf8mb4_unicode_ci',
            'use_unicode': True,
            'connect_timeout': 60,
            'sql_mode': 'TRADITIONAL'
        }
        
        print(f"Connecting to Cloud SQL instance: {config['host']}")
        print(f"Database: {config['database']}")
        print(f"User: {config['user']}")
        
        connection = mysql.connector.connect(**config)
        print("✅ Connected to Cloud SQL successfully!")
        return connection
        
    except mysql.connector.Error as e:
        print(f"❌ Cloud SQL connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if the Cloud SQL instance is running")
        print("2. Verify the IP address and port")
        print("3. Ensure the database exists")
        print("4. Check firewall rules allow your IP")
        print("5. Verify username and password")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def test_connection():
    """Test the Cloud SQL connection"""
    connection = get_cloud_sql_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL version: {version[0]}")
            
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            print(f"✅ Available databases: {[db[0] for db in databases]}")
            
            cursor.close()
            connection.close()
            print("✅ Connection test successful!")
            return True
        except Exception as e:
            print(f"❌ Connection test failed: {e}")
            return False
    return False

def setup_cloud_sql_database():
    """Set up the database schema on Cloud SQL"""
    connection = get_cloud_sql_connection()
    if not connection:
        return False
    
    try:
        cursor = connection.cursor()
        
        # Read and execute the complete schema
        schema_file = os.path.join(os.path.dirname(__file__), 'complete_schema.sql')
        
        if not os.path.exists(schema_file):
            print(f"❌ Error: complete_schema.sql file not found at {schema_file}")
            return False
        
        with open(schema_file, 'r') as file:
            schema_sql = file.read()
        
        print("📖 Reading complete_schema.sql file...")
        
        # Split the SQL into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        executed_count = 0
        for statement in statements:
            try:
                if statement:
                    cursor.execute(statement)
                    executed_count += 1
                    if executed_count % 10 == 0:
                        print(f"  Executed {executed_count} statements...")
            except mysql.connector.Error as e:
                if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                    print(f"  ⚠ Skipped (already exists): {statement[:50]}...")
                else:
                    print(f"  ✗ Error executing statement: {e}")
                    print(f"  Statement: {statement[:100]}...")
        
        # Commit changes
        connection.commit()
        print(f"✅ Database setup completed successfully! Executed {executed_count} statements.")
        
        # Verify the setup
        cursor.execute("SELECT COUNT(*) FROM categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM artisans")
        artisans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM generatedcontent")
        content_count = cursor.fetchone()[0]
        
        print(f"\n✅ Database verification:")
        print(f"  - Categories: {categories_count}")
        print(f"  - Artisans: {artisans_count}")
        print(f"  - Products: {products_count}")
        print(f"  - Generated Content: {content_count}")
        
        cursor.close()
        connection.close()
        print("✅ Cloud SQL database setup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    print("🌩️  Varnika Cloud SQL Setup")
    print("=" * 50)
    
    # Test connection first
    if test_connection():
        print("\n🚀 Setting up database schema...")
        setup_cloud_sql_database()
    else:
        print("\n❌ Cannot proceed without a valid connection.")
        print("\nPlease check your .env file and ensure it contains:")
        print("CLOUD_SQL_HOST=your_instance_ip")
        print("CLOUD_SQL_USER=root")
        print("CLOUD_SQL_PASSWORD=your_password")
        print("CLOUD_SQL_DATABASE=artisan_platform")
        print("CLOUD_SQL_PORT=3306")


