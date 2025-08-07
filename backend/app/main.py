from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
from app.services.products import product_service
from app.services.chat import chat_assistant

app = FastAPI(
    title="AI Shopping Assistant API",
    description="Intelligent shopping assistant with AI-powered recommendations, real product data, and chat support",
    version="2.0.0"
)

# CORS middleware - allows frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "AI Shopping Assistant API is running!",
        "version": "2.0.0",
        "features": [
            "AI-powered semantic search",
            "Real product data from multiple sources",
            "Intelligent chat assistant",
            "Product recommendations",
            "Cart management"
        ]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "total_products": len(product_service.products),
        "ai_model": "all-MiniLM-L6-v2",
        "chat_enabled": True
    }

@app.get("/api/products")
def get_products() -> List[Dict[str, Any]]:
    """Get all products"""
    return product_service.get_all_products()

@app.get("/api/products/{product_id}")
def get_product(product_id: int) -> Dict[str, Any]:
    """Get a specific product"""
    product = product_service.get_product_by_id(product_id)
    if not product:
        return {"error": "Product not found"}
    return product

@app.get("/api/refresh-products")
def refresh_products():
    """Refresh product data from external APIs"""
    try:
        product_service.refresh_products()
        return {
            "message": "Products refreshed successfully",
            "total_products": len(product_service.products),
            "status": "success"
        }
    except Exception as e:
        return {
            "error": f"Failed to refresh products: {str(e)}",
            "status": "error"
        }

@app.get("/api/search")
def search_products(
    q: str = Query(..., description="Search query"),
    limit: int = Query(8, description="Number of results"),
    category: str = Query(None, description="Filter by category"),
    min_price: float = Query(None, description="Minimum price"),
    max_price: float = Query(None, description="Maximum price"),
) -> Dict[str, Any]:
    """AI-powered semantic search"""
    
    # First do AI semantic search
    results = product_service.search_products(q, top_k=limit)
    
    # Then apply filters if provided
    if category or min_price is not None or max_price is not None:
        filtered_results = []
        for product in results:
            if category and product['category'].lower() != category.lower():
                continue
            if min_price is not None and product['price'] < min_price:
                continue
            if max_price is not None and product['price'] > max_price:
                continue
            filtered_results.append(product)
        results = filtered_results
    
    return {
        "query": q,
        "total_results": len(results),
        "products": results[:limit],
        "filters_applied": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price
        }
    }

@app.post("/api/chat")
def chat_with_assistant(message: dict) -> Dict[str, Any]:
    """Chat with AI shopping assistant"""
    user_message = message.get('message', '')
    user_id = message.get('user_id', None)
    
    if not user_message.strip():
        return {
            "error": "Message cannot be empty",
            "message": "Please enter a message to chat with me!",
            "products": [],
            "intent": "error"
        }
    
    try:
        response = chat_assistant.process_message(user_message, user_id)
        return response
    except Exception as e:
        print(f"Chat error: {e}")  # Log error for debugging
        return {
            "message": "Sorry, I'm having trouble processing your request. Please try again! 🤖",
            "products": [],
            "intent": "error",
            "error_details": str(e) if app.debug else None
        }

@app.get("/api/categories")
def get_categories() -> Dict[str, Any]:
    """Get all available product categories"""
    categories = set()
    for product in product_service.products:
        categories.add(product['category'])
    
    return {
        "categories": sorted(list(categories)),
        "total_categories": len(categories)
    }

@app.get("/api/brands")
def get_brands() -> Dict[str, Any]:
    """Get all available brands"""
    brands = set()
    for product in product_service.products:
        brands.add(product['brand'])
    
    return {
        "brands": sorted(list(brands)),
        "total_brands": len(brands)
    }

@app.get("/api/stats")
def get_stats() -> Dict[str, Any]:
    """Get platform statistics"""
    products = product_service.products
    
    # Calculate stats
    total_products = len(products)
    avg_price = sum(p['price'] for p in products) / total_products if products else 0
    price_range = {
        "min": min(p['price'] for p in products) if products else 0,
        "max": max(p['price'] for p in products) if products else 0
    }
    
    # Category distribution
    category_counts = {}
    for product in products:
        category = product['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    # Brand distribution (top 10)
    brand_counts = {}
    for product in products:
        brand = product['brand']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1
    
    top_brands = sorted(brand_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    return {
        "total_products": total_products,
        "average_price": round(avg_price, 2),
        "price_range": price_range,
        "categories": category_counts,
        "top_brands": dict(top_brands),
        "ai_features": {
            "semantic_search": True,
            "chat_assistant": True,
            "product_recommendations": True,
            "real_time_data": True
        }
    }

# Add some fun Easter egg endpoints
@app.get("/api/surprise")
def surprise_me() -> Dict[str, Any]:
    """Get a surprise product recommendation"""
    import random
    
    if not product_service.products:
        return {"message": "No products available for surprises!"}
    
    surprise_product = random.choice(product_service.products)
    
    return {
        "message": "🎉 Surprise! Here's a random product you might like:",
        "product": surprise_product,
        "why": "Sometimes the best discoveries are unexpected! ✨"
    }

@app.get("/api/deal-of-the-day")
def deal_of_the_day() -> Dict[str, Any]:
    """Get the deal of the day (lowest priced product with good rating)"""
    
    # Find products with good ratings (4.0+) sorted by price
    good_products = [p for p in product_service.products if p.get('rating', 0) >= 4.0]
    
    if not good_products:
        return {"message": "No deals available today"}
    
    # Sort by price to find the best value
    deal_product = min(good_products, key=lambda x: x['price'])
    
    return {
        "message": "💎 Today's Best Deal - Great Quality, Great Price!",
        "product": deal_product,
        "deal_score": f"{deal_product['rating']}/5 stars at just ${deal_product['price']:.2f}",
        "savings_tip": "High-rated product at an amazing price! 🔥"
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "message": "The requested endpoint doesn't exist",
        "available_endpoints": [
            "/api/products",
            "/api/search", 
            "/api/chat",
            "/api/refresh-products",
            "/api/categories",
            "/api/brands",
            "/api/stats"
        ]
    }

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": "Something went wrong on our end. Please try again!",
        "support": "If the problem persists, please check the server logs"
    }