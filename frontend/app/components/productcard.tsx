'use client';

import { Star, Heart, ShoppingCart as CartIcon } from 'lucide-react';
import { useState } from 'react';
import { useCartStore } from '../store/cart';

// Define the Product interface directly in this file
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

interface ProductCardProps {
  product: Product;
  showSimilarityScore?: boolean;
}

export default function ProductCard({ product, showSimilarityScore = false }: ProductCardProps) {
  const [isHovered, setIsHovered] = useState(false);
  const [isAdding, setIsAdding] = useState(false);
  const { addItem } = useCartStore();

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const getSimilarityColor = (score: number) => {
    if (score >= 0.7) return 'text-green-600 bg-green-100';
    if (score >= 0.5) return 'text-yellow-600 bg-yellow-100';
    return 'text-gray-600 bg-gray-100';
  };

  const handleAddToCart = async () => {
    setIsAdding(true);
    addItem(product);
    
    // Animation feedback
    setTimeout(() => setIsAdding(false), 1000);
  };

  return (
    <div
      className={`bg-white rounded-xl shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden group cursor-pointer transform h-[520px] flex flex-col ${
        isHovered 
          ? 'scale-105 -translate-y-2 rotate-1' 
          : 'scale-100 translate-y-0 rotate-0'
      } ${isAdding ? 'animate-pulse scale-110' : ''}`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        transformStyle: 'preserve-3d',
        backfaceVisibility: 'hidden',
        perspective: '1000px',
        boxShadow: isHovered 
          ? '0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 20px 40px rgba(59, 130, 246, 0.15)'
          : '0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
      }}
    >
      {/* Image - Fixed height */}
      <div className="relative h-48 flex-shrink-0">
        <img
          src={product.image_url}
          alt={product.name}
          className={`w-full h-full object-cover transition-all duration-700 ${
            isHovered ? 'scale-110 rotate-2' : 'scale-100 rotate-0'
          }`}
        />
        
        {/* Overlay with gradient */}
        <div className={`absolute inset-0 bg-gradient-to-t from-black/20 to-transparent transition-opacity duration-300 ${
          isHovered ? 'opacity-100' : 'opacity-0'
        }`} />
        
        {/* Heart Button */}
        <button className={`absolute top-3 right-3 p-2 rounded-full bg-white/90 hover:bg-white transition-all duration-300 transform ${
          isHovered ? 'scale-110 translate-x-0' : 'scale-100 translate-x-2 opacity-0'
        }`}>
          <Heart className="h-4 w-4 text-gray-600 hover:text-red-500 transition-colors" />
        </button>
        
        {/* AI Similarity Score */}
        {showSimilarityScore && product.similarity_score && (
          <div className={`absolute top-3 left-3 px-3 py-1 rounded-full text-xs font-bold transition-all duration-500 transform ${
            isHovered ? 'scale-110 -rotate-3' : 'scale-100 rotate-0'
          } ${getSimilarityColor(product.similarity_score)}`}>
            🎯 {Math.round(product.similarity_score * 100)}% match
          </div>
        )}

        {/* Quick Add Button (appears on hover) */}
        <button
          onClick={handleAddToCart}
          className={`absolute bottom-3 right-3 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full transition-all duration-300 transform ${
            isHovered ? 'scale-100 translate-y-0 opacity-100' : 'scale-0 translate-y-4 opacity-0'
          } ${isAdding ? 'bg-green-600 scale-125' : ''}`}
        >
          <CartIcon className="h-4 w-4" />
        </button>
      </div>

      {/* Content */}
      <div className="p-5 flex-1 flex flex-col">
        {/* Brand & Category */}
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-bold text-blue-600 uppercase tracking-wide">{product.brand}</span>
          <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
            {product.category}
          </span>
        </div>

        {/* Title - Fixed height with strict line clamp */}
        <h3 className="font-bold text-gray-900 mb-3 leading-tight hover:text-blue-600 transition-colors h-12 flex items-start">
          <span className="line-clamp-2 text-sm">
            {product.name}
          </span>
        </h3>

        {/* Description - Fixed height with strict line clamp */}
        <div className="h-16 mb-4">
          <p className="text-sm text-gray-600 leading-relaxed line-clamp-3">
            {product.description.length > 100 
              ? `${product.description.substring(0, 100)}...` 
              : product.description
            }
          </p>
        </div>

        {/* Bottom section - Fixed space allocation */}
        <div className="flex-1 flex flex-col justify-end">
          {/* Rating - Fixed height */}
          <div className="flex items-center mb-3 h-6">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`h-3 w-3 transition-colors duration-200 ${
                    i < Math.floor(product.rating)
                      ? 'text-yellow-400 fill-current'
                      : 'text-gray-300'
                  }`}
                />
              ))}
            </div>
            <span className="ml-2 text-xs text-gray-600 font-medium truncate">
              {product.rating} ({product.review_count.toLocaleString()})
            </span>
          </div>

          {/* Price & Action - Fixed height */}
          <div className="flex items-center justify-between mb-3 h-10">
            <span className="text-xl font-bold text-gray-900 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              {formatPrice(product.price)}
            </span>
            <button
              onClick={handleAddToCart}
              className={`bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white px-4 py-2 rounded-lg font-bold transition-all duration-300 transform hover:scale-105 hover:-translate-y-1 active:scale-95 shadow-lg hover:shadow-xl text-xs ${
                isAdding ? 'animate-bounce bg-green-500' : ''
              }`}
              style={{
                boxShadow: '0 10px 25px -5px rgba(59, 130, 246, 0.3)'
              }}
            >
              {isAdding ? (
                <span className="flex items-center">
                  <CartIcon className="h-3 w-3 mr-1 animate-bounce" />
                  Added!
                </span>
              ) : (
                'Add to Cart'
              )}
            </button>
          </div>

          {/* Tags - Fixed height */}
          {product.tags && product.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 h-8 overflow-hidden">
              {product.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={tag}
                  className="text-xs bg-gradient-to-r from-gray-100 to-gray-200 text-gray-700 px-2 py-1 rounded-full font-medium transition-all duration-300 hover:from-blue-100 hover:to-purple-100 hover:text-blue-700 transform hover:scale-105 truncate"
                  style={{
                    animationDelay: `${index * 100}ms`
                  }}
                >
                  {tag}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}