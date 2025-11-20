import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BaseProductTypes';

// Enums \\
type KebabSize = 'SMALL' | 'MEDIUM' | 'LARGE' | 'EXTRA_LARGE';
type MeatType = 'CHICKEN' | 'BEEF' | 'LAMB' | 'MIXED' | 'VEGETARIAN';
type SpiceLevel = 'MILD' | 'MEDIUM' | 'HOT' | 'EXTRA_HOT';

// Base Types \\
interface KebabBase {
  size: KebabSize;
  meat_type: MeatType;
  spice_level: SpiceLevel;
  is_vegan: boolean;
  is_alergic: boolean;
}

// Create Schema \\
interface KebabCreate extends ProductBaseCreate, KebabBase {
  category: 'kebab';
}

// Update Schema \\
interface KebabUpdate extends ProductBaseUpdate {
  size?: KebabSize;
  meat_type?: MeatType;
  spice_level?: SpiceLevel;
  is_vegan?: boolean;
  is_alergic?: boolean;
}

// Read Schema \\
interface KebabRead extends ProductBaseRead, KebabBase { }

// In DB Schema \\
type KebabInDB = KebabRead;

// Extended Response \\
interface KebabWithDetails extends KebabRead {
  summary?: string;
  description_summary?: string;
}

// Kebab Summary (for lists) \\
interface KebabSummary {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  size: KebabSize;
  meat_type: MeatType;
  spice_level: SpiceLevel;
  is_active: boolean;
}

export type {
  KebabSize,
  SpiceLevel,
  KebabBase,
  KebabCreate,
  KebabUpdate,
  KebabRead,
  KebabInDB,
  KebabWithDetails,
  KebabSummary
};