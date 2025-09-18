#!/usr/bin/env python3
"""
Database migration script to add missing fields to the products table
"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def migrate_database():
    """Add missing fields to the products table"""
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
        
        # Add missing columns to products table
        migrations = [
            "ALTER TABLE products ADD COLUMN IF NOT EXISTS category VARCHAR(100) DEFAULT 'General'",
            "ALTER TABLE products ADD COLUMN IF NOT EXISTS description TEXT",
        ]
        
        for migration in migrations:
            try:
                cursor.execute(migration)
                print(f"✓ Executed: {migration}")
            except mysql.connector.Error as e:
                if "Duplicate column name" in str(e):
                    print(f"⚠ Column already exists: {migration}")
                else:
                    print(f"✗ Error executing migration: {e}")
        
        # Commit changes
        connection.commit()
        print("✓ Database migration completed successfully!")
        
    except mysql.connector.Error as e:
        print(f"✗ Database error: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("Database connection closed.")

if __name__ == "__main__":
    migrate_database()
