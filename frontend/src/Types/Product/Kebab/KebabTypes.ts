import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BasePRoductTypes';

// --- Enums ---
type KebabSize = 'SMALL' | 'MEDIUM' | 'LARGE' | 'EXTRA_LARGE';
type MeatType = 'CHICKEN' | 'BEEF' | 'LAMB' | 'MIXED' | 'VEGETARIAN';
type SpiceLevel = 'MILD' | 'MEDIUM' | 'HOT' | 'EXTRA_HOT';

// --- Base Types ---
interface KebabBase {
  /** Size of the kebab */
  size: KebabSize;
  /** Type of meat used */
  meat_type: MeatType;
  /** Spice level */
  spice_level: SpiceLevel;
  /** Whether the kebab is vegan */
  is_vegan: boolean;
  /** Whether the kebab contains allergens */
  is_alergic: boolean;
}

// --- Create Schema ---
interface KebabCreate extends ProductBaseCreate, KebabBase {
  /** Category is always 'kebab' */
  category: 'kebab';
}

// --- Update Schema ---
interface KebabUpdate extends ProductBaseUpdate {
  /** Size of the kebab */
  size?: KebabSize;
  /** Type of meat used */
  meat_type?: MeatType;
  /** Spice level */
  spice_level?: SpiceLevel;
  /** Whether the kebab is vegan */
  is_vegan?: boolean;
  /** Whether the kebab contains allergens */
  is_alergic?: boolean;
}

// --- Read Schema ---
interface KebabRead extends ProductBaseRead, KebabBase {
  // Combines product base fields with kebab-specific fields
}

// --- In DB Schema ---
type KebabInDB = KebabRead;

// --- Extended Response ---
interface KebabWithDetails extends KebabRead {
  /** Readable summary of the kebab */
  summary?: string;
  /** Description summary */
  description_summary?: string;
}

// --- Kebab Summary (for lists) ---
interface KebabSummary {
  /** Unique kebab identifier */
  id: number;
  /** Kebab name */
  name: string;
  /** Original price */
  price: string;
  /** Final price after discount */
  final_price: string;
  /** URL to kebab image */
  image_url: string;
  /** Size of the kebab */
  size: KebabSize;
  /** Type of meat */
  meat_type: MeatType;
  /** Spice level */
  spice_level: SpiceLevel;
  /** Whether it's active */
  is_active: boolean;
}

// Export all interfaces
export type {
  KebabSize,
  MeatType,
  SpiceLevel,
  KebabBase,
  KebabCreate,
  KebabUpdate,
  KebabRead,
  KebabInDB,
  KebabWithDetails,
  KebabSummary
};
