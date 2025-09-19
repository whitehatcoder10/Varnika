# Varnika Database Setup Guide

This guide will help you set up the complete database schema for the Varnika handicraft platform.

## 📋 Prerequisites

- MySQL 8.0+ installed and running
- Python 3.8+ with required packages
- Environment variables configured

## 🚀 Quick Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `backend` directory:

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=artisan_platform
GCLOUD_PROJECT_ID=your_project_id
REGION=us-central1
GCS_BUCKET_NAME=your_bucket_name
```

### 3. Run Database Setup

```bash
# From the Varnika root directory
python setup_database.py
```

Or manually:

```bash
# Import the complete schema
mysql -u root -p < complete_schema.sql

# Or run the migration script
cd backend
python migrate_database.py
```

## 📊 Database Schema

### Tables Created

1. **categories** - Product categories with descriptions and images
2. **artisans** - Artisan/seller information and profiles
3. **products** - Product listings with full details
4. **generatedcontent** - AI-generated product descriptions

### Key Features

- **Foreign Key Relationships**: Proper relationships between tables
- **Indexes**: Optimized for performance
- **Views**: Pre-built views for common queries
- **Sample Data**: Pre-populated with demo data
- **Active Status**: Soft delete functionality

## 🔧 Schema Details

### Categories Table
- `category_id` (Primary Key)
- `name` - Category name (unique)
- `description` - Category description
- `image_url` - Category image
- `is_active` - Active status

### Artisans Table
- `artisan_id` (Primary Key)
- `name` - Artisan name
- `email` - Email (unique)
- `password_hash` - Encrypted password
- `bio` - Artisan biography
- `profile_image_url` - Profile picture
- `address`, `city`, `state`, `country` - Location info
- `is_verified` - Verification status
- `is_active` - Active status

### Products Table
- `product_id` (Primary Key)
- `artisan_id` (Foreign Key to artisans)
- `category_id` (Foreign Key to categories)
- `name` - Product name
- `price` - Product price
- `description` - Product description
- `image_url` - Product image
- `category` - Category name (for compatibility)
- `stock_quantity` - Available stock
- `is_active` - Active status
- `is_featured` - Featured product flag
- `weight`, `dimensions`, `materials` - Product details
- `care_instructions`, `shipping_info` - Additional info
- `tags` - Product tags
- `view_count` - View counter

### Generated Content Table
- `content_id` (Primary Key)
- `product_id` (Foreign Key to products)
- `description_text` - AI-generated description
- `instagram_captions` - AI-generated captions
- `generation_prompt` - Original prompt used
- `ai_model_used` - AI model name
- `generation_time` - Time taken to generate

## 📈 Performance Optimizations

### Indexes Created
- `idx_products_search` - Full-text search on name and description
- `idx_products_category_active` - Category and active status
- `idx_artisans_email` - Email lookup
- `idx_categories_active` - Active categories

### Views Created
- `active_products` - All active products with related data
- `featured_products` - Featured products only

## 🧪 Sample Data

The database comes pre-populated with:

- **8 Categories**: Pottery, Textiles, Woodwork, Jewelry, Embroidery, Basketry, Leather, Metalwork
- **3 Artisans**: Sample artisan profiles
- **5 Products**: Sample products with descriptions
- **2 AI Generated Content**: Sample AI-generated descriptions

## 🔍 Verification

After setup, verify the database:

```sql
-- Check table counts
SELECT 
  (SELECT COUNT(*) FROM categories) as categories,
  (SELECT COUNT(*) FROM artisans) as artisans,
  (SELECT COUNT(*) FROM products) as products,
  (SELECT COUNT(*) FROM generatedcontent) as generated_content;

-- Check active products
SELECT COUNT(*) FROM active_products;

-- Check featured products
SELECT COUNT(*) FROM featured_products;
```

## 🚨 Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   # Grant permissions to your MySQL user
   mysql -u root -p
   GRANT ALL PRIVILEGES ON artisan_platform.* TO 'your_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

2. **Connection Refused**
   - Check if MySQL is running
   - Verify host and port settings
   - Check firewall settings

3. **Schema Already Exists**
   - The script handles existing tables gracefully
   - Use `DROP DATABASE artisan_platform;` to start fresh

4. **Frontend Shows "Failed to Load"**
   - Check if backend is running on port 5001
   - Verify database connection
   - Check browser console for errors

### Reset Database

```bash
# Drop and recreate database
mysql -u root -p -e "DROP DATABASE IF EXISTS artisan_platform;"
python setup_database.py
```

## 📝 Next Steps

1. Start the backend server:
   ```bash
   cd backend
   python app.py
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. Test the integration:
   ```bash
   python test_integration.py
   ```

## 🎯 Features Enabled

With this database setup, you get:

- ✅ Complete product management
- ✅ AI content generation
- ✅ Image enhancement
- ✅ Category filtering
- ✅ Artisan profiles
- ✅ Fallback data for offline mode
- ✅ Performance optimizations
- ✅ Data integrity with foreign keys

The frontend will no longer show "failed to load" errors and will gracefully fall back to demo data if the API is unavailable.
