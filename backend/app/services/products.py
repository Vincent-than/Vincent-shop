from typing import List, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Sample product data - in a real app this would come from a database
SAMPLE_PRODUCTS = [
    # Original products
    {
        "id": 1,
        "name": "Nike Air Max 270 Running Shoes",
        "description": "Comfortable lightweight running shoes with air cushioning, perfect for daily workouts and casual wear",
        "price": 89.99,
        "currency": "USD",
        "category": "Footwear",
        "brand": "Nike",
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&crop=center",
        "rating": 4.5,
        "review_count": 1250,
        "tags": ["running", "comfortable", "athletic", "casual", "breathable"]
    },
    {
        "id": 2,
        "name": "Apple MacBook Air M2",
        "description": "Powerful lightweight laptop with M2 chip, perfect for students and professionals. 13-inch display, 8GB RAM",
        "price": 1199.00,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Apple",
        "image_url": "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=300&h=300&fit=crop&crop=center",
        "rating": 4.8,
        "review_count": 890,
        "tags": ["laptop", "student", "professional", "portable", "fast"]
    },
    {
        "id": 3,
        "name": "Sony WH-1000XM5 Wireless Headphones",
        "description": "Premium noise-canceling headphones with excellent bass and 30-hour battery life",
        "price": 279.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Sony",
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop&crop=center",
        "rating": 4.7,
        "review_count": 2100,
        "tags": ["wireless", "noise-canceling", "bass", "premium", "long-battery"]
    },
    {
        "id": 4,
        "name": "Levi's 501 Original Jeans",
        "description": "Classic straight-fit denim jeans, timeless style and durable construction",
        "price": 59.99,
        "currency": "USD",
        "category": "Clothing",
        "brand": "Levi's",
        "image_url": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=300&h=300&fit=crop&crop=center",
        "rating": 4.3,
        "review_count": 750,
        "tags": ["jeans", "classic", "denim", "durable", "casual"]
    },
    {
        "id": 5,
        "name": "Instant Pot Duo 7-in-1 Pressure Cooker",
        "description": "Multi-functional kitchen appliance: pressure cooker, slow cooker, rice cooker, steamer, and more",
        "price": 79.99,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "Instant Pot",
        "image_url": "./instantpot.jpg",
        "rating": 4.6,
        "review_count": 5600,
        "tags": ["kitchen", "cooking", "multi-functional", "pressure-cooker", "convenient"]
    },
    {
        "id": 6,
        "name": "Adidas Ultraboost 22 Running Shoes",
        "description": "High-performance running shoes with responsive Boost midsole and breathable upper",
        "price": 95.00,
        "currency": "USD",
        "category": "Footwear",
        "brand": "Adidas",
        "image_url": "/adidas.jpg",
        "rating": 4.4,
        "review_count": 980,
        "tags": ["running", "performance", "boost", "breathable", "athletic"]
    },
    {
        "id": 7,
        "name": "ASUS ZenBook 14 Laptop",
        "description": "Affordable student laptop with Intel i5 processor, 8GB RAM, perfect for coding and studying",
        "price": 649.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "ASUS",
        "image_url": "/asus.jpg",
        "rating": 4.2,
        "review_count": 445,
        "tags": ["laptop", "budget", "student", "coding", "affordable"]
    },
    {
        "id": 8,
        "name": "JBL Charge 5 Portable Speaker",
        "description": "Waterproof Bluetooth speaker with powerful bass and 20-hour battery life",
        "price": 129.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "JBL",
        "image_url": "/jbl.jpg",
        "rating": 4.5,
        "review_count": 1800,
        "tags": ["speaker", "bluetooth", "waterproof", "bass", "portable"]
    },
    
    {
        "id": 9,
        "name": "Samsung Galaxy S24 Ultra",
        "description": "Premium smartphone with 200MP camera, S Pen, and all-day battery life",
        "price": 1299.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Samsung",
        "image_url": "/samsungs24.jpg",
        "rating": 4.6,
        "review_count": 3200,
        "tags": ["smartphone", "camera", "premium", "s-pen", "android"]
    },
    {
        "id": 10,
        "name": "Nintendo Switch OLED",
        "description": "Portable gaming console with vibrant OLED screen and versatile gameplay",
        "price": 349.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Nintendo",
        "image_url": "/switch.jpg",
        "rating": 4.8,
        "review_count": 4500,
        "tags": ["gaming", "portable", "console", "oled", "family-friendly"]
    },
    {
        "id": 11,
        "name": "Dyson V15 Detect Vacuum",
        "description": "Powerful cordless vacuum with laser dust detection and advanced filtration",
        "price": 549.99,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "Dyson",
        "image_url": "/dyson.jpg",
        "rating": 4.7,
        "review_count": 2800,
        "tags": ["vacuum", "cordless", "powerful", "laser-detection", "filtration"]
    },
    {
        "id": 12,
        "name": "Patagonia Better Sweater Fleece",
        "description": "Cozy fleece jacket made from recycled polyester, perfect for outdoor adventures",
        "price": 119.00,
        "currency": "USD",
        "category": "Clothing",
        "brand": "Patagonia",
        "image_url": "/patagonia.jpg",
        "rating": 4.6,
        "review_count": 1200,
        "tags": ["fleece", "outdoor", "sustainable", "warm", "hiking"]
    },
    {
        "id": 13,
        "name": "KitchenAid Stand Mixer",
        "description": "Professional-grade stand mixer for baking enthusiasts, multiple attachments available",
        "price": 379.99,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "KitchenAid",
        "image_url": "/kitchen.jpg",
        "rating": 4.8,
        "review_count": 3400,
        "tags": ["baking", "mixer", "professional", "kitchen", "durable"]
    },
    {
        "id": 14,
        "name": "Allbirds Tree Runners",
        "description": "Sustainable sneakers made from eucalyptus tree fiber, incredibly comfortable for all-day wear",
        "price": 98.00,
        "currency": "USD",
        "category": "Footwear",
        "brand": "Allbirds",
        "image_url": "/allbirds.jpg",
        "rating": 4.3,
        "review_count": 1850,
        "tags": ["sustainable", "comfortable", "eco-friendly", "casual", "lightweight"]
    },
    {
        "id": 15,
        "name": "iPad Pro 12.9 inch",
        "description": "Professional tablet with M2 chip, perfect for digital art, note-taking, and productivity",
        "price": 1099.00,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Apple",
        "image_url": "/ipad.jpg",
        "rating": 4.7,
        "review_count": 1500,
        "tags": ["tablet", "digital-art", "productivity", "apple-pencil", "professional"]
    },
    {
        "id": 16,
        "name": "Yeti Rambler Tumbler",
        "description": "Insulated stainless steel tumbler that keeps drinks hot or cold for hours",
        "price": 35.00,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "Yeti",
        "image_url": "/yeti.jpg",
        "rating": 4.8,
        "review_count": 2200,
        "tags": ["tumbler", "insulated", "durable", "hot", "cold"]
    },
    {
        "id": 17,
        "name": "Canon EOS R5 Camera",
        "description": "Professional mirrorless camera with 45MP sensor and 8K video recording",
        "price": 3899.00,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Canon",
        "image_url": "/canon.jpg",
        "rating": 4.9,
        "review_count": 650,
        "tags": ["camera", "professional", "mirrorless", "8k-video", "photography"]
    },
    {
        "id": 18,
        "name": "Lululemon Align Leggings",
        "description": "Buttery-soft yoga leggings with four-way stretch, perfect for workouts and lounging",
        "price": 128.00,
        "currency": "USD",
        "category": "Clothing",
        "brand": "Lululemon",
        "image_url": "/lululemon.jpg",
        "rating": 4.5,
        "review_count": 3800,
        "tags": ["leggings", "yoga", "comfortable", "stretch", "activewear"]
    },
    {
        "id": 19,
        "name": "Tesla Model Y Performance Wheels",
        "description": "21-inch Überturbine wheels designed for Tesla Model Y Performance",
        "price": 4500.00,
        "currency": "USD",
        "category": "Automotive",
        "brand": "Tesla",
        "image_url": "/tesla.jpg",
        "rating": 4.4,
        "review_count": 180,
        "tags": ["tesla", "wheels", "performance", "electric-car", "premium"]
    },
    {
        "id": 20,
        "name": "Bose QuietComfort Earbuds",
        "description": "True wireless earbuds with world-class noise cancellation and premium sound",
        "price": 279.00,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Bose",
        "image_url": "/bose.jpg",
        "rating": 4.4,
        "review_count": 2400,
        "tags": ["earbuds", "wireless", "noise-canceling", "premium", "compact"]
    },
    {
        "id": 21,
        "name": "Vitamix A3500 Blender",
        "description": "Professional-grade blender with smart technology and variable speed control",
        "price": 549.99,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "Vitamix",
        "image_url": "/vitamix.jpg",
        "rating": 4.7,
        "review_count": 1800,
        "tags": ["blender", "professional", "smoothies", "powerful", "smart"]
    },
    {
        "id": 22,
        "name": "North Face Puffer Jacket",
        "description": "Warm down-filled winter jacket with water-resistant coating",
        "price": 249.99,
        "currency": "USD",
        "category": "Clothing",
        "brand": "The North Face",
        "image_url": "/northface.jpg",
        "rating": 4.6,
        "review_count": 1600,
        "tags": ["jacket", "winter", "warm", "down-filled", "outdoor"]
    },
    {
        "id": 23,
        "name": "Fitbit Charge 5",
        "description": "Advanced fitness tracker with GPS, stress management, and 7-day battery life",
        "price": 149.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Fitbit",
        "image_url": "/fitbit.jpg",
        "rating": 4.2,
        "review_count": 2900,
        "tags": ["fitness-tracker", "gps", "health", "battery", "stress-management"]
    },
    {
        "id": 24,
        "name": "Cuisinart Coffee Maker",
        "description": "Programmable 12-cup coffee maker with auto shut-off and brew strength control",
        "price": 89.95,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "Cuisinart",
        "image_url": "/cuisinart.jpg",
        "rating": 4.4,
        "review_count": 4200,
        "tags": ["coffee", "programmable", "automatic", "morning", "kitchen"]
    },
    {
        "id": 25,
        "name": "Ray-Ban Aviator Sunglasses",
        "description": "Classic aviator sunglasses with UV protection and timeless style",
        "price": 154.00,
        "currency": "USD",
        "category": "Accessories",
        "brand": "Ray-Ban",
        "image_url": "/rayban.jpg",
        "rating": 4.7,
        "review_count": 8900,
        "tags": ["sunglasses", "classic", "aviator", "uv-protection", "style"]
    },
    {
        "id": 26,
        "name": "Herman Miller Aeron Chair",
        "description": "Ergonomic office chair with breathable mesh and lumbar support, perfect for long work sessions",
        "price": 1395.00,
        "currency": "USD",
        "category": "Furniture",
        "brand": "Herman Miller",
        "image_url": "/herman.jpg",
        "rating": 4.8,
        "review_count": 1200,
        "tags": ["office-chair", "ergonomic", "comfortable", "work", "lumbar-support"]
    },
    {
        "id": 27,
        "name": "Hydro Flask Water Bottle",
        "description": "Insulated stainless steel water bottle that keeps drinks cold for 24 hours",
        "price": 44.95,
        "currency": "USD",
        "category": "Sports & Outdoors",
        "brand": "Hydro Flask",
        "image_url": "/yeti.jpg",
        "rating": 4.6,
        "review_count": 5400,
        "tags": ["water-bottle", "insulated", "cold", "outdoor", "hydration"]
    },
    {
        "id": 28,
        "name": "Roomba i7+ Robot Vacuum",
        "description": "Smart robot vacuum with automatic dirt disposal and advanced mapping",
        "price": 599.99,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "iRobot",
        "image_url": "./roomba.jpg",
        "rating": 4.3,
        "review_count": 3100,
        "tags": ["robot-vacuum", "smart", "automatic", "mapping", "cleaning"]
    },
    {
        "id": 29,
        "name": "Peloton Bike+",
        "description": "Interactive exercise bike with live and on-demand classes, rotating touchscreen",
        "price": 2495.00,
        "currency": "USD",
        "category": "Sports & Outdoors",
        "brand": "Peloton",
        "image_url": "./peloton.jpg",
        "rating": 4.4,
        "review_count": 2200,
        "tags": ["exercise-bike", "fitness", "interactive", "classes", "cardio"]
    },
    {
        "id": 30,
        "name": "AirPods Pro 2nd Gen",
        "description": "Apple's premium wireless earbuds with adaptive transparency and spatial audio",
        "price": 249.00,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Apple",
        "image_url": "/airpods.jpg",
        "rating": 4.6,
        "review_count": 8900,
        "tags": ["earbuds", "wireless", "apple", "spatial-audio", "transparency"]
    },
    {
        "id": 31,
        "name": "Le Creuset Dutch Oven",
        "description": "Enameled cast iron Dutch oven perfect for braising, roasting, and bread baking",
        "price": 329.95,
        "currency": "USD",
        "category": "Home & Kitchen",
        "brand": "Le Creuset",
        "image_url": "/dutch.jpg",
        "rating": 4.9,
        "review_count": 1100,
        "tags": ["dutch-oven", "cast-iron", "baking", "cooking", "premium"]
    },
    {
        "id": 32,
        "name": "Secretlab Omega Gaming Chair",
        "description": "Ergonomic gaming chair with lumbar support and premium materials for long gaming sessions",
        "price": 519.00,
        "currency": "USD",
        "category": "Furniture",
        "brand": "Secretlab",
        "image_url": "./secretlab.jpg",
        "rating": 4.5,
        "review_count": 3600,
        "tags": ["gaming-chair", "ergonomic", "lumbar-support", "gaming", "comfortable"]
    },
    {
        "id": 33,
        "name": "Kindle Oasis E-reader",
        "description": "Premium e-reader with 7-inch display, adjustable warm light, and waterproof design",
        "price": 279.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "Amazon",
        "image_url": "./kindle.jpg",
        "rating": 4.3,
        "review_count": 2800,
        "tags": ["e-reader", "books", "waterproof", "reading", "warm-light"]
    },
    {
        "id": 34,
        "name": "Crocs Classic Clogs",
        "description": "Comfortable foam clogs with ventilation holes, perfect for casual wear and gardening",
        "price": 44.99,
        "currency": "USD",
        "category": "Footwear",
        "brand": "Crocs",
        "image_url": "./crocs.jpg",
        "rating": 4.1,
        "review_count": 12000,
        "tags": ["clogs", "comfortable", "casual", "easy-to-clean", "ventilated"]
    },
    {
        "id": 35,
        "name": "GoPro HERO12 Black",
        "description": "Action camera with 5.3K video, waterproof design, and advanced stabilization",
        "price": 399.99,
        "currency": "USD",
        "category": "Electronics",
        "brand": "GoPro",
        "image_url": "/gopro.jpg",
        "rating": 4.6,
        "review_count": 1900,
        "tags": ["action-camera", "waterproof", "5k-video", "adventure", "stabilization"]
    }
]

class ProductSearchService:
    def __init__(self):
        # Initialize the sentence transformer model for text embeddings
        print("Loading AI model for semantic search...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Precompute embeddings for all products
        self.products = SAMPLE_PRODUCTS
        self.product_embeddings = self._compute_product_embeddings()
        print(f"AI search ready! Loaded {len(self.products)} products.")
    
    def _compute_product_embeddings(self):
        """Precompute embeddings for all products"""
        product_texts = []
        for product in self.products:
            # Combine name, description, and tags for better search
            text = f"{product['name']} {product['description']} {' '.join(product['tags'])}"
            product_texts.append(text)
        
        # Generate embeddings
        embeddings = self.model.encode(product_texts)
        return embeddings
    
    def search_products(self, query: str, top_k: int = 8, min_score: float = 0.1) -> List[Dict[str, Any]]:
        """
        Semantic search using AI embeddings
        
        Args:
            query: User search query (e.g., "comfortable running shoes")
            top_k: Number of results to return
            min_score: Minimum similarity score (0-1)
        
        Returns:
            List of products with similarity scores
        """
        if not query.strip():
            return self.products[:top_k]
        
        # Encode the search query
        query_embedding = self.model.encode([query])
        
        # Calculate similarity scores
        similarities = cosine_similarity(query_embedding, self.product_embeddings)[0]
        
        # Get top results
        product_scores = list(zip(self.products, similarities))
        
        # Filter by minimum score and sort by similarity
        filtered_results = [
            (product, float(score)) for product, score in product_scores 
            if score >= min_score
        ]
        
        # Sort by similarity score (highest first)
        filtered_results.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k results with scores
        results = []
        for product, score in filtered_results[:top_k]:
            result = product.copy()
            result['similarity_score'] = score
            results.append(result)
        
        return results
    
    def get_all_products(self) -> List[Dict[str, Any]]:
        """Get all products"""
        return self.products
    
    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """Get a specific product by ID"""
        for product in self.products:
            if product['id'] == product_id:
                return product
        return None
    
    def filter_products(self, category: str = None, min_price: float = None, max_price: float = None) -> List[Dict[str, Any]]:
        """Filter products by category and price range"""
        filtered = self.products
        
        if category:
            filtered = [p for p in filtered if p['category'].lower() == category.lower()]
        
        if min_price is not None:
            filtered = [p for p in filtered if p['price'] >= min_price]
        
        if max_price is not None:
            filtered = [p for p in filtered if p['price'] <= max_price]
        
        return filtered

# Global instance - in a real app you'd use dependency injection
product_service = ProductSearchService()