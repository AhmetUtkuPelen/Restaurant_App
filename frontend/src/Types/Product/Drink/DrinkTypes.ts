import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BaseProductTypes';

// Enums \\
type DrinkSize = 'SMALL' | 'MEDIUM' | 'LARGE' | 'EXTRA_LARGE';

// Base Types \\
interface DrinkBase {
  size: DrinkSize;
  is_acidic: boolean;
}

// Create Schema \\
interface DrinkCreate extends ProductBaseCreate, DrinkBase {
  category: 'drink';
}

// Update Schema \\
interface DrinkUpdate extends ProductBaseUpdate {
  size?: DrinkSize;
  is_acidic?: boolean;
}

// Read Schema \\
interface DrinkRead extends ProductBaseRead, DrinkBase { }

// In DB Schema \\
type DrinkInDB = DrinkRead;

// Extended Response \\
interface DrinkWithDetails extends DrinkRead {
  summary?: string;
}

// Drink Summary (for lists) \\
interface DrinkSummary {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  size: DrinkSize;
  is_acidic: boolean;
  is_active: boolean;
}

export type {
  DrinkSize,
  DrinkBase,
  DrinkCreate,
  DrinkUpdate,
  DrinkRead,
  DrinkInDB,
  DrinkWithDetails,
  DrinkSummary
};