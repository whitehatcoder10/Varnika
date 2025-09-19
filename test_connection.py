#!/usr/bin/env python3
"""
Test Cloud SQL connection without interactive input
"""

import mysql.connector
import os
from dotenv import load_dotenv

def test_cloud_sql():
    """Test Cloud SQL connection"""
    print("🌩️  Testing Cloud SQL Connection")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv("backend/.env")
    
    host = os.getenv('CLOUD_SQL_HOST', '104.197.43.172')
    user = os.getenv('CLOUD_SQL_USER', 'root')
    password = os.getenv('CLOUD_SQL_PASSWORD', 'your_password_here')
    database = os.getenv('CLOUD_SQL_DATABASE', 'artisan_platform')
    port = int(os.getenv('CLOUD_SQL_PORT', '3306'))
    
    print(f"Host: {host}")
    print(f"User: {user}")
    print(f"Database: {database}")
    print(f"Port: {port}")
    print()
    
    if password == 'your_password_here':
        print("❌ Please update the .env file with your actual Cloud SQL password")
        print("Edit backend/.env and change CLOUD_SQL_PASSWORD=your_password_here")
        print("to CLOUD_SQL_PASSWORD=your_actual_password")
        return False
    
    try:
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
        
        if 'artisans' in table_names:
            cursor.execute("SELECT COUNT(*) FROM artisans")
            artisans_count = cursor.fetchone()[0]
            print(f"✅ Artisans count: {artisans_count}")
        
        if 'products' in table_names:
            cursor.execute("SELECT COUNT(*) FROM products")
            products_count = cursor.fetchone()[0]
            print(f"✅ Products count: {products_count}")
        
        if 'generatedcontent' in table_names:
            cursor.execute("SELECT COUNT(*) FROM generatedcontent")
            content_count = cursor.fetchone()[0]
            print(f"✅ Generated content count: {content_count}")
        
        # Test a sample query
        try:
            cursor.execute("SELECT name, price FROM products LIMIT 3")
            sample_products = cursor.fetchall()
            print(f"✅ Sample products: {sample_products}")
        except Exception as e:
            print(f"⚠️  Sample query failed: {e}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Cloud SQL is ready for the Varnika platform!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Cloud SQL connection failed: {e}")
        print("\nTroubleshooting steps:")
        print("1. Check if the Cloud SQL instance is running")
        print("2. Verify the password is correct in backend/.env")
        print("3. Check if your IP is authorized")
        print("4. Ensure the database exists")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    test_cloud_sql()
