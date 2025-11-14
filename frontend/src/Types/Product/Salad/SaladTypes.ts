import type { IngredientInResponse } from '../Ingredient/IngredientTypes';

// Base Interface
export interface SaladBase {
  /** Name of the salad */
  name: string;
  /** Optional description */
  description?: string | null;
  /** Price of the salad */
  price: number;
  /** Discount percentage (0-100) */
  discount_percentage: number;
  /** URL to salad image */
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
export type SaladCreate = Omit<SaladBase, 'created_at' | 'updated_at' | 'deleted_at' | 'ingredient_count'>;

// Update Schema
export type SaladUpdate = Partial<SaladCreate>;

// Database Schema
export interface SaladInDB extends Omit<SaladBase, 'ingredient_ids'> {
  /** Unique identifier */
  id: number;
}

// Response Schema
export interface SaladResponse extends SaladInDB {
  /** Price after applying discount */
  discounted_price: number;
  /** Total calories in the salad */
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
export interface SaladForList {
  /** Unique identifier */
  id: number;
  /** Name of the salad */
  name: string;
  /** Original price */
  price: number;
  /** Price after discount */
  discounted_price: number;
  /** URL to salad image */
  image?: string | null;
  /** Count of ingredients */
  ingredient_count: number;
}