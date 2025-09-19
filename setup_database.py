#!/usr/bin/env python3
"""
Complete database setup script for Varnika platform
This script will create all required tables and populate them with sample data
"""

import mysql.connector
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Set up the complete Varnika database"""
    try:
        # Connect to MySQL server (without specifying database first)
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
        )
        cursor = connection.cursor()
        
        print("✓ Connected to MySQL server successfully.")
        
        # Read and execute the complete schema
        schema_file = os.path.join(os.path.dirname(__file__), 'complete_schema.sql')
        
        if not os.path.exists(schema_file):
            print(f"✗ Error: complete_schema.sql file not found at {schema_file}")
            return False
        
        with open(schema_file, 'r') as file:
            schema_sql = file.read()
        
        print("✓ Reading complete_schema.sql file...")
        
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
        print(f"✓ Database setup completed successfully! Executed {executed_count} statements.")
        
        # Verify the setup
        cursor.execute("USE artisan_platform")
        cursor.execute("SELECT COUNT(*) FROM categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM artisans")
        artisans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM generatedcontent")
        content_count = cursor.fetchone()[0]
        
        print(f"\n✓ Database verification:")
        print(f"  - Categories: {categories_count}")
        print(f"  - Artisans: {artisans_count}")
        print(f"  - Products: {products_count}")
        print(f"  - Generated Content: {content_count}")
        
        print(f"\n🎉 Varnika database is ready!")
        print(f"   You can now start the backend server with: python backend/app.py")
        
        return True
        
    except mysql.connector.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except FileNotFoundError:
        print("✗ Error: complete_schema.sql file not found. Please ensure it's in the same directory.")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("✓ Database connection closed.")

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['MYSQL_HOST', 'MYSQL_USER', 'MYSQL_PASSWORD', 'MYSQL_DATABASE']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠ Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease create a .env file in the backend directory with:")
        print("MYSQL_HOST=localhost")
        print("MYSQL_USER=root")
        print("MYSQL_PASSWORD=your_password")
        print("MYSQL_DATABASE=artisan_platform")
        print("\nUsing default values for now...")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Varnika Database Setup")
    print("=" * 50)
    
    # Check environment
    check_environment()
    
    # Setup database
    success = setup_database()
    
    if success:
        print("\n✅ Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)
