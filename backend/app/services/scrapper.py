import requests
from bs4 import BeautifulSoup
import json
import re
import time
from typing import List, Dict, Any
import random

class ProductScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_fake_store_api(self) -> List[Dict[str, Any]]:
        """Scrape from Fake Store API - completely free and reliable"""
        try:
            response = self.session.get('https://fakestoreapi.com/products')
            if response.status_code == 200:
                products = response.json()
                
                formatted_products = []
                for i, product in enumerate(products):
                    formatted_product = {
                        "id": product['id'] + 100,  # Offset to avoid conflicts
                        "name": product['title'],
                        "description": product['description'],
                        "price": float(product['price']),
                        "currency": "USD",
                        "category": self._format_category(product['category']),
                        "brand": self._extract_brand(product['title']),
                        "image_url": product['image'],
                        "rating": float(product['rating']['rate']),
                        "review_count": int(product['rating']['count']),
                        "tags": self._generate_tags(product['title'], product['description'], product['category'])
                    }
                    formatted_products.append(formatted_product)
                
                print(f"✅ Scraped {len(formatted_products)} products from Fake Store API")
                return formatted_products
                
        except Exception as e:
            print(f"❌ Error scraping Fake Store API: {e}")
            return []
    
    def scrape_dummyjson_products(self) -> List[Dict[str, Any]]:
        """Scrape from DummyJSON - another free API with good product data"""
        try:
            response = self.session.get('https://dummyjson.com/products?limit=30')
            if response.status_code == 200:
                data = response.json()
                products = data['products']
                
                formatted_products = []
                for product in products:
                    formatted_product = {
                        "id": product['id'] + 200,  # Offset to avoid conflicts
                        "name": product['title'],
                        "description": product['description'],
                        "price": float(product['price']),
                        "currency": "USD",
                        "category": self._format_category(product['category']),
                        "brand": product.get('brand', self._extract_brand(product['title'])),
                        "image_url": product['thumbnail'],
                        "rating": float(product['rating']),
                        "review_count": random.randint(50, 5000),  # API doesn't provide this
                        "tags": self._generate_tags(product['title'], product['description'], product['category'])
                    }
                    formatted_products.append(formatted_product)
                
                print(f"✅ Scraped {len(formatted_products)} products from DummyJSON")
                return formatted_products
                
        except Exception as e:
            print(f"❌ Error scraping DummyJSON: {e}")
            return []
    
    def scrape_platzi_fake_api(self) -> List[Dict[str, Any]]:
        """Scrape from Platzi Fake Store API - more product variety"""
        try:
            response = self.session.get('https://api.escuelajs.co/api/v1/products?offset=0&limit=20')
            if response.status_code == 200:
                products = response.json()
                
                formatted_products = []
                for product in products:
                    # Skip products with invalid data
                    if not product.get('title') or not product.get('price'):
                        continue
                        
                    formatted_product = {
                        "id": product['id'] + 300,  # Offset to avoid conflicts
                        "name": product['title'],
                        "description": product.get('description', 'High-quality product with excellent features'),
                        "price": float(product['price']),
                        "currency": "USD",
                        "category": self._format_category(product.get('category', {}).get('name', 'General')),
                        "brand": self._extract_brand(product['title']),
                        "image_url": product['images'][0] if product.get('images') else 'https://via.placeholder.com/300x300/6366f1/ffffff?text=Product',
                        "rating": round(random.uniform(3.5, 4.9), 1),
                        "review_count": random.randint(100, 3000),
                        "tags": self._generate_tags(product['title'], product.get('description', ''), product.get('category', {}).get('name', ''))
                    }
                    formatted_products.append(formatted_product)
                
                print(f"✅ Scraped {len(formatted_products)} products from Platzi API")
                return formatted_products
                
        except Exception as e:
            print(f"❌ Error scraping Platzi API: {e}")
            return []
    
    def _format_category(self, category: str) -> str:
        """Format category names consistently"""
        if not category:
            return "General"
        
        category_mapping = {
            "men's clothing": "Clothing",
            "women's clothing": "Clothing", 
            "jewelery": "Jewelry",
            "electronics": "Electronics",
            "smartphones": "Electronics",
            "laptops": "Electronics",
            "home-decoration": "Home & Garden",
            "furniture": "Furniture",
            "clothes": "Clothing",
            "shoes": "Footwear",
            "miscellaneous": "General"
        }
        
        category_lower = category.lower()
        return category_mapping.get(category_lower, category.title())
    
    def _extract_brand(self, title: str) -> str:
        """Extract or generate brand from product title"""
        # Common brand patterns
        brands = {
            'apple': 'Apple', 'samsung': 'Samsung', 'nike': 'Nike', 'adidas': 'Adidas',
            'sony': 'Sony', 'hp': 'HP', 'dell': 'Dell', 'lenovo': 'Lenovo',
            'asus': 'ASUS', 'acer': 'Acer', 'canon': 'Canon', 'nikon': 'Nikon',
            'bose': 'Bose', 'jbl': 'JBL', 'beats': 'Beats', 'sennheiser': 'Sennheiser'
        }
        
        title_lower = title.lower()
        for brand_key, brand_name in brands.items():
            if brand_key in title_lower:
                return brand_name
        
        # Generate brand from first word if no known brand found
        first_word = title.split()[0] if title.split() else "Generic"
        return first_word.title()
    
    def _generate_tags(self, title: str, description: str, category: str) -> List[str]:
        """Generate relevant tags from product information"""
        text = f"{title} {description} {category}".lower()
        
        tag_keywords = {
            'wireless': ['wireless', 'bluetooth', 'cordless'],
            'portable': ['portable', 'compact', 'travel', 'lightweight'],
            'premium': ['premium', 'luxury', 'high-end', 'professional'],
            'budget': ['cheap', 'affordable', 'budget', 'value'],
            'gaming': ['gaming', 'gamer', 'esports', 'rgb'],
            'fitness': ['fitness', 'sport', 'workout', 'exercise', 'running'],
            'smart': ['smart', 'ai', 'intelligent', 'connected'],
            'waterproof': ['waterproof', 'water-resistant', 'splash'],
            'fast': ['fast', 'quick', 'speed', 'rapid'],
            'comfortable': ['comfortable', 'soft', 'cozy', 'ergonomic']
        }
        
        tags = []
        for tag, keywords in tag_keywords.items():
            if any(keyword in text for keyword in keywords):
                tags.append(tag)
        
        # Add category as tag
        if category and category.lower() not in [tag.lower() for tag in tags]:
            tags.append(category.lower().replace(' & ', '-').replace(' ', '-'))
        
        return tags[:5]  # Limit to 5 tags
    
    def get_all_real_products(self) -> List[Dict[str, Any]]:
        """Get products from multiple free APIs"""
        all_products = []
        
        print("🌐 Fetching real product data from multiple sources...")
        
        # Scrape from multiple free APIs
        fake_store_products = self.scrape_fake_store_api()
        dummyjson_products = self.scrape_dummyjson_products()
        platzi_products = self.scrape_platzi_fake_api()
        
        # Combine all products
        all_products.extend(fake_store_products)
        all_products.extend(dummyjson_products)
        all_products.extend(platzi_products)
        
        # Remove duplicates based on name similarity
        unique_products = self._remove_duplicates(all_products)
        
        print(f"🎉 Total unique products loaded: {len(unique_products)}")
        return unique_products
    
    def _remove_duplicates(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate products based on name similarity"""
        unique_products = []
        seen_names = set()
        
        for product in products:
            # Create a normalized name for comparison
            normalized_name = re.sub(r'[^a-zA-Z0-9\s]', '', product['name'].lower())
            normalized_name = ' '.join(normalized_name.split())
            
            if normalized_name not in seen_names:
                seen_names.add(normalized_name)
                unique_products.append(product)
        
        return unique_products

# Global instance
product_scraper = ProductScraper()