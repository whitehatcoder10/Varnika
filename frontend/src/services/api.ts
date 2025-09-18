const API_BASE_URL = 'http://localhost:5001/api';

export interface Product {
  product_id: number;
  artisan_id: number;
  name: string;
  price: number;
  category: string;
  description: string;
  image_url: string;
  created_at: string;
  artisan_name?: string;
  description_text?: string;
  instagram_captions?: string;
}

export interface AddProductData {
  name: string;
  price: number;
  category: string;
  description: string;
  image_url: string;
  artisan_id?: number;
}

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || 'An error occurred',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  // Product APIs
  async getProducts(category?: string, artisanId?: number): Promise<ApiResponse<{ products: Product[] }>> {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (artisanId) params.append('artisan_id', artisanId.toString());
    
    const queryString = params.toString();
    const endpoint = queryString ? `/products?${queryString}` : '/products';
    
    return this.request<{ products: Product[] }>(endpoint);
  }

  async getProduct(productId: number): Promise<ApiResponse<{ product: Product }>> {
    return this.request<{ product: Product }>(`/products/${productId}`);
  }

  async addProduct(productData: AddProductData): Promise<ApiResponse<{ message: string; product_id: number }>> {
    return this.request<{ message: string; product_id: number }>('/products', {
      method: 'POST',
      body: JSON.stringify(productData),
    });
  }

  async updateProduct(productId: number, productData: Partial<AddProductData>): Promise<ApiResponse<{ message: string }>> {
    return this.request<{ message: string }>(`/products/${productId}`, {
      method: 'PUT',
      body: JSON.stringify(productData),
    });
  }

  async deleteProduct(productId: number): Promise<ApiResponse<{ message: string }>> {
    return this.request<{ message: string }>(`/products/${productId}`, {
      method: 'DELETE',
    });
  }

  // AI Content Generation APIs
  async generateContent(productType: string, keywords: string): Promise<ApiResponse<{ description: string; captions: string }>> {
    return this.request<{ description: string; captions: string }>('/generate_content', {
      method: 'POST',
      body: JSON.stringify({ product_type: productType, keywords }),
    });
  }

  async enhanceImage(imageFile: File, prompt?: string): Promise<ApiResponse<{ image_url: string }>> {
    const formData = new FormData();
    formData.append('image', imageFile);
    if (prompt) {
      formData.append('prompt', prompt);
    }

    try {
      const response = await fetch(`${API_BASE_URL}/enhance_image`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || 'Image enhancement failed',
        };
      }

      return {
        success: true,
        data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }
}

export const apiService = new ApiService();
