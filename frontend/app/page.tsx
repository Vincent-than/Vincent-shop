'use client';

import { useState, useEffect } from 'react';
import { testConnection, productApi } from './lib/api';
import { ShoppingCart, Wifi, WifiOff, Sparkles } from 'lucide-react';
import SearchBar from './components/searchbar';
import ProductCard from './components/productcard';
import Cart from './components/cart';
import ChatAssistant from './components/chatassistant';
import Advanced3DBackground from './components/background';

// Define types inline to avoid import issues
interface Product {
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
  similarity_score?: number;
}

interface SearchResponse {
  query: string;
  total_results: number;
  products: Product[];
}

export default function Home() {
  const [backendStatus, setBackendStatus] = useState<string>('checking...');
  const [backendData, setBackendData] = useState<any>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Check backend connection and load initial products
  useEffect(() => {
    const checkBackend = async () => {
      try {
        const data = await testConnection();
        setBackendData(data);
        setBackendStatus('connected');
        
        // Load initial products
        const productsResponse = await productApi.getProducts();
        setProducts(productsResponse.data);
      } catch (error) {
        setBackendStatus('disconnected');
        console.error('Failed to connect to backend:', error);
      }
    };

    checkBackend();
  }, []);

  // Handle search functionality
  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setHasSearched(true);
    
    
    try {
      const response = await productApi.searchProducts({ q: query });
      setSearchResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
      setSearchResults(null);
    } finally {
      setIsLoading(false);
    }
  };

  const displayProducts = searchResults ? searchResults.products : products;


  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Advanced 3D Particle Background */}
      <Advanced3DBackground />
      
      {/* Gradient overlay for better text readability */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50/80 via-indigo-50/60 to-purple-50/80 z-10"></div>
      
      {/* 3D Cart Component */}
      <Cart />
      
      {/* AI Chat Assistant */}
      <ChatAssistant />
      
      <div className="relative z-20 container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <div className="relative">
              <ShoppingCart className="h-12 w-12 text-blue-600 mr-3 animate-pulse" />
              <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full animate-ping"></div>
            </div>
            <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 bg-clip-text text-transparent">
              Vincent Shopping
            </h1>
            <Sparkles className="h-8 w-8 text-yellow-500 ml-2 animate-bounce" />
          </div>
          <p className="text-xl text-gray-600 mb-6">Just for testing purpose</p>
          
          {/* Backend Connection Status */}
          <div className="max-w-md mx-auto mb-6">
            <div className={`p-3 rounded-xl border-2 transition-all duration-300 transform hover:scale-105 ${
              backendStatus === 'connected' 
                ? 'bg-green-50 border-green-200 shadow-lg shadow-green-100' 
                : backendStatus === 'disconnected'
                ? 'bg-red-50 border-red-200 shadow-lg shadow-red-100'
                : 'bg-yellow-50 border-yellow-200 shadow-lg shadow-yellow-100'
            }`}>
              <div className="flex items-center justify-center">
                {backendStatus === 'connected' ? (
                  <Wifi className="h-4 w-4 text-green-600 mr-2 animate-pulse" />
                ) : (
                  <WifiOff className="h-4 w-4 text-red-600 mr-2" />
                )}
                <span className="text-sm font-bold">
                  🤖 Backend: {backendStatus}
                </span>
              </div>
            </div>
          </div>

          {/* Search Bar */}
          <div className="transform hover:scale-105 transition-transform duration-300">
            <SearchBar 
              onSearch={handleSearch} 
              isLoading={isLoading}
              placeholder="Try: 'comfortable running shoes' or 'budget laptop for students'"
            />
          </div>
        </div>

        {/* Search Results Header */}
        {hasSearched && searchResults && (
          <div className="mb-8">
            <div className="bg-white rounded-xl p-6 shadow-lg border-l-4 border-blue-500 transform hover:scale-105 transition-all duration-300">
              <h2 className="text-xl font-bold text-gray-900 mb-2">
                🎯 Found {searchResults.total_results} products for "{searchResults.query}"
              </h2>
              <p className="text-sm text-gray-600">
                Results ranked by similarity • Powered by semantic search
              </p>
            </div>
          </div>
        )}

        {/* Products Grid with 3D Animation */}
        {displayProducts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {displayProducts.map((product, index) => (
              <div
                key={product.id}
                className="transform transition-all duration-500"
                style={{
                  animationDelay: `${index * 100}ms`,
                  animation: 'fadeInUp 0.6s ease-out forwards'
                }}
              >
                <ProductCard 
                  product={product} 
                  showSimilarityScore={hasSearched && !!searchResults}
                />
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            {isLoading ? (
              <div className="flex flex-col items-center justify-center">
                <div className="relative">
                  <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600"></div>
                  <div className="absolute inset-0 animate-ping rounded-full h-16 w-16 border-b-4 border-blue-300 opacity-30"></div>
                </div>
                <span className="mt-4 text-lg text-gray-600 font-medium">🤖 Vincent is searching...</span>
                <span className="text-sm text-gray-500">Using semantic understanding</span>
              </div>
            ) : hasSearched ? (
              <div className="text-gray-500">
                <div className="text-6xl mb-4">🔍</div>
                <p className="text-xl mb-2">No products found</p>
                <p className="text-sm">Try a different search term</p>
              </div>
            ) : (
              <div className="text-gray-500">
                <div className="text-6xl mb-4 animate-bounce">📦</div>
                <p className="text-xl mb-2">Loading products...</p>
              </div>
            )}
          </div>
        )}
      </div>

      {/* CSS for custom 3D animations */}
      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px) rotateX(10deg);
          }
          to {
            opacity: 1;
            transform: translateY(0) rotateX(0deg);
          }
        }
        
        @keyframes float {
          0%, 100% {
            transform: translateY(0px) rotate(0deg) scale(1);
          }
          33% {
            transform: translateY(-20px) rotate(120deg) scale(1.1);
          }
          66% {
            transform: translateY(10px) rotate(240deg) scale(0.9);
          }
        }
        
        @keyframes float-delayed {
          0%, 100% {
            transform: translateY(0px) rotate(0deg) scale(1);
          }
          50% {
            transform: translateY(-30px) rotate(180deg) scale(1.2);
          }
        }
        
        @keyframes float-slow {
          0%, 100% {
            transform: translateY(0px) rotateX(0deg);
          }
          50% {
            transform: translateY(-15px) rotateX(15deg);
          }
        }
        
        @keyframes spin-slow {
          from {
            transform: rotate(0deg) rotateY(0deg);
          }
          to {
            transform: rotate(360deg) rotateY(360deg);
          }
        }
        
        .animate-float {
          animation: float 6s ease-in-out infinite;
        }
        
        .animate-float-delayed {
          animation: float-delayed 8s ease-in-out infinite;
          animation-delay: 2s;
        }
        
        .animate-float-slow {
          animation: float-slow 10s ease-in-out infinite;
          animation-delay: 4s;
        }
        
        .animate-spin-slow {
          animation: spin-slow 20s linear infinite;
        }
      `}</style>
    </div>
  );
}