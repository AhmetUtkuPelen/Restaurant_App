// Enums \\
type PaymentStatus =
  | "PENDING"
  | "SUCCESS"
  | "FAILURE"
  | "CANCELLED"
  | "REFUNDED";

// Base Types \\
interface CardInfo {
  last_four?: string | null;
  family?: string | null;
  association?: string | null;
  type?: string | null;
}

// Create Schema \\
interface PaymentCreate {
  order_ids?: number[];
  reservation_id?: number | null;
  amount: string;
  currency?: string;
  installment?: number;
  ip_address: string;
  metadata?: Record<string, unknown> | null;
}

// Update Schema \\
interface PaymentUpdate {
  status?: PaymentStatus;
  provider_payment_id?: string | null;
  provider_payment_token?: string | null;
  fraud_status?: number | null;
  card_last_four?: string | null;
  card_family?: string | null;
  card_association?: string | null;
  card_type?: string | null;
}

// --- Response Schemas ---
interface PaymentRead {
  id: number;
  user_id: number;
  reservation_id?: number | null;
  amount: string;
  currency: string;
  status: PaymentStatus;
  provider?: string | null;
  provider_payment_id?: string | null;
  conversation_id?: string | null;
  installment: number;
  fraud_status?: number | null;
  card_info?: CardInfo | null;
  created_at: string;
  updated_at?: string | null;
  order_ids: number[];
}

interface PaymentInDB extends PaymentRead {
  provider_payment_token?: string | null;
  payment_group?: string | null;
  ip_address?: string | null;
  basket_id?: string | null;
  metadata?: Record<string, unknown> | null;
}

interface PaymentWithUser extends PaymentRead {
  // User information \\
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
}

interface PaymentWithOrders extends PaymentRead {
  // Order information \\
  orders?: Array<{
    id: number;
    status: string;
    total_amount: string;
    created_at: string;
  }>;
}

interface PaymentWithReservation extends PaymentRead {
  // Reservation information \\
  reservation?: {
    id: number;
    table_id: number;
    reservation_time: string;
    number_of_guests: number;
    status: string;
  };
}

interface PaymentWithRelations extends PaymentRead {
  // User information \\
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
  // Order information \\
  orders?: Array<{
    id: number;
    status: string;
    total_amount: string;
    created_at: string;
  }>;
  // Reservation information \\
  reservation?: {
    id: number;
    table_id: number;
    reservation_time: string;
    number_of_guests: number;
    status: string;
  };
}

// Payment Operations \\
interface PaymentRequest {
  amount: string;
  currency?: string;
  installment?: number;
  order_ids?: number[];
  reservation_id?: number;
  ip_address: string;
}

interface PaymentResponse {
  payment_id: number;
  status: PaymentStatus;
  payment_url?: string;
  payment_token?: string;
  conversation_id?: string;
  error_message?: string;
}

interface PaymentStats {
  total_payments: number;
  total_amount: string;
  successful_payments: number;
  failed_payments: number;
  success_rate: number;
  payments_by_status: Record<PaymentStatus, number>;
  average_amount: string;
}

// Admin Operations \\
interface PaymentFilters {
  status?: PaymentStatus;
  user_id?: number;
  provider?: string;
  date_from?: string;
  date_to?: string;
  min_amount?: number;
  max_amount?: number;
}

interface RefundRequest {
  payment_id: number;
  amount?: string;
  reason?: string;
}

export type {
  PaymentStatus,
  CardInfo,
  PaymentCreate,
  PaymentUpdate,
  PaymentRead,
  PaymentInDB,
  PaymentWithUser,
  PaymentWithOrders,
  PaymentWithReservation,
  PaymentWithRelations,
  PaymentRequest,
  PaymentResponse,
  PaymentStats,
  PaymentFilters,
  RefundRequest,
};