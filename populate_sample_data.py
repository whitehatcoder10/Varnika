#!/usr/bin/env python3
"""
Populate Cloud SQL with sample data for Varnika platform
"""

import mysql.connector
import os
from dotenv import load_dotenv

def populate_sample_data():
    """Populate the database with sample data"""
    print("🌩️  Populating Cloud SQL with Sample Data")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv("backend/.env")
    
    host = os.getenv('CLOUD_SQL_HOST', '104.197.43.172')
    user = os.getenv('CLOUD_SQL_USER', 'Aayush')
    password = os.getenv('CLOUD_SQL_PASSWORD')
    database = os.getenv('CLOUD_SQL_DATABASE', 'artisan_platform')
    port = int(os.getenv('CLOUD_SQL_PORT', '3306'))
    
    try:
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
        cursor = connection.cursor()
        
        # Insert sample artisans
        print("👨‍🎨 Adding sample artisans...")
        artisans_data = [
            (1, 'Rajesh Kumar', 'rajesh@example.com', 'Delhi', 'Traditional pottery and ceramics', 'https://example.com/rajesh.jpg'),
            (2, 'Priya Sharma', 'priya@example.com', 'Jaipur', 'Handwoven textiles and fabrics', 'https://example.com/priya.jpg'),
            (3, 'Amit Singh', 'amit@example.com', 'Varanasi', 'Wooden handicrafts and furniture', 'https://example.com/amit.jpg')
        ]
        
        for artisan in artisans_data:
            try:
                cursor.execute("""
                    INSERT INTO artisans (artisan_id, name, email, location, specialization, profile_image_url)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    email = VALUES(email),
                    location = VALUES(location),
                    specialization = VALUES(specialization),
                    profile_image_url = VALUES(profile_image_url)
                """, artisan)
                print(f"  ✅ Added artisan: {artisan[1]}")
            except Exception as e:
                print(f"  ⚠️  Artisan {artisan[1]} already exists or error: {e}")
        
        # Insert sample products
        print("\n🛍️  Adding sample products...")
        products_data = [
            (1, 1, 1, 'Handcrafted Ceramic Vase', 2500.00, 'Pottery', 'Beautiful handcrafted ceramic vase with traditional Indian motifs. Perfect for home decoration.', 'https://example.com/vase1.jpg', True),
            (2, 2, 2, 'Silk Saree with Gold Work', 8500.00, 'Textiles', 'Elegant silk saree with intricate gold embroidery. Traditional craftsmanship at its finest.', 'https://example.com/saree1.jpg', True),
            (3, 3, 3, 'Wooden Jewelry Box', 1800.00, 'Woodwork', 'Exquisite wooden jewelry box with hand-carved designs. Made from premium teak wood.', 'https://example.com/jewelry_box.jpg', True),
            (4, 1, 1, 'Terracotta Pot Set', 1200.00, 'Pottery', 'Set of 3 terracotta pots in different sizes. Perfect for plants and home decoration.', 'https://example.com/pots.jpg', True),
            (5, 2, 2, 'Cotton Table Runner', 800.00, 'Textiles', 'Handwoven cotton table runner with traditional patterns. Adds elegance to any dining table.', 'https://example.com/table_runner.jpg', True)
        ]
        
        for product in products_data:
            try:
                cursor.execute("""
                    INSERT INTO products (product_id, artisan_id, category_id, name, price, category, description, image_url, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    price = VALUES(price),
                    description = VALUES(description),
                    image_url = VALUES(image_url),
                    is_active = VALUES(is_active)
                """, product)
                print(f"  ✅ Added product: {product[3]}")
            except Exception as e:
                print(f"  ⚠️  Product {product[3]} already exists or error: {e}")
        
        # Insert sample generated content
        print("\n🤖 Adding sample AI-generated content...")
        content_data = [
            (1, 1, 'This exquisite handcrafted ceramic vase is a masterpiece of traditional Indian pottery. Each piece is carefully molded by skilled artisans using age-old techniques passed down through generations. The intricate motifs and patterns tell stories of our rich cultural heritage, making this vase not just a decorative piece but a conversation starter. The smooth finish and perfect proportions make it ideal for displaying fresh flowers or as a standalone art piece. Crafted with love and attention to detail, this vase will add elegance and warmth to any space.'),
            (2, 2, 'Experience the luxury of authentic Indian silk with this stunning saree adorned with intricate gold work. Every thread tells a story of tradition, every pattern reflects the skill of master craftsmen. The rich fabric drapes beautifully, creating an elegant silhouette that celebrates the timeless beauty of Indian women. Perfect for special occasions, festivals, or when you want to make a statement. This saree is not just clothing; it\'s a piece of art that honors centuries of textile craftsmanship.')
        ]
        
        for content in content_data:
            try:
                cursor.execute("""
                    INSERT INTO generatedcontent (content_id, product_id, description_text)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    description_text = VALUES(description_text)
                """, content)
                print(f"  ✅ Added AI content for product {content[1]}")
            except Exception as e:
                print(f"  ⚠️  Content for product {content[1]} already exists or error: {e}")
        
        # Verify the data
        print("\n📊 Verifying sample data...")
        cursor.execute("SELECT COUNT(*) FROM artisans")
        artisans_count = cursor.fetchone()[0]
        print(f"✅ Artisans: {artisans_count}")
        
        cursor.execute("SELECT COUNT(*) FROM products")
        products_count = cursor.fetchone()[0]
        print(f"✅ Products: {products_count}")
        
        cursor.execute("SELECT COUNT(*) FROM generatedcontent")
        content_count = cursor.fetchone()[0]
        print(f"✅ Generated content: {content_count}")
        
        cursor.close()
        connection.close()
        
        print("\n🎉 Sample data populated successfully!")
        print("Your Varnika platform now has sample artisans and products to display!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    populate_sample_data()
