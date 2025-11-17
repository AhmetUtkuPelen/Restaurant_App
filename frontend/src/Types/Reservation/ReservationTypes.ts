// --- Enums ---
type ReservationStatus = "PENDING" | "CONFIRMED" | "CANCELLED" | "COMPLETED";

// --- Base Types ---
interface ReservationBase {
  /** Table ID for the reservation */
  table_id: number;
  /** Date and time of the reservation */
  reservation_time: string; // ISO datetime string
  /** Number of guests (1-20) */
  number_of_guests: number;
  /** Special requests or notes (max 500 chars) */
  special_requests?: string | null;
}

// --- Create Schema ---
type ReservationCreate = ReservationBase;

// --- Update Schema ---
interface ReservationUpdate {
  /** Table ID for the reservation */
  table_id?: number;
  /** Date and time of the reservation */
  reservation_time?: string;
  /** Number of guests (1-20) */
  number_of_guests?: number;
  /** Reservation status */
  status?: ReservationStatus;
  /** Special requests or notes (max 500 chars) */
  special_requests?: string | null;
}

// --- Response Schemas ---
interface ReservationRead extends ReservationBase {
  /** Unique reservation identifier */
  id: number;
  /** User ID who made the reservation */
  user_id: number;
  /** Current status of the reservation */
  status: ReservationStatus;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** List of payment IDs associated with this reservation */
  payments: number[];
}

interface ReservationInDB extends ReservationRead {
  /** Deletion timestamp (if soft-deleted) */
  deleted_at?: string | null;
}

// --- Extended Response with Relations ---
interface ReservationWithRelations extends Omit<ReservationRead, "payments"> {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
  /** Table information */
  table?: {
    id: number;
    table_number: string;
    capacity: number;
    location: string;
  };
  /** Payment information */
  payments?: Array<{
    id: number;
    amount: number;
    status: string;
    created_at: string;
  }>;
}

// Export all interfaces
export type {
  ReservationStatus,
  ReservationBase,
  ReservationCreate,
  ReservationUpdate,
  ReservationRead,
  ReservationInDB,
  ReservationWithRelations,
};
