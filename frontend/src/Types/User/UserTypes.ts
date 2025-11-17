import type { CartRead } from "../Cart/CartTypes";

// --- Base Types ---
interface UserBase {
  /** Username, must be 3-20 characters, alphanumeric and underscores only */
  username: string;
  /** User's email address */
  email: string;
  /** Phone number in international format, e.g., +90XXXXXXXXXX or 10 digits */
  phone?: string | null;
  /** User's physical address (min 5 characters) */
  address?: string | null;
  /** URL to user's profile picture */
  image_url?: string | null;
  /** User's role in the system */
  role?: UserRole;
}

// --- Enums ---
type UserRole = "USER" | "STAFF" | "ADMIN";

// --- Authentication Schemas ---
interface UserLogin {
  /** Username for login */
  username: string;
  /** User's password */
  password: string;
}

interface UserRegister extends UserBase {
  /** User's password. Must be at least 8 characters long and strong */
  password: string;
}

// --- Update Schemas ---
interface UserUpdate {
  /** Username, must be 3-20 characters, alphanumeric and underscores only */
  username?: string;
  /** User's email address */
  email?: string;
  /** URL to user's profile picture */
  image_url?: string;
  /** Phone number in international format */
  phone?: string;
  /** User's physical address */
  address?: string;
  /** User's password (optional for updates) */
  password?: string;
}

interface UserProfileUpdate {
  /** Username, must be 3-20 characters, alphanumeric and underscores only */
  username?: string;
  /** User's email address */
  email?: string;
  /** User's password (optional for updates) */
  password?: string;
  /** URL to user's profile picture */
  image_url?: string;
  /** Phone number in international format */
  phone?: string;
  /** User's physical address */
  address?: string;
}

// --- Admin Schemas ---
interface AdminCreateUser {
  /** Username, must be 3-20 characters */
  username: string;
  /** User's email address */
  email: string;
  /** User's password */
  password: string;
  /** User's role in the system */
  role?: UserRole;
  /** URL to user's profile picture */
  image_url?: string;
  /** Phone number in international format */
  phone?: string;
  /** User's physical address */
  address?: string;
  /** Whether the user account is active */
  is_active?: boolean;
}

interface AdminUpdateUser {
  /** Username, must be 3-20 characters */
  username?: string;
  /** User's email address */
  email?: string;
  /** User's role in the system */
  role?: UserRole;
  /** URL to user's profile picture */
  image_url?: string;
  /** Phone number in international format */
  phone?: string;
  /** User's physical address */
  address?: string;
  /** Whether the user account is active */
  is_active?: boolean;
  /** User's password (admin can reset) */
  password?: string;
}

// --- Response Schemas ---
interface UserInDbBase extends UserBase {
  /** Unique user identifier */
  id: number;
  /** Whether the user account is active */
  is_active: boolean;
  /** Account creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** Account deletion timestamp (if soft-deleted) */
  deleted_at?: string | null;
  /** User's role in the system */
  role: UserRole;
  /** List of favourite product IDs */
  favourite_products: number[];
  /** List of order IDs */
  orders: number[];
  /** List of comment IDs */
  comments: number[];
  /** User's cart information */
  cart?: CartRead | null;
  /** List of reservation IDs */
  reservations: number[];
  /** List of payment IDs */
  payments: number[];
}

type User = UserInDbBase;

interface UserInDb extends UserInDbBase {
  /** Hashed password (internal use only) */
  hashed_password: string;
}

interface UserProfileRead {
  /** Unique user identifier */
  id: number;
  /** Username */
  username: string;
  /** User's email address */
  email: string;
  /** URL to user's profile picture */
  image_url?: string | null;
  /** Phone number */
  phone?: string | null;
  /** User's address */
  address?: string | null;
  /** User's role as string */
  role: string;
  /** Whether the user account is active */
  is_active: boolean;
  /** Account creation timestamp */
  created_at: string;
  /** List of favourite product IDs */
  favourite_products: number[];
  /** List of order IDs */
  orders: number[];
  /** List of comment IDs */
  comments: number[];
  /** User's cart information */
  cart?: CartRead | null;
  /** List of reservation IDs */
  reservations: number[];
  /** List of payment IDs */
  payments: number[];
}

// --- Related Data Interfaces ---
interface Reservation {
  id: number;
  product_id: number;
  quantity: number;
  created_at: string;
  updated_at: string;
  status: "pending" | "confirmed" | "cancelled" | "completed";
}

interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  added_at: string;
  updated_at: string;
  size?: string;
  color?: string;
}

interface FavoriteProduct {
  id: number;
  product_id: number;
  added_at: string;
  product_name: string;
  product_image?: string;
  price: number;
}

interface UserWithRelationsResponse
  extends Omit<User, "reservations" | "favourite_products" | "cart"> {
  /** List of user's reservations with full details */
  reservations: Reservation[];
  /** Items in user's shopping cart */
  cart_items: CartItem[];
  /** User's favorite products with full details */
  favorite_products: FavoriteProduct[];
}

// --- Token Schemas ---
interface Token {
  /** JWT access token for API authentication */
  access_token: string;
  /** Refresh token for obtaining new access tokens */
  refresh_token: string;
  /** Type of token, typically 'bearer' */
  token_type: "bearer" | string;
  /** User information returned with token */
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
  };
}

interface TokenData {
  /** Subject (usually user ID) */
  sub: string;
  /** Token type */
  token_type?: string;
  /** User's role */
  role?: UserRole;
  /** JWT ID */
  jti?: string;
  /** Expiration timestamp */
  exp?: number;
  /** Issued at timestamp */
  iat?: number;
}

interface RefreshTokenRequest {
  /** Refresh token */
  refresh_token: string;
}

// Note: UserAdminCreate and UserAdminUpdate are already defined above
// These duplicate definitions are removed to avoid conflicts

// --- Email & Password Operations ---
interface RequestEmailSchema {
  /** Email address for password reset or verification */
  email: string;
}

interface ResetPasswordSchema {
  /** The password reset token sent via email */
  token: string;
  /** New password, must be strong */
  new_password: string;
  /** New password confirmation */
  new_password_confirm: string;
}

interface VerifyEmailSchema {
  /** The email verification token sent via email */
  token: string;
}

// Export all interfaces
export type {
  UserBase,
  UserRole,
  UserLogin,
  UserRegister,
  UserUpdate,
  UserProfileUpdate,
  AdminCreateUser,
  AdminUpdateUser,
  UserInDbBase,
  User,
  UserInDb,
  UserProfileRead,
  UserWithRelationsResponse,
  Reservation,
  CartItem,
  FavoriteProduct,
  Token,
  TokenData,
  RefreshTokenRequest,
  RequestEmailSchema,
  ResetPasswordSchema,
  VerifyEmailSchema,
};
