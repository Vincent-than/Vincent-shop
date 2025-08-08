import { create } from 'zustand';

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

interface CartItem extends Product {
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  totalItems: number;
  totalPrice: number;
  isOpen: boolean;
  
  addItem: (product: Product) => void;
  removeItem: (productId: number) => void;
  updateQuantity: (productId: number, quantity: number) => void;
  clearCart: () => void;
  toggleCart: () => void;
  getItemCount: () => number;
  getTotalPrice: () => number;
}

export const useCartStore = create<CartStore>((set, get) => ({
  items: [],
  totalItems: 0,
  totalPrice: 0,
  isOpen: false,

  addItem: (product: Product) => {
    const state = get();
    const existingItem = state.items.find(item => item.id === product.id);
    
    if (existingItem) {
      set({
        items: state.items.map(item =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        )
      });
    } else {
      set({
        items: [...state.items, { ...product, quantity: 1 }]
      });
    }
  },

  removeItem: (productId: number) => {
    set(state => ({
      items: state.items.filter(item => item.id !== productId)
    }));
  },

  updateQuantity: (productId: number, quantity: number) => {
    if (quantity <= 0) {
      get().removeItem(productId);
      return;
    }
    
    set(state => ({
      items: state.items.map(item =>
        item.id === productId
          ? { ...item, quantity }
          : item
      )
    }));
  },

  clearCart: () => {
    set({
      items: [],
      totalItems: 0,
      totalPrice: 0
    });
  },

  toggleCart: () => {
    set(state => ({ isOpen: !state.isOpen }));
  },

  getItemCount: () => {
    const state = get();
    return state.items.reduce((total, item) => total + item.quantity, 0);
  },

  getTotalPrice: () => {
    const state = get();
    return state.items.reduce((total, item) => total + (item.price * item.quantity), 0);
  }
}));