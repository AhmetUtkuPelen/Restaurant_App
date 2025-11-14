import type { IngredientInResponse } from '../Ingredient/IngredientTypes';

// Base Interface
export interface KebabBase {
  /** Name of the kebab */
  name: string;
  /** Optional description */
  description?: string | null;
  /** Price of the kebab */
  price: number;
  /** Discount percentage (0-100) */
  discount_percentage: number;
  /** URL to kebab image */
  image?: string | null;
  /** List of ingredient IDs */
  ingredient_ids: number[];
  /** Count of ingredients */
  ingredient_count: number;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at: string | null;
  /** Deletion timestamp if soft-deleted */
  deleted_at: string | null;
}

// Kebab Ingredient Schema
export interface KebabIngredientCreate {
  /** ID of the ingredient */
  ingredient_id: number;
  /** Quantity needed */
  quantity: number;
  /** Unit of measurement (default: 'g') */
  unit: string;
}

// Create Schema
export interface KebabCreate extends Omit<KebabBase, 'created_at' | 'updated_at' | 'deleted_at' | 'ingredient_count'> {
  /** List of ingredients with quantities */
  ingredients: KebabIngredientCreate[];
}

// Update Schema
export type KebabUpdate = Partial<KebabBase>;

// Database Schema
export interface KebabInDB extends Omit<KebabBase, 'ingredient_ids'> {
  /** Unique identifier */
  id: number;
  created_at: string;
  updated_at: string | null;
  deleted_at: string | null;
}

// Response Schema
export interface KebabResponse extends KebabInDB {
  /** Price after applying discount */
  discounted_price: number;
  /** Total calories in the kebab */
  total_calories: number;
  /** Total protein content */
  total_protein: number;
  /** Total carbohydrates content */
  total_carbs: number;
  /** Total fat content */
  total_fat: number;
  /** Allergen warnings */
  allergen_warning: Record<string, unknown>;
  /** Stock warnings */
  stock_warning: Record<string, unknown>;
  /** List of ingredients with details */
  ingredients: IngredientInResponse[];
}

// List View Schema
export interface KebabForList {
  /** Unique identifier */
  id: number;
  /** Name of the kebab */
  name: string;
  /** Original price */
  price: number;
  /** Price after discount */
  discounted_price: number;
  /** URL to kebab image */
  image?: string | null;
  /** Count of ingredients */
  ingredient_count: number;
}