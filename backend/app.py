import os
import io
import re
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import db

# --- Vertex AI Imports ---
import vertexai
from vertexai.vision_models import ImageGenerationModel, Image as VisionImage
from vertexai.generative_models import GenerativeModel
from google.cloud import storage

# --- Initial Setup ---
load_dotenv()

PROJECT_ID = os.getenv("GCLOUD_PROJECT_ID")
REGION = os.getenv("REGION")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")

app = Flask(__name__)
CORS(app)

# --- AI and Cloud Initialization ---
vertexai.init(project=PROJECT_ID, location=REGION)

text_model = GenerativeModel(model_name="gemini-2.5-flash-lite")
image_generation_model = ImageGenerationModel.from_pretrained("imagegeneration@006")
storage_client = storage.Client()

# --- Database Connection ---
db.connect()

# --- Helper Function ---
def upload_to_gcs(bucket_name, file_bytes, destination_blob_name):
    """Uploads a file from an in-memory bytes buffer to a GCS bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    file_bytes.seek(0)
    blob.upload_from_file(file_bytes, content_type='image/jpeg')
    return blob.public_url

# --- API Endpoints ---

# Product Management APIs
@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products with optional filtering by category"""
    try:
        category = request.args.get('category')
        artisan_id = request.args.get('artisan_id')
        
        query = """
        SELECT p.*, a.name as artisan_name, gc.description_text, gc.instagram_captions
        FROM products p
        LEFT JOIN artisans a ON p.artisan_id = a.artisan_id
        LEFT JOIN generatedcontent gc ON p.product_id = gc.product_id
        WHERE 1=1
        """
        params = []
        
        if category:
            query += " AND p.category = %s"
            params.append(category)
            
        if artisan_id:
            query += " AND p.artisan_id = %s"
            params.append(artisan_id)
            
        query += " ORDER BY p.created_at DESC"
        
        db.cursor.execute(query, params)
        products = db.cursor.fetchall()
        
        return jsonify({"products": products})
        
    except Exception as e:
        print(f"Error fetching products: {e}")
        return jsonify({"error": "Failed to fetch products"}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product"""
    try:
        data = request.json
        name = data.get('name')
        price = data.get('price')
        category = data.get('category')
        description = data.get('description', '')
        artisan_id = data.get('artisan_id', 1)  # Default to artisan_id 1 for demo
        image_url = data.get('image_url', '')
        
        if not all([name, price, category]):
            return jsonify({"error": "Missing required fields"}), 400
        
        # Insert product
        insert_query = """
        INSERT INTO products (artisan_id, name, price, category, description, image_url)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        db.cursor.execute(insert_query, (artisan_id, name, price, category, description, image_url))
        product_id = db.cursor.lastrowid
        
        # Generate AI content if description is provided
        if description:
            try:
                prompt_text = (f"You are a skilled copywriter for handmade Indian crafts. "
                             f"Write a compelling product description and three Instagram captions with hashtags for a {category}. "
                             f"Product: {name}. Description: {description}. "
                             f"Format the output clearly with 'Description:' and 'Captions:' labels.")
                
                response = text_model.generate_content(prompt_text)
                generated_text = response.text
                
                description_match = re.search(r"Description:(.*?)Captions:", generated_text, re.DOTALL)
                captions_match = re.search(r"Captions:(.*)", generated_text, re.DOTALL)
                
                ai_description = description_match.group(1).strip() if description_match else description
                ai_captions = captions_match.group(1).strip() if captions_match else "Check out this amazing handmade product!"
                
                # Insert generated content
                content_query = """
                INSERT INTO generatedcontent (product_id, description_text, instagram_captions)
                VALUES (%s, %s, %s)
                """
                db.cursor.execute(content_query, (product_id, ai_description, ai_captions))
                
            except Exception as e:
                print(f"Error generating AI content: {e}")
                # Continue without AI content
        
        db.connection.commit()
        
        return jsonify({
            "message": "Product added successfully",
            "product_id": product_id
        }), 201
        
    except Exception as e:
        print(f"Error adding product: {e}")
        db.connection.rollback()
        return jsonify({"error": "Failed to add product"}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    try:
        query = """
        SELECT p.*, a.name as artisan_name, gc.description_text, gc.instagram_captions
        FROM products p
        LEFT JOIN artisans a ON p.artisan_id = a.artisan_id
        LEFT JOIN generatedcontent gc ON p.product_id = gc.product_id
        WHERE p.product_id = %s
        """
        db.cursor.execute(query, (product_id,))
        product = db.cursor.fetchone()
        
        if not product:
            return jsonify({"error": "Product not found"}), 404
            
        return jsonify({"product": product})
        
    except Exception as e:
        print(f"Error fetching product: {e}")
        return jsonify({"error": "Failed to fetch product"}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    try:
        data = request.json
        name = data.get('name')
        price = data.get('price')
        category = data.get('category')
        description = data.get('description')
        image_url = data.get('image_url')
        
        # Update product
        update_query = """
        UPDATE products 
        SET name = %s, price = %s, category = %s, description = %s, image_url = %s
        WHERE product_id = %s
        """
        db.cursor.execute(update_query, (name, price, category, description, image_url, product_id))
        
        if db.cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404
        
        db.connection.commit()
        
        return jsonify({"message": "Product updated successfully"})
        
    except Exception as e:
        print(f"Error updating product: {e}")
        db.connection.rollback()
        return jsonify({"error": "Failed to update product"}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        delete_query = "DELETE FROM products WHERE product_id = %s"
        db.cursor.execute(delete_query, (product_id,))
        
        if db.cursor.rowcount == 0:
            return jsonify({"error": "Product not found"}), 404
        
        db.connection.commit()
        
        return jsonify({"message": "Product deleted successfully"})
        
    except Exception as e:
        print(f"Error deleting product: {e}")
        db.connection.rollback()
        return jsonify({"error": "Failed to delete product"}), 500

@app.route('/api/generate_content', methods=['POST'])
def generate_content_endpoint():
    """API endpoint to generate product descriptions and captions from text."""
    try:
        data = request.json
        product_type = data.get('product_type', 'product')
        keywords = data.get('keywords', '')

        prompt_text = (f"You are a skilled copywriter for handmade Indian crafts. "
                       f"Write a compelling product description and three Instagram captions with hashtags for a {product_type}. "
                       f"Keywords: {keywords}. Format the output clearly with 'Description:' and 'Captions:' labels.")

        response = text_model.generate_content(prompt_text)
        generated_text = response.text

        description_match = re.search(r"Description:(.*?)Captions:", generated_text, re.DOTALL)
        captions_match = re.search(r"Captions:(.*)", generated_text, re.DOTALL)

        description = description_match.group(1).strip() if description_match else "Could not generate a description."
        captions = captions_match.group(1).strip() if captions_match else "Could not generate captions."

        return jsonify({
            "description": description,
            "captions": captions
        })

    except Exception as e:
        print(f"An error occurred in generate_content: {e}")
        return jsonify({"error": "An error occurred during content generation."}), 500

@app.route('/api/enhance_image', methods=['POST'])
def enhance_image_endpoint():
    """API endpoint to enhance a product image using AI."""
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files['image']
        prompt_text = request.form.get(
            'prompt',
            "Edit this low-quality product photo. Transform it into a professional, high-quality studio shot with soft, even lighting. Replace the cluttered background with  clean and balanced colours. Ensure the products are sharply in focus, well-composed, and elegantly displayed on minimalist light pink geometric risers. Add a subtle, blurred green botanical element in the background for a fresh, natural touch. The overall aesthetic should be modern, clean, and inviting, with minimal harsh shadows."
        )

        image_bytes = image_file.read()
        base_image = VisionImage(image_bytes=image_bytes)

        response = image_generation_model.edit_image(
            base_image=base_image,
            prompt=prompt_text,
            edit_mode="product-image",
            number_of_images=1,
        )

        generated_image = response.images[0]
        
        # --- THIS IS THE NEW FIX ---
        # 1. Access the raw image data from the private ._image_bytes attribute.
        #    This is necessary due to recent changes in the SDK.
        raw_image_bytes = generated_image._image_bytes
        # 2. Create an in-memory bytes buffer from this data for uploading.
        generated_image_bytes_io = io.BytesIO(raw_image_bytes)
        # --- End of FIX ---
        
        filename = f"enhanced_{os.urandom(16).hex()}.jpg"
        
        image_url = upload_to_gcs(BUCKET_NAME, generated_image_bytes_io, filename)

        return jsonify({"image_url": image_url})

    except Exception as e:
        print(f"An error occurred in enhance_image: {e}")
        return jsonify({"error": "An error occurred during image enhancement."}), 500

# --- Run the Application ---
if __name__ == '__main__':
    app.run(debug=True, port=5001)