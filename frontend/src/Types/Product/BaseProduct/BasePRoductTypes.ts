// --- Base Product Types ---

// Base Interface
interface ProductBase {
  /** Product name (1-200 characters, unique) */
  name: string;
  /** Product description */
  description: string;
  /** Product category */
  category: string;
  /** Product tags for filtering/search */
  tags?: string[] | null;
  /** Product price */
  price: string; // Decimal as string
  /** Discount percentage (0-100) */
  discount_percentage?: string; // Decimal as string
  /** URL to product image */
  image_url: string;
  /** Whether the product is active/available */
  is_active?: boolean;
  /** Whether to display on front page */
  is_front_page?: boolean;
}

// Create Schema
type ProductBaseCreate = ProductBase;

// Update Schema
interface ProductBaseUpdate {
  /** Product name (1-200 characters) */
  name?: string;
  /** Product description */
  description?: string;
  /** Product category */
  category?: string;
  /** Product tags */
  tags?: string[] | null;
  /** Product price */
  price?: string; // Decimal as string
  /** Discount percentage (0-100) */
  discount_percentage?: string; // Decimal as string
  /** URL to product image */
  image_url?: string;
  /** Whether the product is active/available */
  is_active?: boolean;
  /** Whether to display on front page */
  is_front_page?: boolean;
}

// Read Schema
interface ProductBaseRead extends ProductBase {
  /** Unique product identifier */
  id: number;
  /** Final price after discount */
  final_price: string; // Decimal as string
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** Deletion timestamp (if soft-deleted) */
  deleted_at?: string | null;
  /** List of user IDs who favorited this product */
  favourited_product: number[];
  /** List of user IDs who commented on this product */
  comments: number[];
}

// In DB Schema
type ProductBaseInDB = ProductBaseRead;

// Extended Response with Relations
interface ProductWithRelations extends ProductBaseRead {
  /** Cart items containing this product */
  cart_items?: Array<{
    id: number;
    cart_id: number;
    quantity: number;
    created_at: string;
  }>;
  /** Order items containing this product */
  order_items?: Array<{
    id: number;
    order_id: number;
    quantity: number;
    unit_price: string;
    subtotal: string;
  }>;
}

// Product Summary (for lists/cards)
interface ProductSummary {
  /** Unique product identifier */
  id: number;
  /** Product name */
  name: string;
  /** Product category */
  category: string;
  /** Original price */
  price: string; // Decimal as string
  /** Final price after discount */
  final_price: string; // Decimal as string
  /** Discount percentage */
  discount_percentage: string; // Decimal as string
  /** URL to product image */
  image_url: string;
  /** Whether the product is active */
  is_active: boolean;
  /** Product tags */
  tags?: string[] | null;
}

// Export all interfaces
export type {
  ProductBase,
  ProductBaseCreate,
  ProductBaseUpdate,
  ProductBaseRead,
  ProductBaseInDB,
  ProductWithRelations,
  ProductSummary,
};
