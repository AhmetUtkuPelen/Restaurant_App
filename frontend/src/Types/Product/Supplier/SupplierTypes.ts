// Base Interface
export interface SupplierBase {
  /** Unique name of the supplier */
  name: string;
  /** Short description of the supplier */
  description?: string | null;
  /** Supplier contact details such as email or phone */
  contact_info?: string | null;
  /** Physical address or warehouse location */
  address?: string | null;
  /** Optional image or logo of the supplier */
  image?: string | null;
}

// Create Schema
// Remove this interface and use SupplierBase directly
export type SupplierCreate = SupplierBase;

// Update Schema
export interface SupplierUpdate {
  name?: string;
  description?: string | null;
  contact_info?: string | null;
  address?: string | null;
  image?: string | null;
}

// Database Schema
export interface SupplierInDB extends SupplierBase {
  /** Unique identifier for the supplier */
  id: number;
  /** Timestamp when the supplier was created */
  created_at: string; // Using string here as dates are typically serialized to ISO strings in APIs
  /** Timestamp when the supplier was last updated */
  updated_at: string | null;
}

// Response Schemas
export type SupplierResponse = SupplierInDB;

export interface SupplierForList {
  /** Unique identifier for the supplier */
  id: number;
  /** Name of the supplier */
  name: string;
  /** Contact information */
  contact_info: string | null;
  /** Physical address */
  address: string | null;
  /** URL to supplier's image/logo */
  image: string | null;
}

// Example data (for reference)
export const exampleSupplier: SupplierBase = {
  name: "FarmFresh Organics",
  description: "Supplier of fresh organic vegetables and ingredients.",
  contact_info: "farmfresh@example.com / +90 555 123 4567",
  address: "Yeniköy Mah. No:12, İzmir, Türkiye",
  image: "https://example.com/suppliers/farmfresh.png"
};