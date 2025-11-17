import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BasePRoductTypes';

// --- Enums ---
type DonerSize = 'SMALL' | 'MEDIUM' | 'LARGE' | 'EXTRA_LARGE';
type MeatType = 'CHICKEN' | 'BEEF' | 'LAMB' | 'MIXED' | 'VEGETARIAN';
type SpiceLevel = 'MILD' | 'MEDIUM' | 'HOT' | 'EXTRA_HOT';

// --- Base Types ---
interface DonerBase {
  /** Size of the doner */
  size: DonerSize;
  /** Type of meat used */
  meat_type: MeatType;
  /** Spice level */
  spice_level: SpiceLevel;
  /** Whether the doner is vegan */
  is_vegan: boolean;
  /** Whether the doner contains allergens */
  is_alergic: boolean;
}

// --- Create Schema ---
interface DonerCreate extends ProductBaseCreate, DonerBase {
  /** Category is always 'doner' */
  category: 'doner';
}

// --- Update Schema ---
interface DonerUpdate extends ProductBaseUpdate {
  /** Size of the doner */
  size?: DonerSize;
  /** Type of meat used */
  meat_type?: MeatType;
  /** Spice level */
  spice_level?: SpiceLevel;
  /** Whether the doner is vegan */
  is_vegan?: boolean;
  /** Whether the doner contains allergens */
  is_alergic?: boolean;
}

// --- Read Schema ---
interface DonerRead extends ProductBaseRead, DonerBase {
  // Combines product base fields with doner-specific fields
}

// --- In DB Schema ---
type DonerInDB = DonerRead;

// --- Extended Response ---
interface DonerWithDetails extends DonerRead {
  /** Readable summary of the doner */
  summary?: string;
  /** Description summary */
  description_summary?: string;
}

// --- Doner Summary (for lists) ---
interface DonerSummary {
  /** Unique doner identifier */
  id: number;
  /** Doner name */
  name: string;
  /** Original price */
  price: string;
  /** Final price after discount */
  final_price: string;
  /** URL to doner image */
  image_url: string;
  /** Size of the doner */
  size: DonerSize;
  /** Type of meat */
  meat_type: MeatType;
  /** Spice level */
  spice_level: SpiceLevel;
  /** Whether it's active */
  is_active: boolean;
}

// Export all interfaces
export type {
  DonerSize,
  MeatType,
  SpiceLevel,
  DonerBase,
  DonerCreate,
  DonerUpdate,
  DonerRead,
  DonerInDB,
  DonerWithDetails,
  DonerSummary
};
