#!/usr/bin/env python3
"""
Database migration script to set up the complete Varnika database schema
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_database():
    """Set up the complete database schema"""
    try:
        # Connect to database
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE")
        )
        cursor = connection.cursor()
        
        print("Connected to database successfully.")
        print("Setting up complete Varnika database schema...")
        
        # Read and execute the complete schema
        with open('complete_schema.sql', 'r') as file:
            schema_sql = file.read()
        
        # Split the SQL into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        executed_count = 0
        for statement in statements:
            try:
                if statement:
                    cursor.execute(statement)
                    executed_count += 1
                    print(f"✓ Executed statement {executed_count}")
            except mysql.connector.Error as e:
                if "already exists" in str(e).lower() or "duplicate" in str(e).lower():
                    print(f"⚠ Skipped (already exists): {statement[:50]}...")
                else:
                    print(f"✗ Error executing statement: {e}")
                    print(f"Statement: {statement[:100]}...")
        
        # Commit changes
        connection.commit()
        print(f"✓ Database migration completed successfully! Executed {executed_count} statements.")
        
        # Verify the setup
        cursor.execute("SELECT COUNT(*) FROM categories")
        categories_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM artisans")
        artisans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        
        print(f"✓ Database verification:")
        print(f"  - Categories: {categories_count}")
        print(f"  - Artisans: {artisans_count}")
        print(f"  - Products: {products_count}")
        
    except mysql.connector.Error as e:
        print(f"✗ Database error: {e}")
    except FileNotFoundError:
        print("✗ Error: complete_schema.sql file not found. Please ensure it's in the same directory.")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    migrate_database()
