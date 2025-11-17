import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BasePRoductTypes';

// --- Base Types ---
interface SaladBase {
  /** Whether the salad is vegan */
  is_vegan: boolean;
  /** Whether the salad contains allergens */
  is_alergic: boolean;
  /** Calories per serving */
  calories: number;
}

// --- Create Schema ---
interface SaladCreate extends ProductBaseCreate, SaladBase {
  /** Category is always 'salad' */
  category: 'salad';
}

// --- Update Schema ---
interface SaladUpdate extends ProductBaseUpdate {
  /** Whether the salad is vegan */
  is_vegan?: boolean;
  /** Whether the salad contains allergens */
  is_alergic?: boolean;
  /** Calories per serving */
  calories?: number;
}

// --- Read Schema ---
interface SaladRead extends ProductBaseRead, SaladBase {
  // Combines product base fields with salad-specific fields
}

// --- In DB Schema ---
type SaladInDB = SaladRead;

// --- Extended Response ---
interface SaladWithDetails extends SaladRead {
  /** Summary of the salad */
  summary?: string;
}

// --- Salad Summary (for lists) ---
interface SaladSummary {
  /** Unique salad identifier */
  id: number;
  /** Salad name */
  name: string;
  /** Original price */
  price: string;
  /** Final price after discount */
  final_price: string;
  /** URL to salad image */
  image_url: string;
  /** Whether it's vegan */
  is_vegan: boolean;
  /** Calories per serving */
  calories: number;
  /** Whether it's active */
  is_active: boolean;
}

// Export all interfaces
export type {
  SaladBase,
  SaladCreate,
  SaladUpdate,
  SaladRead,
  SaladInDB,
  SaladWithDetails,
  SaladSummary
};
