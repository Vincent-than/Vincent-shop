'use client';

import { useState } from 'react';
import { ShoppingCart, X, Plus, Minus, Trash2 } from 'lucide-react';
import { useCartStore } from '../store/cart';

export default function Cart() {
  const {
    items,
    totalItems,
    isOpen,
    toggleCart,
    removeItem,
    updateQuantity,
    clearCart,
    getTotalPrice
  } = useCartStore();

  const [isAnimating, setIsAnimating] = useState(false);

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(price);
  };

  const handleAddToCart = () => {
    setIsAnimating(true);
    setTimeout(() => setIsAnimating(false), 600);
  };

  return (
    <>
      {/* Cart Button - 3D Floating */}
      <button
        onClick={toggleCart}
        className={`fixed top-4 right-4 z-50 bg-gradient-to-r from-blue-600 to-blue-700 text-white p-4 rounded-full shadow-2xl hover:shadow-3xl transform transition-all duration-300 hover:scale-110 hover:-translate-y-1 ${
          isAnimating ? 'animate-bounce scale-125' : ''
        } group`}
        style={{
          background: 'linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #60a5fa 100%)',
          boxShadow: '0 20px 40px rgba(59, 130, 246, 0.3), 0 0 20px rgba(59, 130, 246, 0.2)'
        }}
      >
        <div className="relative">
          <ShoppingCart className="h-6 w-6 group-hover:animate-pulse" />
          {totalItems > 0 && (
            <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-bold animate-pulse">
              {totalItems}
            </span>
          )}
        </div>
      </button>

      {/* Cart Sidebar - 3D Slide In - No backdrop */}
      <div
        className={`fixed inset-y-0 right-0 z-40 w-96 bg-white shadow-2xl transform transition-all duration-500 ease-in-out ${
          isOpen 
            ? 'translate-x-0 scale-100 opacity-100' 
            : 'translate-x-full scale-95 opacity-0'
        }`}
        style={{
          transform: isOpen 
            ? 'translateX(0) rotateY(0deg) scale(1)' 
            : 'translateX(100%) rotateY(-10deg) scale(0.95)',
          transformStyle: 'preserve-3d',
          backfaceVisibility: 'hidden'
        }}
      >
        {/* Cart Header */}
        <div className="p-6 border-b bg-gradient-to-r from-blue-600 to-purple-600 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-bold">Shopping Cart</h2>
              <p className="text-blue-100">{totalItems} items</p>
            </div>
            <button
              onClick={toggleCart}
              className="p-2 hover:bg-white/20 rounded-full transition-colors"
            >
              <X className="h-6 w-6" />
            </button>
          </div>
        </div>

        {/* Cart Items */}
        <div className="flex-1 overflow-y-auto p-4">
          {items.length === 0 ? (
            <div className="text-center py-12">
              <ShoppingCart className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-lg">Your cart is empty</p>
              <p className="text-gray-400 text-sm">Add some products to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {items.map((item, index) => (
                <div
                  key={item.id}
                  className="bg-gray-50 rounded-lg p-4 hover:shadow-md transition-all duration-300 transform hover:scale-105"
                  style={{
                    animationDelay: `${index * 100}ms`,
                    animation: 'slideInFromRight 0.5s ease-out forwards'
                  }}
                >
                  <div className="flex items-center space-x-4">
                    {/* Product Image */}
                    <img
                      src={item.image_url}
                      alt={item.name}
                      className="w-16 h-16 object-cover rounded-lg shadow-md"
                    />
                    
                    {/* Product Info */}
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 text-sm">{item.name}</h3>
                      <p className="text-gray-600 text-xs">{item.brand}</p>
                      <p className="font-bold text-blue-600">{formatPrice(item.price)}</p>
                    </div>
                    
                    {/* Quantity Controls */}
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity - 1)}
                        className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                      >
                        <Minus className="h-4 w-4" />
                      </button>
                      <span className="w-8 text-center font-medium">{item.quantity}</span>
                      <button
                        onClick={() => updateQuantity(item.id, item.quantity + 1)}
                        className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                      >
                        <Plus className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => removeItem(item.id)}
                        className="p-1 hover:bg-red-100 text-red-500 rounded-full transition-colors ml-2"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Cart Footer */}
        {items.length > 0 && (
          <div className="border-t p-6 bg-gray-50">
            <div className="flex justify-between items-center mb-4">
              <span className="text-lg font-semibold text-gray-900">Total:</span>
              <span className="text-2xl font-bold text-blue-600">
                {formatPrice(getTotalPrice())}
              </span>
            </div>
            
            <div className="space-y-3">
              <button className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-4 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl">
                Checkout ({totalItems} items)
              </button>
              
              <button
                onClick={clearCart}
                className="w-full bg-gray-200 text-gray-700 py-2 px-4 rounded-lg font-medium hover:bg-gray-300 transition-colors"
              >
                Clear Cart
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Optional: Very light backdrop that still shows background */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-transparent z-30"
          onClick={toggleCart}
        />
      )}

      {/* CSS for animations */}
      <style jsx>{`
        @keyframes slideInFromRight {
          from {
            transform: translateX(100%) rotateY(90deg);
            opacity: 0;
          }
          to {
            transform: translateX(0) rotateY(0deg);
            opacity: 1;
          }
        }
        
        .shadow-3xl {
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25), 0 0 30px rgba(59, 130, 246, 0.3);
        }
      `}</style>
    </>
  );
}