# Google Cloud SQL Setup Guide for Varnika

This guide will help you configure Google Cloud SQL for the Varnika platform.

## 🚀 Quick Setup

### 1. Get Cloud SQL Instance Details

```bash
# Get connection name and IP address
gcloud sql instances describe varnika-instance-final --format="value(connectionName,ipAddresses[0].ipAddress)"

# Example output:
# your-project:us-central1:varnika-instance-final
# 34.123.45.67
```

### 2. Create Database

```bash
# Create the artisan_platform database
gcloud sql databases create artisan_platform --instance=varnika-instance-final
```

### 3. Set Root Password

```bash
# Set root password (replace YOUR_PASSWORD with your desired password)
gcloud sql users set-password root --host=% --instance=varnika-instance-final --password=YOUR_PASSWORD
```

### 4. Configure Authorized Networks

```bash
# Add your IP address to authorized networks
gcloud sql instances patch varnika-instance-final --authorized-networks=YOUR_IP_ADDRESS/32

# To get your current IP:
curl ifconfig.me
```

### 5. Update Environment Configuration

Create a `.env` file in the `backend` directory:

```env
# Cloud SQL Configuration
CLOUD_SQL_HOST=34.123.45.67
CLOUD_SQL_USER=root
CLOUD_SQL_PASSWORD=YOUR_PASSWORD
CLOUD_SQL_DATABASE=artisan_platform
CLOUD_SQL_PORT=3306

# Google Cloud Configuration
GCLOUD_PROJECT_ID=your_project_id
REGION=us-central1
GCS_BUCKET_NAME=your_bucket_name

# Fallback Local MySQL (optional)
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_local_password
MYSQL_DATABASE=artisan_platform
```

## 🔧 Test Connection

### Test Cloud SQL Connection

```bash
# Test the connection
python cloud_sql_connection.py
```

### Expected Output

```
🌩️  Varnika Cloud SQL Setup
==================================================
Connecting to Cloud SQL instance: 34.123.45.67
Database: artisan_platform
User: root
✅ Connected to Cloud SQL successfully!
✅ MySQL version: 8.0.35
✅ Available databases: ['information_schema', 'mysql', 'performance_schema', 'sys', 'artisan_platform']
✅ Connection test successful!

🚀 Setting up database schema...
📖 Reading complete_schema.sql file...
  Executed 10 statements...
  Executed 20 statements...
✅ Database setup completed successfully! Executed 25 statements.

✅ Database verification:
  - Categories: 8
  - Artisans: 3
  - Products: 5
  - Generated Content: 2

✅ Cloud SQL database setup completed!
```

## 🚀 Start the Application

### 1. Start Backend

```bash
cd backend
python app.py
```

You should see:
```
🌩️  Attempting to connect to Cloud SQL...
✅ Successfully connected to Cloud SQL database.
 * Running on http://127.0.0.1:5001
```

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Connection Refused
```
❌ Cloud SQL connection failed: 2003: Can't connect to MySQL server on '34.123.45.67:3306' (Connection refused)
```

**Solutions:**
- Check if the Cloud SQL instance is running
- Verify the IP address is correct
- Check if your IP is in authorized networks
- Ensure the instance is not in maintenance mode

#### 2. Access Denied
```
❌ Cloud SQL connection failed: 1045: Access denied for user 'root'@'your-ip' (using password: YES)
```

**Solutions:**
- Verify the password is correct
- Check if the user exists
- Ensure the user has proper permissions

#### 3. Database Not Found
```
❌ Cloud SQL connection failed: 1049: Unknown database 'artisan_platform'
```

**Solutions:**
- Create the database: `gcloud sql databases create artisan_platform --instance=varnika-instance-final`
- Verify the database name in .env file

#### 4. Timeout
```
❌ Cloud SQL connection failed: 2013: Lost connection to MySQL server during query
```

**Solutions:**
- Check network connectivity
- Increase connection timeout
- Verify firewall rules

### Debug Commands

```bash
# Check instance status
gcloud sql instances describe varnika-instance-final

# Check databases
gcloud sql databases list --instance=varnika-instance-final

# Check users
gcloud sql users list --instance=varnika-instance-final

# Check authorized networks
gcloud sql instances describe varnika-instance-final --format="value(settings.ipConfiguration.authorizedNetworks[].value)"
```

## 📊 Verify Setup

### Check Database Tables

```bash
# Connect to Cloud SQL
gcloud sql connect varnika-instance-final --user=root --database=artisan_platform

# In MySQL prompt:
SHOW TABLES;
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM artisans;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM generatedcontent;
```

### Test API Endpoints

```bash
# Test products endpoint
curl http://localhost:5001/api/products

# Test specific product
curl http://localhost:5001/api/products/1
```

## 🔒 Security Best Practices

1. **Use Strong Passwords**: Set a strong root password
2. **Limit Authorized Networks**: Only add necessary IP addresses
3. **Use SSL**: Enable SSL connections for production
4. **Regular Backups**: Set up automated backups
5. **Monitor Access**: Enable Cloud SQL audit logs

## 📈 Performance Optimization

1. **Connection Pooling**: Use connection pooling for production
2. **Indexes**: Ensure proper indexes are created
3. **Query Optimization**: Monitor slow queries
4. **Resource Scaling**: Adjust instance size as needed

## 🎯 Next Steps

1. ✅ Cloud SQL instance configured
2. ✅ Database created and populated
3. ✅ Backend connected to Cloud SQL
4. ✅ Frontend displaying data
5. 🚀 Deploy to production!

Your Varnika platform is now running on Google Cloud SQL! 🌩️


