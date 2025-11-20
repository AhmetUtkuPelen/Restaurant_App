// Base Product Types \\

// Base Interface \\
interface ProductBase {
  name: string;
  description: string;
  category: string;
  tags?: string[] | null;
  price: string;
  discount_percentage?: string;
  image_url: string;
  is_active?: boolean;
  is_front_page?: boolean;
}

// Create Schema \\
type ProductBaseCreate = ProductBase;

// Update Schema \\
interface ProductBaseUpdate {
  name?: string;
  description?: string;
  category?: string;
  tags?: string[] | null;
  price?: string;
  discount_percentage?: string;
  image_url?: string;
  is_active?: boolean;
  is_front_page?: boolean;
}

// Read Schema \\
interface ProductBaseRead extends ProductBase {
  id: number;
  final_price: string;
  created_at: string;
  updated_at?: string | null;
  deleted_at?: string | null;
  favourited_product: number[];
  comments: number[];
}

// In DB Schema \\
type ProductBaseInDB = ProductBaseRead;

// Extended Response with Relations \\
interface ProductWithRelations extends ProductBaseRead {
  cart_items?: Array<{
    id: number;
    cart_id: number;
    quantity: number;
    created_at: string;
  }>;
  order_items?: Array<{
    id: number;
    order_id: number;
    quantity: number;
    unit_price: string;
    subtotal: string;
  }>;
}

// Product Summary (for lists/cards) \\
interface ProductSummary {
  id: number;
  name: string;
  category: string;
  price: string;
  final_price: string;
  discount_percentage: string;
  image_url: string;
  is_active: boolean;
  tags?: string[] | null;
}

export type {
  ProductBase,
  ProductBaseCreate,
  ProductBaseUpdate,
  ProductBaseRead,
  ProductBaseInDB,
  ProductWithRelations,
  ProductSummary,
};