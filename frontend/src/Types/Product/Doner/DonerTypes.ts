import type { IngredientInResponse } from '../Ingredient/IngredientTypes';

// Base Interface
export interface DonerBase {
  /** Name of the doner */
  name: string;
  /** Optional description */
  description?: string | null;
  /** Price of the doner */
  price: number;
  /** Discount percentage (0-100) */
  discount_percentage: number;
  /** URL to doner image */
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

// Create Schema
export interface DonerCreate extends Omit<DonerBase, 'created_at' | 'updated_at' | 'deleted_at' | 'ingredient_count'> {
  ingredient_ids: number[];
}

// Update Schema
export type DonerUpdate = Partial<DonerCreate>;

// Database Schema
export interface DonerInDB extends Omit<DonerBase, 'ingredient_ids'> {
  /** Unique identifier */
  id: number;
  created_at: string;
  updated_at: string | null;
  deleted_at: string | null;
}

// Response Schema
export interface DonerResponse extends DonerInDB {
  /** Price after applying discount */
  discounted_price: number;
  /** Total calories in the doner */
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
export interface DonerForList {
  /** Unique identifier */
  id: number;
  /** Name of the doner */
  name: string;
  /** Original price */
  price: number;
  /** Price after discount */
  discounted_price: number;
  /** URL to doner image */
  image?: string | null;
  /** Count of ingredients */
  ingredient_count: number;
}