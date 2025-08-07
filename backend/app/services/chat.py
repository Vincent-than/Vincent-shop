from typing import List, Dict, Any, Optional
import json
import re
from app.services.products import product_service

class ShoppingChatAssistant:
    def __init__(self):
        self.conversation_history = []
        
    def process_message(self, message: str, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Process user message and return AI response with product recommendations"""
        
        # Analyze the message to understand intent
        intent = self._analyze_intent(message)
        
        # Generate response based on intent
        if intent['type'] == 'product_search':
            return self._handle_product_search(message, intent)
        elif intent['type'] == 'comparison':
            return self._handle_comparison(message, intent)
        elif intent['type'] == 'recommendation':
            return self._handle_recommendation(message, intent)
        elif intent['type'] == 'question':
            return self._handle_question(message, intent)
        else:
            return self._handle_general(message)
    
    def _analyze_intent(self, message: str) -> Dict[str, Any]:
        """Analyze user message to understand intent"""
        message_lower = message.lower()
        
        # Search for products patterns
        search_patterns = [
            r'find.*(?:headphones?|earbuds?|speakers?)',
            r'(?:show|find|search).*(?:laptop|computer|phone)',
            r'(?:looking for|need|want).*(?:shoes?|sneakers?|boots?)',
            r'(?:find|show).*(?:under|below|less than).*\$?\d+',
            r'(?:budget|cheap|affordable).*(?:laptop|phone|headphones?)'
        ]
        
        # Comparison patterns
        comparison_patterns = [
            r'(?:compare|vs|versus|better|difference)',
            r'(?:which is better|what.*difference)',
            r'(?:should i get|choose between)'
        ]
        
        # Recommendation patterns
        recommendation_patterns = [
            r'(?:recommend|suggest|advice)',
            r'(?:what should i|help me choose)',
            r'(?:best.*for|good.*for)'
        ]
        
        # Question patterns
        question_patterns = [
            r'(?:how much|what.*price|cost)',
            r'(?:is.*good|worth it|reliable)',
            r'(?:what.*features|specs|specifications)'
        ]
        
        # Determine intent
        if any(re.search(pattern, message_lower) for pattern in search_patterns):
            return {'type': 'product_search', 'query': message}
        elif any(re.search(pattern, message_lower) for pattern in comparison_patterns):
            return {'type': 'comparison', 'query': message}
        elif any(re.search(pattern, message_lower) for pattern in recommendation_patterns):
            return {'type': 'recommendation', 'query': message}
        elif any(re.search(pattern, message_lower) for pattern in question_patterns):
            return {'type': 'question', 'query': message}
        else:
            return {'type': 'general', 'query': message}
    
    def _handle_product_search(self, message: str, intent: Dict) -> Dict[str, Any]:
        """Handle product search requests"""
        
        # Extract search parameters
        search_query = self._extract_search_terms(message)
        budget = self._extract_budget(message)
        category = self._extract_category(message)
        
        # Search products
        products = product_service.search_products(search_query, top_k=6)
        
        # Apply budget filter if found
        if budget:
            products = [p for p in products if p['price'] <= budget]
        
        # Generate natural response
        if products:
            response_text = self._generate_search_response(search_query, products, budget)
        else:
            response_text = f"I couldn't find any products matching '{search_query}'. Try a different search term or check out our popular items!"
        
        return {
            'message': response_text,
            'products': products[:4],  # Return top 4 for chat
            'intent': 'product_search',
            'search_query': search_query,
            'budget': budget
        }
    
    def _handle_comparison(self, message: str, intent: Dict) -> Dict[str, Any]:
        """Handle product comparison requests"""
        
        # Extract product names or categories to compare
        search_terms = self._extract_search_terms(message)
        products = product_service.search_products(search_terms, top_k=4)
        
        if len(products) >= 2:
            response_text = f"Here are some great options to compare:\n\n"
            for i, product in enumerate(products[:3]):
                response_text += f"{i+1}. **{product['name']}** - ${product['price']:.2f}\n"
                response_text += f"   Rating: {product['rating']}/5 ⭐ | {product['brand']}\n\n"
            
            response_text += "Would you like me to highlight the key differences between any of these?"
        else:
            response_text = "I need more specific product names to make a good comparison. What products are you thinking about?"
        
        return {
            'message': response_text,
            'products': products[:3],
            'intent': 'comparison'
        }
    
    def _handle_recommendation(self, message: str, intent: Dict) -> Dict[str, Any]:
        """Handle recommendation requests"""
        
        # Extract what they're looking for
        search_terms = self._extract_search_terms(message)
        budget = self._extract_budget(message)
        
        products = product_service.search_products(search_terms, top_k=5)
        
        if budget:
            products = [p for p in products if p['price'] <= budget]
        
        if products:
            best_product = products[0]
            response_text = f"Based on your needs, I'd recommend the **{best_product['name']}** by {best_product['brand']}.\n\n"
            response_text += f"💰 Price: ${best_product['price']:.2f}\n"
            response_text += f"⭐ Rating: {best_product['rating']}/5 ({best_product['review_count']} reviews)\n\n"
            response_text += f"Why it's great: {best_product['description'][:100]}...\n\n"
            response_text += "Here are a few other excellent options:"
        else:
            response_text = "I'd love to help with recommendations! Could you tell me more about what you're looking for and your budget?"
        
        return {
            'message': response_text,
            'products': products[:4],
            'intent': 'recommendation'
        }
    
    def _handle_question(self, message: str, intent: Dict) -> Dict[str, Any]:
        """Handle questions about products"""
        
        search_terms = self._extract_search_terms(message)
        products = product_service.search_products(search_terms, top_k=3)
        
        if products:
            product = products[0]
            response_text = f"About the **{product['name']}**:\n\n"
            response_text += f"💰 Price: ${product['price']:.2f}\n"
            response_text += f"⭐ Customer rating: {product['rating']}/5\n"
            response_text += f"📦 Category: {product['category']}\n"
            response_text += f"🏷️ Brand: {product['brand']}\n\n"
            response_text += f"{product['description']}"
        else:
            response_text = "I'd be happy to answer questions about our products! What specifically would you like to know?"
        
        return {
            'message': response_text,
            'products': products[:2],
            'intent': 'question'
        }
    
    def _handle_general(self, message: str) -> Dict[str, Any]:
        """Handle general conversation"""
        
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        help_requests = ['help', 'assist', 'support']
        
        message_lower = message.lower()
        
        if any(greeting in message_lower for greeting in greetings):
            response_text = "Hello! 👋 I'm your AI shopping assistant. I can help you:\n\n" \
                          "🔍 Find products: 'Find wireless headphones under $200'\n" \
                          "💡 Get recommendations: 'Recommend a good laptop for students'\n" \
                          "⚖️ Compare products: 'Compare iPhone vs Samsung phones'\n" \
                          "❓ Answer questions: 'How good is the Sony WH-1000XM5?'\n\n" \
                          "What can I help you find today?"
        elif any(help_req in message_lower for help_req in help_requests):
            response_text = "I'm here to help! You can ask me to:\n\n" \
                          "• Find specific products\n" \
                          "• Recommend items within your budget\n" \
                          "• Compare different options\n" \
                          "• Answer questions about products\n\n" \
                          "Just tell me what you're looking for!"
        else:
            response_text = "I'm your AI shopping assistant! I specialize in helping you find and compare products. " \
                          "What are you shopping for today? 🛍️"
        
        return {
            'message': response_text,
            'products': [],
            'intent': 'general'
        }
    
    def _extract_search_terms(self, message: str) -> str:
        """Extract main search terms from message"""
        # Remove common stop words and focus on product-related terms
        stop_words = {'find', 'show', 'get', 'me', 'a', 'an', 'the', 'for', 'with', 'under', 'below', 'above', 'over'}
        
        # Clean the message
        words = re.findall(r'\b\w+\b', message.lower())
        search_words = [word for word in words if word not in stop_words]
        
        return ' '.join(search_words[:6])  # Limit to 6 words for better search
    
    def _extract_budget(self, message: str) -> Optional[float]:
        """Extract budget from message"""
        # Look for price patterns
        price_patterns = [
            r'\$(\d+(?:\.\d{2})?)',
            r'under (\d+)',
            r'below (\d+)',
            r'less than (\d+)',
            r'budget (\d+)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, message.lower())
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def _extract_category(self, message: str) -> Optional[str]:
        """Extract product category from message"""
        categories = {
            'electronics': ['phone', 'laptop', 'computer', 'tablet', 'camera', 'headphones', 'speaker'],
            'clothing': ['shirt', 'pants', 'dress', 'jacket', 'clothes', 'jeans'],
            'footwear': ['shoes', 'sneakers', 'boots', 'sandals'],
            'home & kitchen': ['kitchen', 'cooking', 'blender', 'pot', 'appliance'],
            'furniture': ['chair', 'desk', 'table', 'furniture'],
            'sports & outdoors': ['fitness', 'exercise', 'outdoor', 'sports']
        }
        
        message_lower = message.lower()
        for category, keywords in categories.items():
            if any(keyword in message_lower for keyword in keywords):
                return category
        
        return None
    
    def _generate_search_response(self, query: str, products: List[Dict], budget: Optional[float]) -> str:
        """Generate natural language response for search results"""
        
        if not products:
            return f"I couldn't find any products for '{query}'. Try a different search!"
        
        response = f"Great! I found some excellent options for '{query}':\n\n"
        
        # Highlight top product
        top_product = products[0]
        response += f"🥇 **Top match**: {top_product['name']}\n"
        response += f"💰 ${top_product['price']:.2f} | ⭐ {top_product['rating']}/5\n"
        response += f"🎯 {int(top_product.get('similarity_score', 0) * 100)}% match to your search\n\n"
        
        # Mention budget if relevant
        if budget:
            budget_products = [p for p in products if p['price'] <= budget]
            if budget_products:
                response += f"💡 Within your ${budget:.0f} budget: {len(budget_products)} options found!\n\n"
        
        if len(products) > 1:
            response += "Here are more great options below. Want me to compare any of these or help you narrow down your choice? 🤔"
        
        return response

# Global instance
chat_assistant = ShoppingChatAssistant()