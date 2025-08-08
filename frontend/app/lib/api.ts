import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Product types - Make sure these are exported
export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  currency: string;
  category: string;
  brand: string;
  image_url: string;
  rating: number;
  review_count: number;
  tags: string[];
  similarity_score?: number; // For AI search results
}

export interface SearchResponse {
  query: string;
  total_results: number;
  products: Product[];
}

export interface SearchParams {
  q: string;
  limit?: number;
  category?: string;
  min_price?: number;
  max_price?: number;
}

// Test connection to backend
export const testConnection = async () => {
  try {
    const response = await api.get('/');
    return response.data;
  } catch (error) {
    console.error('Backend connection failed:', error);
    throw error;
  }
};

// API functions
export const productApi = {
  // Get all products
  getProducts: () => 
    api.get<Product[]>('/api/products'),
  
  // Get single product
  getProduct: (id: number) =>
    api.get<Product>(`/api/products/${id}`),
  
  // AI-powered search
  searchProducts: (params: SearchParams) =>
    api.get<SearchResponse>('/api/search', { params }),
  
  // Refresh products from external APIs
  refreshProducts: () =>
    api.get('/api/refresh-products'),
};

// Chat API
export const chatApi = {
  sendMessage: (message: string, userId?: string) =>
    api.post('/api/chat', { message, user_id: userId }),
};