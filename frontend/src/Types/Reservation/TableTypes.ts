// --- Enums ---
type TableLocation = 'MAIN_DINING_ROOM' | 'PRIVATE_ROOM' | 'OUTDOOR_TERRACE' | 'BAR_AREA' | 'VIP_SECTION';

// --- Base Types ---
interface TableBase {
  /** Table number/identifier (1-10 chars) */
  table_number: string;
  /** Maximum number of people the table can seat (1-20) */
  capacity: number;
  /** Location of the table in the restaurant */
  location: TableLocation;
  /** Whether the table is currently available for reservations */
  is_available: boolean;
}

// --- Create Schema ---
type TableCreate = TableBase;

// --- Update Schema ---
interface TableUpdate {
  /** Table number/identifier (1-10 chars) */
  table_number?: string;
  /** Maximum number of people the table can seat (1-20) */
  capacity?: number;
  /** Location of the table in the restaurant */
  location?: TableLocation;
  /** Whether the table is currently available for reservations */
  is_available?: boolean;
}

// --- Response Schemas ---
interface TableRead extends TableBase {
  /** Unique table identifier */
  id: number;
}

type TableInDB = TableRead;

// --- Extended Response with Relations ---
interface TableWithReservations extends TableRead {
  /** Current and upcoming reservations for this table */
  reservations?: Array<{
    id: number;
    user_id: number;
    reservation_time: string;
    number_of_guests: number;
    status: string;
  }>;
  /** Whether table is currently occupied */
  is_occupied?: boolean;
  /** Next available time slot */
  next_available?: string | null;
}

// Export all interfaces
export type {
  TableLocation,
  TableBase,
  TableCreate,
  TableUpdate,
  TableRead,
  TableInDB,
  TableWithReservations
};