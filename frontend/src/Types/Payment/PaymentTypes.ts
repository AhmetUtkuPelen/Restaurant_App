// --- Enums ---
type PaymentStatus =
  | "PENDING"
  | "SUCCESS"
  | "FAILURE"
  | "CANCELLED"
  | "REFUNDED";

// --- Base Types ---
interface CardInfo {
  /** Last 4 digits of the card */
  last_four?: string | null;
  /** Card family (e.g., 'Bonus', 'Maximum') */
  family?: string | null;
  /** Card association (e.g., 'VISA', 'MASTER_CARD') */
  association?: string | null;
  /** Card type (e.g., 'CREDIT_CARD', 'DEBIT_CARD') */
  type?: string | null;
}

// --- Create Schema ---
interface PaymentCreate {
  /** Order IDs to pay for */
  order_ids?: number[];
  /** Reservation ID to pay for */
  reservation_id?: number | null;
  /** Payment amount */
  amount: string; // Decimal as string
  /** Currency code */
  currency?: string;
  /** Number of installments (1-12) */
  installment?: number;
  /** User's IP address (required by Iyzico) */
  ip_address: string;
  /** Optional metadata */
  metadata?: Record<string, unknown> | null;
}

// --- Update Schema ---
interface PaymentUpdate {
  /** Payment status */
  status?: PaymentStatus;
  /** Provider payment ID */
  provider_payment_id?: string | null;
  /** Provider payment token */
  provider_payment_token?: string | null;
  /** Fraud detection status */
  fraud_status?: number | null;
  /** Last 4 digits of card */
  card_last_four?: string | null;
  /** Card family */
  card_family?: string | null;
  /** Card association */
  card_association?: string | null;
  /** Card type */
  card_type?: string | null;
}

// --- Response Schemas ---
interface PaymentRead {
  /** Unique payment identifier */
  id: number;
  /** User ID who made the payment */
  user_id: number;
  /** Reservation ID (if paying for reservation) */
  reservation_id?: number | null;
  /** Payment amount */
  amount: string; // Decimal as string
  /** Currency code */
  currency: string;
  /** Payment status */
  status: PaymentStatus;
  /** Payment provider (e.g., 'iyzico') */
  provider?: string | null;
  /** Provider's payment ID */
  provider_payment_id?: string | null;
  /** Conversation ID for tracking */
  conversation_id?: string | null;
  /** Number of installments */
  installment: number;
  /** Fraud detection status */
  fraud_status?: number | null;
  /** Card information */
  card_info?: CardInfo | null;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** Order IDs associated with this payment */
  order_ids: number[];
}

interface PaymentInDB extends PaymentRead {
  /** Provider payment token (sensitive) */
  provider_payment_token?: string | null;
  /** Payment group */
  payment_group?: string | null;
  /** User's IP address */
  ip_address?: string | null;
  /** Basket ID reference */
  basket_id?: string | null;
  /** Payment metadata */
  metadata?: Record<string, unknown> | null;
}

// --- Extended Response with Relations ---
interface PaymentWithUser extends PaymentRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
}

interface PaymentWithOrders extends PaymentRead {
  /** Order information */
  orders?: Array<{
    id: number;
    status: string;
    total_amount: string;
    created_at: string;
  }>;
}

interface PaymentWithReservation extends PaymentRead {
  /** Reservation information */
  reservation?: {
    id: number;
    table_id: number;
    reservation_time: string;
    number_of_guests: number;
    status: string;
  };
}

interface PaymentWithRelations extends PaymentRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
  /** Order information */
  orders?: Array<{
    id: number;
    status: string;
    total_amount: string;
    created_at: string;
  }>;
  /** Reservation information */
  reservation?: {
    id: number;
    table_id: number;
    reservation_time: string;
    number_of_guests: number;
    status: string;
  };
}

// --- Payment Operations ---
interface PaymentRequest {
  /** Payment amount */
  amount: string;
  /** Currency (default: TRY) */
  currency?: string;
  /** Number of installments */
  installment?: number;
  /** Order IDs to pay for */
  order_ids?: number[];
  /** Reservation ID to pay for */
  reservation_id?: number;
  /** User's IP address */
  ip_address: string;
}

interface PaymentResponse {
  /** Payment ID */
  payment_id: number;
  /** Payment status */
  status: PaymentStatus;
  /** Provider payment URL (for redirect) */
  payment_url?: string;
  /** Provider payment token */
  payment_token?: string;
  /** Conversation ID */
  conversation_id?: string;
  /** Error message (if failed) */
  error_message?: string;
}

// --- Payment Statistics ---
interface PaymentStats {
  /** Total payments count */
  total_payments: number;
  /** Total amount processed */
  total_amount: string; // Decimal as string
  /** Successful payments count */
  successful_payments: number;
  /** Failed payments count */
  failed_payments: number;
  /** Success rate percentage */
  success_rate: number;
  /** Payments by status */
  payments_by_status: Record<PaymentStatus, number>;
  /** Average payment amount */
  average_amount: string; // Decimal as string
}

// --- Admin Operations ---
interface PaymentFilters {
  /** Filter by status */
  status?: PaymentStatus;
  /** Filter by user ID */
  user_id?: number;
  /** Filter by provider */
  provider?: string;
  /** Filter by date range (start) */
  date_from?: string;
  /** Filter by date range (end) */
  date_to?: string;
  /** Filter by minimum amount */
  min_amount?: number;
  /** Filter by maximum amount */
  max_amount?: number;
}

interface RefundRequest {
  /** Payment ID to refund */
  payment_id: number;
  /** Refund amount (partial refund if less than original) */
  amount?: string;
  /** Reason for refund */
  reason?: string;
}

// Export all interfaces
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
