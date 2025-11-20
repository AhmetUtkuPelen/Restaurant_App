import type { CartRead } from "../Cart/CartTypes";

// Base Types \\
interface UserBase {
  username: string;
  email: string;
  phone?: string | null;
  address?: string | null;
  image_url?: string | null;
  role?: UserRole;
}

// Enums \\
type UserRole = "USER" | "STAFF" | "ADMIN";

// Authentication Schemas \\
interface UserLogin {
  username: string;
  password: string;
}

interface UserRegister extends UserBase {
  password: string;
}

// Update Schemas \\
interface UserUpdate {
  username?: string;
  email?: string;
  image_url?: string;
  phone?: string;
  address?: string;
  password?: string;
}

interface UserProfileUpdate {
  username?: string;
  email?: string;
  password?: string;
  image_url?: string;
  phone?: string;
  address?: string;
}

// Admin Schemas \\
interface AdminCreateUser {
  username: string;
  email: string;
  password: string;
  role?: UserRole;
  image_url?: string;
  phone?: string;
  address?: string;
  is_active?: boolean;
}

interface AdminUpdateUser {
  username?: string;
  email?: string;
  role?: UserRole;
  image_url?: string;
  phone?: string;
  address?: string;
  is_active?: boolean;
  password?: string;
}

// Response Schemas \\
interface UserInDbBase extends UserBase {
  id: number;
  is_active: boolean;
  created_at: string;
  updated_at?: string | null;
  deleted_at?: string | null;
  role: UserRole;
  favourite_products: number[];
  orders: number[];
  comments: number[];
  cart?: CartRead | null;
  reservations: number[];
  payments: number[];
}

type User = UserInDbBase;

interface UserInDb extends UserInDbBase {
  hashed_password: string;
}

interface UserProfileRead {
  id: number;
  username: string;
  email: string;
  image_url?: string | null;
  phone?: string | null;
  address?: string | null;
  role: string;
  is_active: boolean;
  created_at: string;
  favourite_products: number[];
  orders: number[];
  comments: number[];
  cart?: CartRead | null;
  reservations: number[];
  payments: number[];
}

// User Related Data Interfaces \\
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
  reservations: Reservation[];
  cart_items: CartItem[];
  favorite_products: FavoriteProduct[];
}

// Token Schemas \\
interface Token {
  access_token: string;
  refresh_token: string;
  token_type: "bearer" | string;
  user: {
    id: number;
    username: string;
    email: string;
    role: string;
  };
}

interface TokenData {
  sub: string;
  token_type?: string;
  role?: UserRole;
  jti?: string;
  exp?: number;
  iat?: number;
}

interface RefreshTokenRequest {
  refresh_token: string;
}

// Email & Password Operations \\
interface RequestEmailSchema {
  email: string;
}

interface ResetPasswordSchema {
  token: string;
  new_password: string;
  new_password_confirm: string;
}

interface VerifyEmailSchema {
  token: string;
}

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

export interface UserProfile {
  id: number;
  username: string;
  email: string;
  image_url: string | null;
  phone: string | null;
  address: string | null;
  role: string;
  is_active: boolean;
  created_at: string;
  favourite_products: number[];
  orders: number[];
  comments: number[];
  cart: Record<string, unknown> | null;
  reservations: number[];
  payments: number[];
}

export interface UpdateProfileData {
  username?: string;
  email?: string;
  image_url?: string;
  phone?: string;
  address?: string;
}

export interface ChangePasswordData {
  current_password: string;
  new_password: string;
}