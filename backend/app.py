import os
import io
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

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

# --- Helper Function ---
def upload_to_gcs(bucket_name, file_bytes, destination_blob_name):
    """Uploads a file from an in-memory bytes buffer to a GCS bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    file_bytes.seek(0)
    blob.upload_from_file(file_bytes, content_type='image/jpeg')
    return blob.public_url

# --- API Endpoints ---

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
            "Enhance this product photo. Give it a clean, white background, soft studio lighting, and make it look professional and high-resolution, suitable for e-commerce."
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
    app.run(debug=True, port=5000)