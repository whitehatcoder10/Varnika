#!/usr/bin/env python3
"""
Populate Cloud SQL with corrected sample data for Varnika platform
"""

import mysql.connector
import os
from dotenv import load_dotenv

def populate_corrected_data():
    """Populate the database with corrected sample data"""
    print("🌩️  Populating Cloud SQL with Corrected Sample Data")
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
        
        # Clear existing data first
        print("🧹 Clearing existing data...")
        cursor.execute("DELETE FROM generatedcontent")
        cursor.execute("DELETE FROM products")
        cursor.execute("DELETE FROM artisans")
        print("✅ Existing data cleared")
        
        # Insert sample artisans with correct schema
        print("\n👨‍🎨 Adding sample artisans...")
        artisans_data = [
            ('Rajesh Kumar', 'rajesh@example.com', 'password123', '+91-9876543210', 'Master potter with 20 years of experience in traditional ceramics', 'https://example.com/rajesh.jpg', '123 Main Street', 'Delhi', 'Delhi', 'India', '110001', 1, 1),
            ('Priya Sharma', 'priya@example.com', 'password123', '+91-9876543211', 'Expert weaver specializing in handwoven textiles and fabrics', 'https://example.com/priya.jpg', '456 Craft Lane', 'Jaipur', 'Rajasthan', 'India', '302001', 1, 1),
            ('Amit Singh', 'amit@example.com', 'password123', '+91-9876543212', 'Skilled woodworker creating beautiful handicrafts and furniture', 'https://example.com/amit.jpg', '789 Wood Street', 'Varanasi', 'Uttar Pradesh', 'India', '221001', 1, 1)
        ]
        
        for artisan in artisans_data:
            cursor.execute("""
                INSERT INTO artisans (name, email, password_hash, phone, bio, profile_image_url, address, city, state, country, pincode, is_verified, is_active)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, artisan)
            print(f"  ✅ Added artisan: {artisan[0]}")
        
        # Get artisan IDs
        cursor.execute("SELECT artisan_id, name FROM artisans")
        artisans = cursor.fetchall()
        artisan_map = {name: artisan_id for artisan_id, name in artisans}
        
        # Get category IDs
        cursor.execute("SELECT category_id, name FROM categories")
        categories = cursor.fetchall()
        category_map = {name: category_id for category_id, name in categories}
        
        # Insert sample products with correct schema
        print("\n🛍️  Adding sample products...")
        products_data = [
            ('Handcrafted Ceramic Vase', 2500.00, 'Beautiful handcrafted ceramic vase with traditional Indian motifs. Perfect for home decoration.', 'https://example.com/vase1.jpg', 'Pottery', 10, 1, 0, 2.5, '12x8x8 inches', 'Clay, Natural Glaze', 'Handle with care, avoid direct sunlight', 'Free shipping across India', 'ceramic,vase,pottery,traditional', 0),
            ('Silk Saree with Gold Work', 8500.00, 'Elegant silk saree with intricate gold embroidery. Traditional craftsmanship at its finest.', 'https://example.com/saree1.jpg', 'Textiles', 5, 1, 1, 0.8, '6 yards', 'Pure Silk, Gold Thread', 'Dry clean only', 'Express shipping available', 'silk,saree,gold,embroidery', 0),
            ('Wooden Jewelry Box', 1800.00, 'Exquisite wooden jewelry box with hand-carved designs. Made from premium teak wood.', 'https://example.com/jewelry_box.jpg', 'Woodwork', 8, 1, 0, 1.2, '8x6x4 inches', 'Teak Wood, Brass Hinges', 'Polish with soft cloth', 'Standard shipping', 'wooden,jewelry,box,handmade', 0),
            ('Terracotta Pot Set', 1200.00, 'Set of 3 terracotta pots in different sizes. Perfect for plants and home decoration.', 'https://example.com/pots.jpg', 'Pottery', 15, 1, 0, 3.0, 'Various sizes', 'Terracotta Clay', 'Water regularly', 'Free shipping', 'terracotta,pots,plants,decor', 0),
            ('Cotton Table Runner', 800.00, 'Handwoven cotton table runner with traditional patterns. Adds elegance to any dining table.', 'https://example.com/table_runner.jpg', 'Textiles', 20, 1, 0, 0.3, '60x12 inches', 'Pure Cotton', 'Machine wash cold', 'Standard shipping', 'cotton,table,runner,handwoven', 0)
        ]
        
        for i, product in enumerate(products_data, 1):
            # Map artisan and category
            artisan_names = ['Rajesh Kumar', 'Priya Sharma', 'Amit Singh', 'Rajesh Kumar', 'Priya Sharma']
            category_names = ['Pottery', 'Textiles', 'Woodwork', 'Pottery', 'Textiles']
            
            artisan_id = artisan_map[artisan_names[i-1]]
            category_id = category_map.get(category_names[i-1], 1)  # Default to category 1 if not found
            
            cursor.execute("""
                INSERT INTO products (artisan_id, category_id, name, price, description, image_url, category, stock_quantity, is_active, is_featured, weight, dimensions, materials, care_instructions, shipping_info, tags, view_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (artisan_id, category_id) + product)
            print(f"  ✅ Added product: {product[0]}")
        
        # Get product IDs
        cursor.execute("SELECT product_id, name FROM products")
        products = cursor.fetchall()
        product_map = {name: product_id for product_id, name in products}
        
        # Insert sample generated content
        print("\n🤖 Adding sample AI-generated content...")
        content_data = [
            ('Handcrafted Ceramic Vase', 'This exquisite handcrafted ceramic vase is a masterpiece of traditional Indian pottery. Each piece is carefully molded by skilled artisans using age-old techniques passed down through generations. The intricate motifs and patterns tell stories of our rich cultural heritage, making this vase not just a decorative piece but a conversation starter. The smooth finish and perfect proportions make it ideal for displaying fresh flowers or as a standalone art piece. Crafted with love and attention to detail, this vase will add elegance and warmth to any space.'),
            ('Silk Saree with Gold Work', 'Experience the luxury of authentic Indian silk with this stunning saree adorned with intricate gold work. Every thread tells a story of tradition, every pattern reflects the skill of master craftsmen. The rich fabric drapes beautifully, creating an elegant silhouette that celebrates the timeless beauty of Indian women. Perfect for special occasions, festivals, or when you want to make a statement. This saree is not just clothing; it\'s a piece of art that honors centuries of textile craftsmanship.')
        ]
        
        for product_name, description in content_data:
            if product_name in product_map:
                product_id = product_map[product_name]
                cursor.execute("""
                    INSERT INTO generatedcontent (product_id, description_text)
                    VALUES (%s, %s)
                """, (product_id, description))
                print(f"  ✅ Added AI content for: {product_name}")
        
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
        
        # Show sample data
        print("\n📋 Sample Data Preview:")
        cursor.execute("SELECT name, city, state FROM artisans LIMIT 3")
        artisans = cursor.fetchall()
        for artisan in artisans:
            print(f"  👨‍🎨 {artisan[0]} from {artisan[1]}, {artisan[2]}")
        
        cursor.execute("SELECT name, price, category FROM products LIMIT 3")
        products = cursor.fetchall()
        for product in products:
            print(f"  🛍️  {product[0]} - ₹{product[1]} ({product[2]})")
        
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
    populate_corrected_data()
