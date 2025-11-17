import type {
  ProductBaseCreate,
  ProductBaseUpdate,
  ProductBaseRead,
} from "../BaseProduct/BasePRoductTypes";

// --- Enums ---
type DessertType =
  | "CAKE"
  | "PIE"
  | "PUDDING"
  | "ICE_CREAM"
  | "PASTRY"
  | "COOKIE"
  | "OTHER";

// --- Base Types ---
interface DessertBase {
  /** Whether the dessert is vegan */
  is_vegan: boolean;
  /** Whether the dessert contains allergens */
  is_alergic: boolean;
  /** Type of dessert */
  dessert_type: DessertType;
  /** Calories per serving */
  calories: number;
}

// --- Create Schema ---
interface DessertCreate extends ProductBaseCreate, DessertBase {
  /** Category is always 'dessert' */
  category: "dessert";
}

// --- Update Schema ---
interface DessertUpdate extends ProductBaseUpdate {
  /** Whether the dessert is vegan */
  is_vegan?: boolean;
  /** Whether the dessert contains allergens */
  is_alergic?: boolean;
  /** Type of dessert */
  dessert_type?: DessertType;
  /** Calories per serving */
  calories?: number;
}

// --- Read Schema ---
interface DessertRead extends ProductBaseRead, DessertBase {
  // Combines product base fields with dessert-specific fields
}

// --- In DB Schema ---
type DessertInDB = DessertRead;

// --- Extended Response ---
interface DessertWithDetails extends DessertRead {
  /** Allergen warning message */
  alergen_warning?: string;
  /** Vegan status message */
  vegan_warning?: string;
}

// --- Dessert Summary (for lists) ---
interface DessertSummary {
  /** Unique dessert identifier */
  id: number;
  /** Dessert name */
  name: string;
  /** Original price */
  price: string;
  /** Final price after discount */
  final_price: string;
  /** URL to dessert image */
  image_url: string;
  /** Type of dessert */
  dessert_type: DessertType;
  /** Whether it's vegan */
  is_vegan: boolean;
  /** Calories per serving */
  calories: number;
  /** Whether it's active */
  is_active: boolean;
}

// Export all interfaces
export type {
  DessertType,
  DessertBase,
  DessertCreate,
  DessertUpdate,
  DessertRead,
  DessertInDB,
  DessertWithDetails,
  DessertSummary,
};
