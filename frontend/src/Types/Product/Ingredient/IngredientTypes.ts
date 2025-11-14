// Enums

export enum ReorderLevel {
  LOW = "LOW",
  MEDIUM = "MEDIUM",
  HIGH = "HIGH"
}

// Base Interface

export interface IngredientBase {
  /** Name of the ingredient */
  name: string;
  /** Detailed description of the ingredient */
  description?: string | null;
  /** Calories per standard unit */
  calories: number;
  /** True if the ingredient is vegan */
  is_vegan: boolean;
  /** True if the ingredient is gluten-free */
  is_gluten_free: boolean;
  /** True if the ingredient contains common allergens */
  contains_allergens: boolean;
  /** Price per standard unit */
  price: number;
  /** Discount percentage (0-100) */
  discount_percentage: number;
  /** Measurement unit (e.g., 'g', 'ml', 'pcs') */
  unit: string;
  /** Stock Keeping Unit for inventory tracking */
  sku?: string | null;
  /** Category for grouping (e.g., 'Vegetable', 'Meat', 'Spice') */
  category?: string | null;
  /** URL of an image for the ingredient */
  image?: string | null;

  // Nutritional Information
  /** Grams of protein per unit */
  protein: number;
  /** Grams of carbohydrates per unit */
  carbs: number;
  /** Grams of fat per unit */
  fat: number;
  /** Grams of sugar per unit */
  sugar: number;
  /** Milligrams of sodium per unit */
  sodium: number;

  // Inventory and Supply Chain
  /** Minimum desired stock level before reordering */
  min_stock: number;
  /** Maximum desired stock level to avoid overstocking */
  max_stock: number;
  /** Current quantity in stock */
  current_stock: number;
  /** Name of the primary supplier */
  supplier_name?: string | null;
  /** Urgency level for reordering */
  reorder_level?: ReorderLevel | null;
  /** False if the ingredient is temporarily disabled */
  is_active: boolean;
  /** Recommended storage temperature (e.g., '0-4°C') */
  storage_temp?: string | null;
  /** Expected shelf life in days from acquisition */
  shelf_life_days?: number | null;
  /** Expiration date of the current batch */
  expiration_date?: string | null;
  /** Comma-separated tags for filtering/searching */
  tags?: string | null;
  /** Internal notes about the ingredient */
  notes?: string | null;
}

// Create Schema
export type IngredientCreate = Omit<IngredientBase, 'is_active'>;

// Update Schema
export interface IngredientUpdate {
  name?: string;
  description?: string | null;
  calories?: number;
  is_vegan?: boolean;
  is_gluten_free?: boolean;
  contains_allergens?: boolean;
  price?: number;
  discount_percentage?: number;
  unit?: string;
  sku?: string | null;
  category?: string | null;
  image?: string | null;
  protein?: number;
  carbs?: number;
  fat?: number;
  sugar?: number;
  sodium?: number;
  min_stock?: number;
  max_stock?: number;
  current_stock?: number;
  supplier_name?: string | null;
  reorder_level?: ReorderLevel | null;
  is_active?: boolean;
  storage_temp?: string | null;
  shelf_life_days?: number | null;
  expiration_date?: string | null;
  tags?: string | null;
  notes?: string | null;
}

// Database Schema
export interface IngredientInDB extends IngredientBase {
  /** Unique identifier */
  id: number;
  /** Timestamp of creation */
  created_at: string;
  /** Timestamp of last update */
  updated_at: string | null;
  /** Timestamp of soft deletion */
  deleted_at: string | null;
}

// Response Schemas

export interface Ingredient extends IngredientInDB {
  /** Price after applying the discount */
  discounted_price: number;
  /** True if current stock is at or below minimum stock */
  needs_reorder: boolean;
  /** Ratio of current stock to maximum stock (0.0 to 1.0+) */
  stock_ratio: number;
  /** Warning message if the ingredient contains allergens */
  allergen_warning?: {
    [key: string]: boolean;
  } | null;
}

export interface IngredientForList {
  /** Unique identifier */
  id: number;
  /** Name of the ingredient */
  name: string;
  /** Price per standard unit */
  price: number;
  /** Price after discount */
  discounted_price: number;
  /** Current quantity in stock */
  current_stock: number;
  /** True if the ingredient is active */
  is_active: boolean;
  /** Category for grouping */
  category?: string | null;
  /** URL of an image for the ingredient */
  image?: string | null;
  /** True if stock is low and needs reorder */
  needs_reorder: boolean;
}

export interface IngredientStockInfo {
  /** Unique identifier */
  id: number;
  /** Name of the ingredient */
  name: string;
  /** Stock Keeping Unit */
  sku?: string | null;
  /** Current quantity in stock */
  current_stock: number;
  /** Minimum desired stock level */
  min_stock: number;
  /** Maximum desired stock level */
  max_stock: number;
  /** Name of the primary supplier */
  supplier_name?: string | null;
  /** True if stock is low and needs reorder */
  needs_reorder: boolean;
  /** Ratio of current stock to maximum stock */
  stock_ratio: number;
}

export interface IngredientInResponse {
  /** Unique identifier */
  id: number;
  /** Name of the ingredient */
  name: string;
  /** Price per standard unit */
  price: number;
  /** Price after discount */
  discounted_price: number;
  /** Quantity used in the recipe */
  quantity: number;
  /** Measurement unit */
  unit: string;
}