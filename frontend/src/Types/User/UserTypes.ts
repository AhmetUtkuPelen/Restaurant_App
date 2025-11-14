// --- Base Types ---
interface UserBase {
  /** Username, must be 3-50 characters, alphanumeric and underscores only */
  username: string;
  /** User's email address */
  email: string;
  /** Phone number in international format, e.g., +1234567890 */
  phone?: string | null;
  /** User's physical address (5-200 characters) */
  address: string;
  /** URL to user's profile picture */
  profile_picture?: string | null;
}

// --- Schemas for Authentication & Creation ---
interface UserCreate extends Omit<UserBase, 'phone' | 'profile_picture'> {
  /** Phone number in international format (required for creation) */
  phone: string;
  /** URL to user's profile picture */
  profile_picture?: string;
  /** User's password. Must be at least 8 characters long and strong */
  password: string;
  /** Password confirmation, must match password */
  password_confirm: string;
}

interface UserLogin {
  /** Username or email address for login */
  identifier: string;
  /** User's password */
  password: string;
}

// --- Schemas for Updates ---
interface UserUpdate {
  /** Username, must be 3-50 characters, alphanumeric and underscores only */
  username?: string;
  /** User's email address */
  email?: string;
  /** Phone number in international format, e.g., +1234567890 */
  phone?: string;
  /** User's physical address (5-200 characters) */
  address?: string;
  /** URL to user's profile picture */
  profile_picture?: string;
}

interface PasswordUpdate {
  /** User's current password */
  current_password: string;
  /** New password, must be strong */
  new_password: string;
  /** New password confirmation */
  new_password_confirm: string;
}

// --- API Response Schemas ---
type UserRole = 'user' | 'admin' | 'moderator';

interface UserResponse extends UserBase {
  /** Unique user identifier */
  id: number;
  /** User's role in the system */
  role: UserRole;
  /** Whether the user account is active */
  is_active: boolean;
  /** Whether the user's email has been verified */
  is_verified: boolean;
  /** Account creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at: string;
  /** Account deletion timestamp (if soft-deleted) */
  deleted_at?: string | null;
}

// --- Related Data Interfaces ---
interface Reservation {
  id: number;
  product_id: number;
  quantity: number;
  created_at: string;
  updated_at: string;
  status: 'pending' | 'confirmed' | 'cancelled' | 'completed';
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

interface UserWithRelationsResponse extends UserResponse {
  /** List of user's reservations */
  reservations: Reservation[];
  /** Items in user's shopping cart */
  cart_items: CartItem[];
  /** User's favorite products */
  favorite_products: FavoriteProduct[];
}

// --- Token Schemas ---
interface Token {
  /** JWT access token for API authentication */
  access_token: string;
  /** Refresh token for obtaining new access tokens */
  refresh_token: string;
  /** Type of token, typically 'bearer' */
  token_type: 'bearer' | string;
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

// --- Admin Schemas ---
interface UserAdminCreate extends Omit<UserCreate, 'role' | 'is_active' | 'is_verified'> {
  /** User's role in the system */
  role?: UserRole;
  /** Whether the user account is active */
  is_active?: boolean;
  /** Whether the user's email has been verified */
  is_verified?: boolean;
}

interface UserAdminUpdate extends Partial<Omit<UserUpdate, 'role' | 'is_active' | 'is_verified'>> {
  /** User's role in the system */
  role?: UserRole;
  /** Whether the user account is active */
  is_active?: boolean;
  /** Whether the user's email has been verified */
  is_verified?: boolean;
  /** New password (if changing) */
  password?: string;
}

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
  UserCreate,
  UserLogin,
  UserUpdate,
  PasswordUpdate,
  UserRole,
  UserResponse,
  UserWithRelationsResponse,
  Token,
  TokenData,
  RefreshTokenRequest,
  UserAdminCreate,
  UserAdminUpdate,
  RequestEmailSchema,
  ResetPasswordSchema,
  VerifyEmailSchema
};