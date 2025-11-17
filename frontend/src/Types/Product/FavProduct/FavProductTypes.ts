// --- Base Types ---
interface FavouriteProductBase {
  /** User ID who favorited the product */
  user_id: number;
  /** Product ID that was favorited */
  product_id: number;
}

// --- Create Schema ---
interface FavouriteProductCreate {
  /** Product ID to add to favorites */
  product_id: number;
  // user_id will come from authenticated user
}

// --- Read Schema ---
interface FavouriteProductRead extends FavouriteProductBase {
  /** Unique favorite identifier */
  id: number;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
}

// --- In DB Schema ---
interface FavouriteProductInDB extends FavouriteProductRead {
  /** Deletion timestamp (if soft-deleted) */
  deleted_at?: string | null;
}

// --- Extended Response with Relations ---
interface FavouriteProductWithUser extends FavouriteProductRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
  };
}

interface FavouriteProductWithProduct extends FavouriteProductRead {
  /** Product information */
  product?: {
    id: number;
    name: string;
    category: string;
    price: string;
    final_price: string;
    image_url: string;
    is_active: boolean;
  };
}

interface FavouriteProductWithRelations extends FavouriteProductRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
  };
  /** Product information */
  product?: {
    id: number;
    name: string;
    category: string;
    price: string;
    final_price: string;
    image_url: string;
    is_active: boolean;
  };
}

// --- User's Favorite Products List ---
interface UserFavoritesList {
  /** Total number of favorites */
  total: number;
  /** List of favorite products with details */
  favorites: FavouriteProductWithProduct[];
}

// Export all interfaces
export type {
  FavouriteProductBase,
  FavouriteProductCreate,
  FavouriteProductRead,
  FavouriteProductInDB,
  FavouriteProductWithUser,
  FavouriteProductWithProduct,
  FavouriteProductWithRelations,
  UserFavoritesList
};
