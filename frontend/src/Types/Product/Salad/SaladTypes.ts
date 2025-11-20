import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BaseProductTypes';

// Base Types \\
interface SaladBase {
  is_vegan: boolean;
  is_alergic: boolean;
  calories: number;
}

// Create Schema \\
interface SaladCreate extends ProductBaseCreate, SaladBase {
  category: 'salad';
}

// Update Schema \\
interface SaladUpdate extends ProductBaseUpdate {
  is_vegan?: boolean;
  is_alergic?: boolean;
  calories?: number;
}

// Read Schema \\
interface SaladRead extends ProductBaseRead, SaladBase { }

// In DB Schema \\
type SaladInDB = SaladRead;

// Extended Response \\
interface SaladWithDetails extends SaladRead {
  summary?: string;
}

// Salad Summary (for lists) \\
interface SaladSummary {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  is_vegan: boolean;
  calories: number;
  is_active: boolean;
}

export type {
  SaladBase,
  SaladCreate,
  SaladUpdate,
  SaladRead,
  SaladInDB,
  SaladWithDetails,
  SaladSummary
};