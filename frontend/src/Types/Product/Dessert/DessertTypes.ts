import type {
  ProductBaseCreate,
  ProductBaseUpdate,
  ProductBaseRead,
} from "../BaseProduct/BaseProductTypes";

// Enums \\
type DessertType =
  | "CAKE"
  | "PIE"
  | "PUDDING"
  | "ICE_CREAM"
  | "PASTRY"
  | "COOKIE"
  | "OTHER";

// Base Types \\
interface DessertBase {
  is_vegan: boolean;
  is_alergic: boolean;
  dessert_type: DessertType;
  calories: number;
}

// Create Schema \\
interface DessertCreate extends ProductBaseCreate, DessertBase {
  category: "dessert";
}

// Update Schema \\
interface DessertUpdate extends ProductBaseUpdate {
  is_vegan?: boolean;
  is_alergic?: boolean;
  dessert_type?: DessertType;
  calories?: number;
}

// Read Schema \\
interface DessertRead extends ProductBaseRead, DessertBase { }

// In DB Schema \\
type DessertInDB = DessertRead;

// Extended Response \\
interface DessertWithDetails extends DessertRead {
  alergen_warning?: string;
  vegan_warning?: string;
}

// Dessert Summary (for lists) \\
interface DessertSummary {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  dessert_type: DessertType;
  is_vegan: boolean;
  calories: number;
  is_active: boolean;
}

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