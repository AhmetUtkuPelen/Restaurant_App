import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BasePRoductTypes';

// --- Enums ---
type DrinkSize = 'SMALL' | 'MEDIUM' | 'LARGE' | 'EXTRA_LARGE';

// --- Base Types ---
interface DrinkBase {
  /** Size of the drink */
  size: DrinkSize;
  /** Whether the drink is acidic */
  is_acidic: boolean;
}

// --- Create Schema ---
interface DrinkCreate extends ProductBaseCreate, DrinkBase {
  /** Category is always 'drink' */
  category: 'drink';
}

// --- Update Schema ---
interface DrinkUpdate extends ProductBaseUpdate {
  /** Size of the drink */
  size?: DrinkSize;
  /** Whether the drink is acidic */
  is_acidic?: boolean;
}

// --- Read Schema ---
interface DrinkRead extends ProductBaseRead, DrinkBase {
  // Combines product base fields with drink-specific fields
}

// --- In DB Schema ---
type DrinkInDB = DrinkRead;

// --- Extended Response ---
interface DrinkWithDetails extends DrinkRead {
  /** Summary of the drink */
  summary?: string;
}

// --- Drink Summary (for lists) ---
interface DrinkSummary {
  /** Unique drink identifier */
  id: number;
  /** Drink name */
  name: string;
  /** Original price */
  price: string;
  /** Final price after discount */
  final_price: string;
  /** URL to drink image */
  image_url: string;
  /** Size of the drink */
  size: DrinkSize;
  /** Whether it's acidic */
  is_acidic: boolean;
  /** Whether it's active */
  is_active: boolean;
}

// Export all interfaces
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
