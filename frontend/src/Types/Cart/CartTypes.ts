// --- Base Types ---
interface CartItemBase {
  /** Product ID */
  product_id: number;
  /** Quantity of the product (minimum 1) */
  quantity: number;
}

// --- Create Schema ---
type CartItemCreate = CartItemBase;

// --- Update Schema ---
interface CartItemUpdate {
  /** Quantity of the product (minimum 1) */
  quantity: number;
}

// --- Response Schemas ---
interface CartItemRead extends CartItemBase {
  /** Unique cart item identifier */
  id: number;
  /** Cart ID this item belongs to */
  cart_id: number;
  /** Creation timestamp */
  created_at: string;
}

// --- Cart Schemas ---
interface CartBase {
  /** User ID who owns the cart */
  user_id: number;
}

// Cart is auto-created for user, no fields needed for creation
type CartCreate = Record<string, never>;

interface CartRead extends CartBase {
  /** Unique cart identifier */
  id: number;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** List of items in the cart */
  cart_items: CartItemRead[];
  /** Total number of items in cart */
  total_items: number;
  /** Total price of all items in cart */
  total_price: string; // Decimal as string
}

type CartInDB = CartRead;

// --- Extended Response with Product Details ---
interface CartItemWithProduct extends CartItemRead {
  /** Product information */
  product?: {
    id: number;
    name: string;
    price: string; // Decimal as string
    image_url?: string | null;
    category: string;
    is_available: boolean;
  };
  /** Subtotal for this item (quantity * product price) */
  subtotal: string; // Decimal as string
}

interface CartWithProducts extends Omit<CartRead, 'cart_items'> {
  /** Cart items with full product details */
  cart_items: CartItemWithProduct[];
}

// --- Cart Operations ---
interface AddToCartRequest {
  /** Product ID to add */
  product_id: number;
  /** Quantity to add (default: 1) */
  quantity?: number;
}

interface UpdateCartItemRequest {
  /** New quantity for the item */
  quantity: number;
}

interface CartSummary {
  /** Total number of unique items */
  item_count: number;
  /** Total quantity of all items */
  total_quantity: number;
  /** Total price of cart */
  total_price: string; // Decimal as string
  /** Whether cart has any items */
  is_empty: boolean;
}

// Export all interfaces
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