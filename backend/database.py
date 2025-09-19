import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.connection_type = None

    def connect(self):
        try:
            # Check if Cloud SQL configuration is available
            cloud_sql_host = os.getenv("CLOUD_SQL_HOST")
            cloud_sql_user = os.getenv("CLOUD_SQL_USER")
            cloud_sql_password = os.getenv("CLOUD_SQL_PASSWORD")
            cloud_sql_database = os.getenv("CLOUD_SQL_DATABASE")
            cloud_sql_port = os.getenv("CLOUD_SQL_PORT", "3306")
            
            # Try Cloud SQL first if configured
            if cloud_sql_host and cloud_sql_user and cloud_sql_password:
                print("🌩️  Attempting to connect to Cloud SQL...")
                self.connection = mysql.connector.connect(
                    host=cloud_sql_host,
                    user=cloud_sql_user,
                    password=cloud_sql_password,
                    database=cloud_sql_database,
                    port=int(cloud_sql_port),
                    autocommit=True,
                    charset='utf8mb4',
                    collation='utf8mb4_unicode_ci',
                    use_unicode=True,
                    connect_timeout=60,
                    sql_mode='TRADITIONAL'
                )
                self.connection_type = "Cloud SQL"
                print("✅ Successfully connected to Cloud SQL database.")
            else:
                # Fallback to local MySQL
                print("🏠 Attempting to connect to local MySQL...")
                self.connection = mysql.connector.connect(
                    host=os.getenv("MYSQL_HOST", "localhost"),
                    user=os.getenv("MYSQL_USER", "root"),
                    password=os.getenv("MYSQL_PASSWORD", ""),
                    database=os.getenv("MYSQL_DATABASE", "artisan_platform")
                )
                self.connection_type = "Local MySQL"
                print("✅ Successfully connected to local MySQL database.")
            
            self.cursor = self.connection.cursor(dictionary=True) # dictionary=True makes rows accessible by column name
            
        except mysql.connector.Error as err:
            print(f"❌ Error connecting to database: {err}")
            print("\nTroubleshooting steps:")
            if self.connection_type == "Cloud SQL":
                print("1. Check if the Cloud SQL instance is running")
                print("2. Verify the IP address and port in .env file")
                print("3. Ensure the database exists")
                print("4. Check firewall rules allow your IP")
                print("5. Verify username and password")
            else:
                print("1. Check if MySQL is running locally")
                print("2. Verify connection parameters in .env file")
                print("3. Ensure the database exists")
                print("4. Check MySQL user permissions")

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print(f"MySQL connection ({self.connection_type}) is closed.")

    def get_connection_info(self):
        """Get information about the current connection"""
        if self.connection and self.connection.is_connected():
            return {
                "type": self.connection_type,
                "host": self.connection.server_host,
                "port": self.connection.server_port,
                "database": self.connection.database,
                "user": self.connection.user
            }
        return None

# Initialize the database class for use in other files
db = Database()