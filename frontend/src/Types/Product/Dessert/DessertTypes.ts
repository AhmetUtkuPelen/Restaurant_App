import type { IngredientInResponse } from '../Ingredient/IngredientTypes';
import type { SupplierResponse } from '../Supplier/SupplierTypes';

// Base Interface
export interface DessertBase {
  /** Name of the dessert */
  name: string;
  /** Optional description */
  description?: string | null;
  /** Price of the dessert */
  price: number;
  /** Discount percentage (0-100) */
  discount_percentage: number;
  /** URL to dessert image */
  image?: string | null;
  /** List of ingredient IDs */
  ingredient_ids: number[];
  /** Count of ingredients */
  ingredient_count: number;
  /** Optional supplier ID */
  supplier_id?: number | null;
  /** Optional supplier details */
  supplier?: SupplierResponse | null;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at: string | null;
  /** Deletion timestamp if soft-deleted */
  deleted_at: string | null;
}

// Create Schema
export type DessertCreate = Omit<DessertBase, 'created_at' | 'updated_at' | 'deleted_at' | 'ingredient_count'>;

// Update Schema
export type DessertUpdate = Partial<DessertCreate>;

// Database Schema
export interface DessertInDB extends Omit<DessertBase, 'ingredient_ids' | 'supplier'> {
  /** Unique identifier */
  id: number;
}

// Response Schema
export interface DessertResponse extends DessertInDB {
  /** Price after applying discount */
  discounted_price: number;
  /** Total calories in the dessert */
  total_calories: number;
  /** Total protein content */
  total_protein: number;
  /** Total carbohydrates content */
  total_carbs: number;
  /** Total fat content */
  total_fat: number;
  /** Allergen warnings */
  allergen_warning: Record<string, unknown>;
  /** List of ingredients with details */
  ingredients: IngredientInResponse[];
}

// List View Schema
export interface DessertForList {
  /** Unique identifier */
  id: number;
  /** Name of the dessert */
  name: string;
  /** Original price */
  price: number;
  /** Price after discount */
  discounted_price: number;
  /** URL to dessert image */
  image?: string | null;
  /** Count of ingredients */
  ingredient_count: number;
}