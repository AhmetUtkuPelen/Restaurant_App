import type { ProductBaseCreate, ProductBaseUpdate, ProductBaseRead } from '../BaseProduct/BaseProductTypes';

// Enums \\
type DonerSize = 'SMALL' | 'MEDIUM' | 'LARGE' | 'EXTRA_LARGE';
type MeatType = 'CHICKEN' | 'BEEF' | 'LAMB' | 'MIXED' | 'VEGETARIAN';
type SpiceLevel = 'MILD' | 'MEDIUM' | 'HOT' | 'EXTRA_HOT';

// Base Types \\
interface DonerBase {
  size: DonerSize;
  meat_type: MeatType;
  spice_level: SpiceLevel;
  is_vegan: boolean;
  is_alergic: boolean;
}

// Create Schema \\
interface DonerCreate extends ProductBaseCreate, DonerBase {
  category: 'doner';
}

// Update Schema \\
interface DonerUpdate extends ProductBaseUpdate {
  size?: DonerSize;
  meat_type?: MeatType;
  spice_level?: SpiceLevel;
  is_vegan?: boolean;
  is_alergic?: boolean;
}

// Read Schema \\
interface DonerRead extends ProductBaseRead, DonerBase { }

// In DB Schema \\
type DonerInDB = DonerRead;

// Extended Response \\
interface DonerWithDetails extends DonerRead {
  summary?: string;
  description_summary?: string;
}

// Doner Summary (for lists) \\
interface DonerSummary {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  size: DonerSize;
  meat_type: MeatType;
  spice_level: SpiceLevel;
  is_active: boolean;
}

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