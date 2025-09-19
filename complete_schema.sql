-- Varnika Complete Database Schema
-- This file contains all tables required for the Varnika handicraft platform

CREATE DATABASE IF NOT EXISTS `artisan_platform` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_0900_ai_ci;

USE `artisan_platform`;

-- Drop existing tables if they exist (in correct order due to foreign keys)
DROP TABLE IF EXISTS `generatedcontent`;
DROP TABLE IF EXISTS `products`;
DROP TABLE IF EXISTS `artisans`;
DROP TABLE IF EXISTS `categories`;

-- Create categories table
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` text,
  `image_url` varchar(500),
  `is_active` boolean DEFAULT TRUE,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `unique_category_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create artisans table
CREATE TABLE `artisans` (
  `artisan_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `phone` varchar(20),
  `bio` text,
  `profile_image_url` varchar(500),
  `address` text,
  `city` varchar(100),
  `state` varchar(100),
  `country` varchar(100),
  `pincode` varchar(10),
  `is_verified` boolean DEFAULT FALSE,
  `is_active` boolean DEFAULT TRUE,
  `join_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`artisan_id`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `idx_artisan_active` (`is_active`),
  KEY `idx_artisan_verified` (`is_verified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create products table
CREATE TABLE `products` (
  `product_id` int NOT NULL AUTO_INCREMENT,
  `artisan_id` int NOT NULL,
  `category_id` int,
  `name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text,
  `image_url` varchar(500),
  `category` varchar(100) DEFAULT 'General',
  `stock_quantity` int DEFAULT 0,
  `is_active` boolean DEFAULT TRUE,
  `is_featured` boolean DEFAULT FALSE,
  `weight` decimal(8,2),
  `dimensions` varchar(100),
  `materials` varchar(255),
  `care_instructions` text,
  `shipping_info` text,
  `tags` text,
  `view_count` int DEFAULT 0,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`product_id`),
  KEY `artisan_id` (`artisan_id`),
  KEY `category_id` (`category_id`),
  KEY `idx_product_active` (`is_active`),
  KEY `idx_product_featured` (`is_featured`),
  KEY `idx_product_category` (`category`),
  KEY `idx_product_price` (`price`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`artisan_id`) REFERENCES `artisans` (`artisan_id`) ON DELETE CASCADE,
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Create generatedcontent table
CREATE TABLE `generatedcontent` (
  `content_id` int NOT NULL AUTO_INCREMENT,
  `product_id` int NOT NULL,
  `description_text` text,
  `instagram_captions` text,
  `generation_prompt` text,
  `ai_model_used` varchar(100),
  `generation_time` decimal(10,3),
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`content_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `generatedcontent_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Insert sample categories
INSERT INTO `categories` (`name`, `description`, `image_url`) VALUES
('Pottery', 'Handcrafted ceramic and clay products', 'https://images.unsplash.com/photo-1695746999130-17bc94e000e8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwb3R0ZXJ5JTIwaGFuZGljcmFmdCUyMGNlcmFtaWN8ZW58MXx8fHwxNzU4MjAyOTM0fDA&ixlib=rb-4.1.0&q=80&w=300'),
('Textiles', 'Handwoven fabrics and textile products', 'https://images.unsplash.com/photo-1719462211900-3d4c1a62cae4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZXh0aWxlJTIwd2VhdmluZyUyMGhhbmRpY3JhZnR8ZW58MXx8fHwxNzU4MjAyOTM1fDA&ixlib=rb-4.1.0&q=80&w=300'),
('Woodwork', 'Hand-carved wooden items and furniture', 'https://images.unsplash.com/photo-1603789766884-aef036cd3b5a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b29kd29yayUyMGhhbmRpY3JhZnQlMjBjYXJ2aW5nfGVufDF8fHx8MTc1ODIwMjkzNXww&ixlib=rb-4.1.0&q=80&w=300'),
('Jewelry', 'Handcrafted jewelry and accessories', 'https://images.unsplash.com/photo-1717917197052-fda91a7e003c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxqZXdlbHJ5JTIwaGFuZGljcmFmdCUyMHRyYWRpdGlvbmFsfGVufDF8fHx8MTc1ODIwMjkzNnww&ixlib=rb-4.1.0&q=80&w=400'),
('Embroidery', 'Hand-embroidered textiles and garments', 'https://images.unsplash.com/photo-1657470036063-c7e49da31393?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxlbWJyb2lkZXJ5JTIwaGFuZGljcmFmdCUyMHRleHRpbGV8ZW58MXx8fHwxNzU4MjAyOTM2fDA&ixlib=rb-4.1.0&q=80&w=400'),
('Basketry', 'Handwoven baskets and containers', 'https://images.unsplash.com/photo-1617191598003-fa321e7e425b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiYXNrZXQlMjB3ZWF2aW5nJTIwaGFuZGljcmFmdHxlbnwxfHx8fDE3NTgyMDI5MzZ8MA&ixlib=rb-4.1.0&q=80&w=400'),
('Leather', 'Handcrafted leather goods', 'https://images.unsplash.com/photo-1543874835-ad7d64196a07?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxsZWF0aGVyJTIwaGFuZGljcmFmdCUyMHRyYWRpdGlvbmFsfGVufDF8fHx8MTc1ODIwMjkzN3ww&ixlib=rb-4.1.0&q=80&w=400'),
('Metalwork', 'Hand-forged metal items and sculptures', 'https://images.unsplash.com/photo-1638256049300-d5fbdae0e8c7?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxtZXRhbCUyMGhhbmRpY3JhZnQlMjBjcmFmdHxlbnwxfHx8fDE3NTgyMDI5Mzd8MA&ixlib=rb-4.1.0&q=80&w=400');

-- Insert sample artisan
INSERT INTO `artisans` (`name`, `email`, `password_hash`, `bio`, `is_verified`, `is_active`) VALUES
('Jane Smith', 'jane@example.com', 'hashed_password_123', 'Passionate ceramic artist from India with 15 years of experience in traditional pottery techniques.', TRUE, TRUE),
('Rajesh Kumar', 'rajesh@example.com', 'hashed_password_456', 'Master woodworker specializing in traditional Indian furniture and decorative items.', TRUE, TRUE),
('Priya Sharma', 'priya@example.com', 'hashed_password_789', 'Expert textile weaver creating beautiful handloom fabrics and garments.', TRUE, TRUE);

-- Insert sample products
INSERT INTO `products` (`artisan_id`, `category_id`, `name`, `price`, `description`, `image_url`, `category`, `stock_quantity`, `is_active`, `is_featured`) VALUES
(1, 1, 'Handcrafted Ceramic Vase', 85.00, 'Beautiful handmade ceramic vase with traditional glazing techniques, perfect for home decor.', 'https://images.unsplash.com/photo-1695746999130-17bc94e000e8?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxwb3R0ZXJ5JTIwaGFuZGljcmFmdCUyMGNlcmFtaWN8ZW58MXx8fHwxNzU4MjAyOTM0fDA&ixlib=rb-4.1.0&q=80&w=400', 'Pottery', 10, TRUE, TRUE),
(2, 3, 'Carved Wooden Bowl', 65.00, 'Hand-carved wooden bowl made from sustainable wood with intricate traditional patterns.', 'https://images.unsplash.com/photo-1603789766884-aef036cd3b5a?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx3b29kd29yayUyMGhhbmRpY3JhZnQlMjBjYXJ2aW5nfGVufDF8fHx8MTc1ODIwMjkzNXww&ixlib=rb-4.1.0&q=80&w=400', 'Woodwork', 5, TRUE, TRUE),
(3, 2, 'Woven Cotton Scarf', 45.00, 'Soft cotton scarf with intricate woven patterns, handcrafted using traditional techniques.', 'https://images.unsplash.com/photo-1719462211900-3d4c1a62cae4?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHx0ZXh0aWxlJTIwd2VhdmluZyUyMGhhbmRpY3JhZnR8ZW58MXx8fHwxNzU4MjAyOTM1fDA&ixlib=rb-4.1.0&q=80&w=400', 'Textiles', 15, TRUE, FALSE),
(1, 4, 'Silver Filigree Earrings', 120.00, 'Delicate silver earrings with traditional filigree work, perfect for special occasions.', 'https://images.unsplash.com/photo-1717917197052-fda91a7e003c?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxqZXdlbHJ5JTIwaGFuZGljcmFmdCUyMHRyYWRpdGlvbmFsfGVufDF8fHx8MTc1ODIwMjkzNnww&ixlib=rb-4.1.0&q=80&w=400', 'Jewelry', 8, TRUE, TRUE),
(3, 5, 'Embroidered Wall Hanging', 95.00, 'Traditional embroidered wall art with vibrant colors and intricate patterns.', 'https://images.unsplash.com/photo-1657470036063-c7e49da31393?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxlbWJyb2lkZXJ5JTIwaGFuZGljcmFmdCUyMHRleHRpbGV8ZW58MXx8fHwxNzU4MjAyOTM2fDA&ixlib=rb-4.1.0&q=80&w=400', 'Embroidery', 3, TRUE, FALSE);

-- Insert sample generated content
INSERT INTO `generatedcontent` (`product_id`, `description_text`, `instagram_captions`, `ai_model_used`) VALUES
(1, 'Transform your living space with this exquisite handcrafted ceramic vase that embodies the rich heritage of Indian pottery. Each piece is meticulously created by skilled artisans using time-honored techniques passed down through generations. The intricate glazing and traditional patterns make this vase a true work of art that will add elegance and cultural charm to any home decor.', 'Discover the beauty of traditional Indian craftsmanship! ✨ #Handmade #Ceramics #IndianArt #HomeDecor #ArtisanCraft', 'gemini-2.5-flash-lite'),
(2, 'Crafted from sustainably sourced wood, this hand-carved bowl showcases the exceptional skill of traditional Indian woodworkers. The intricate patterns and smooth finish demonstrate the artisan\'s dedication to preserving ancient carving techniques. Perfect for serving or as a decorative centerpiece, this bowl brings natural beauty and cultural authenticity to your home.', 'Nature meets artistry in this stunning hand-carved wooden bowl! 🌿 #Woodwork #Handmade #Sustainable #IndianCraft #HomeDecor', 'gemini-2.5-flash-lite');

-- Create indexes for better performance
CREATE INDEX idx_products_search ON products(name, description);
CREATE INDEX idx_products_category_active ON products(category, is_active);
CREATE INDEX idx_artisans_email ON artisans(email);
CREATE INDEX idx_categories_active ON categories(is_active);

-- Create views for easier querying
CREATE VIEW active_products AS
SELECT 
    p.product_id,
    p.name,
    p.price,
    p.description,
    p.image_url,
    p.category,
    p.stock_quantity,
    p.is_featured,
    p.created_at,
    a.name as artisan_name,
    a.email as artisan_email,
    c.name as category_name,
    gc.description_text as ai_description
FROM products p
LEFT JOIN artisans a ON p.artisan_id = a.artisan_id
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN generatedcontent gc ON p.product_id = gc.product_id
WHERE p.is_active = TRUE AND a.is_active = TRUE;

CREATE VIEW featured_products AS
SELECT 
    p.product_id,
    p.name,
    p.price,
    p.description,
    p.image_url,
    p.category,
    p.stock_quantity,
    p.created_at,
    a.name as artisan_name,
    c.name as category_name,
    gc.description_text as ai_description
FROM products p
LEFT JOIN artisans a ON p.artisan_id = a.artisan_id
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN generatedcontent gc ON p.product_id = gc.product_id
WHERE p.is_active = TRUE AND p.is_featured = TRUE AND a.is_active = TRUE;

-- Grant permissions (adjust as needed for your setup)
-- GRANT ALL PRIVILEGES ON artisan_platform.* TO 'your_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Show completion message
SELECT 'Database schema created successfully!' as status;
SELECT COUNT(*) as total_categories FROM categories;
SELECT COUNT(*) as total_artisans FROM artisans;
SELECT COUNT(*) as total_products FROM products;
SELECT COUNT(*) as total_generated_content FROM generatedcontent;
