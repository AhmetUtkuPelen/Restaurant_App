import type { SupplierResponse } from '../Supplier/SupplierTypes';

export enum ReorderLevel {
  LOW = "LOW",
  MEDIUM = "MEDIUM",
  HIGH = "HIGH"
}

// Base Interface
export interface DrinkBase {
  /** Name of the drink */
  name: string;
  /** Brand of the drink */
  brand?: string | null;
  /** Description of the drink */
  description?: string | null;
  /** URL to drink image */
  image?: string | null;
  /** Tags for categorization */
  tags?: string | null;
  /** Additional notes */
  notes?: string | null;
  /** Recommended storage temperature */
  storage_temp?: string | null;
  /** Size in milliliters */
  size_ml: number;
  /** Price of the drink */
  price: number;
  /** Current stock quantity */
  in_stock: number;
  /** Minimum stock level before reorder */
  min_stock?: number | null;
  /** Maximum stock capacity */
  max_stock?: number | null;
  /** Reorder level indicator */
  reorder_level?: ReorderLevel;
  /** Whether the drink is sugar-free */
  sugar_free: boolean;
  /** Whether the drink is carbonated */
  carbonated: boolean;
  /** Whether the drink should be served cold */
  is_cold: boolean;
  /** Supplier ID */
  supplier_id?: number | null;
  /** Supplier details */
  supplier?: SupplierResponse | null;
}

// Create Schema
export type DrinkCreate = Omit<DrinkBase, 'supplier' | 'created_at' | 'updated_at' | 'deleted_at'>;

// Update Schema
export interface DrinkUpdate {
  name?: string;
  brand?: string | null;
  size_ml?: number;
  price?: number;
  in_stock?: number;
  reorder_level?: number;
  sugar_free?: boolean;
  carbonated?: boolean;
  is_cold?: boolean;
  description?: string | null;
  image?: string | null;
  supplier_id?: number | null;
}

// Read/Response Schema
export interface DrinkResponse extends Omit<DrinkBase, 'supplier_id'> {
  /** Unique identifier */
  id: number;
  /** Whether the drink needs to be reordered */
  needs_reorder: boolean;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at: string | null;
}