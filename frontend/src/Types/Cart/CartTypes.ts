// Base Types \\
interface CartItemBase {
  product_id: number;
  quantity: number;
}

// Create Schema \\
type CartItemCreate = CartItemBase;

// Update Schema \\
interface CartItemUpdate {
  quantity: number;
}

// Response Schemas \\
interface CartItemRead extends CartItemBase {
  id: number;
  cart_id: number;
  created_at: string;
}

// Cart Schemas \\
interface CartBase {
  user_id: number;
}

// Cart is auto-created for user \\
type CartCreate = Record<string, never>;

interface CartRead extends CartBase {
  id: number;
  created_at: string;
  updated_at?: string | null;
  cart_items: CartItemRead[];
  total_items: number;
  total_price: string;
}

type CartInDB = CartRead;

// Extended Response with Product Details \\
interface CartItemWithProduct extends CartItemRead {
  // Product information \\
  product?: {
    id: number;
    name: string;
    price: string;
    image_url?: string | null;
    category: string;
    is_available: boolean;
  };
  //** Subtotal for this item (quantity * product price) \\
  subtotal: string;
}

interface CartWithProducts extends Omit<CartRead, 'cart_items'> {
  // Cart items with full product details \\
  cart_items: CartItemWithProduct[];
}

// Cart Operations \\
interface AddToCartRequest {
  product_id: number;
  quantity?: number;
}

interface UpdateCartItemRequest {
  quantity: number;
}

interface CartSummary {
  item_count: number;
  total_quantity: number;
  total_price: string;
  is_empty: boolean;
}

export type {
  CartItemBase,
  CartItemCreate,
  CartItemUpdate,
  CartItemRead,
  CartBase,
  CartCreate,
  CartRead,
  CartInDB,
  CartItemWithProduct,
  CartWithProducts,
  AddToCartRequest,
  UpdateCartItemRequest,
  CartSummary
};