# Varnika Setup Instructions

## Backend Setup

1. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Database Setup**
   - Import the `Artisans_platform.sql` file into your MySQL database
   - Run the migration script to add missing fields:
     ```bash
     python migrate_database.py
     ```

3. **Environment Configuration**
   Create a `.env` file in the backend directory with:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=artisan_platform
   
   GCLOUD_PROJECT_ID=your_project_id
   REGION=us-central1
   GCS_BUCKET_NAME=your_bucket_name
   ```

4. **Start Backend Server**
   ```bash
   python app.py
   ```

## Frontend Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

## Features Implemented

### Seller Features
- ✅ Add products with name, price, category, and description
- ✅ Upload product images
- ✅ AI-powered image enhancement
- ✅ Voice-to-text description input
- ✅ AI-generated product descriptions and Instagram captions
- ✅ Real-time product listing

### Buyer Features
- ✅ Browse products by category
- ✅ View product details
- ✅ Add products to cart
- ✅ Shopping cart management

### Backend APIs
- ✅ GET /api/products - List all products
- ✅ POST /api/products - Add new product
- ✅ GET /api/products/{id} - Get specific product
- ✅ PUT /api/products/{id} - Update product
- ✅ DELETE /api/products/{id} - Delete product
- ✅ POST /api/generate_content - Generate AI content
- ✅ POST /api/enhance_image - Enhance product images

## Testing the Integration

1. Start both backend and frontend servers
2. Navigate to the frontend (usually http://localhost:5173)
3. Login as a seller
4. Go to "Add Product" page
5. Fill in product details, upload an image, and enhance it
6. Submit the product
7. Verify the product appears in the product listing
8. Test the buyer flow by switching to buyer mode
