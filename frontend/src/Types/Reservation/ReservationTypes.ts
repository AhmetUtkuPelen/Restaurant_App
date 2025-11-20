export interface ReservationCreate {
  table_id: number;
  reservation_time: string;
  number_of_guests: number;
  special_requests?: string;
}

export interface Reservation {
  id: number;
  user_id: number;
  table_id: number;
  reservation_time: string;
  number_of_guests: number;
  special_requests: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}