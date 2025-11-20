import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";
import type { ReservationCreate  } from "@/Types/Reservation/ReservationTypes";
import type { Table } from "@/Types/Reservation/TableTypes";
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

// Fetch all available tables \\
export const useTables = () => {
  return useQuery({
    queryKey: ["tables"],
    queryFn: async () => {
      const response = await axiosInstance.get<Table[]>("/tables");
      return response.data;
    },
  });
};

// Fetch available tables by criteria \\
export const useAvailableTables = (minCapacity?: number, location?: string) => {
  return useQuery({
    queryKey: ["tables", "available", minCapacity, location],
    queryFn: async () => {
      const params = new URLSearchParams();
      if (minCapacity) params.append("min_capacity", minCapacity.toString());
      if (location) params.append("location", location);
      
      const response = await axiosInstance.get<Table[]>(
        `/tables/available/search?${params.toString()}`
      );
      return response.data;
    },
    enabled: !!minCapacity,
  });
};

// Create a new reservation \\
export const useCreateReservation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: ReservationCreate) => {
      const response = await axiosInstance.post<{ message: string; reservation: Reservation }>("/reservations", data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reservations"] });
      queryClient.invalidateQueries({ queryKey: ["tables"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};

// Fetch user's reservations \\
export const useMyReservations = () => {
  return useQuery({
    queryKey: ["reservations", "my"],
    queryFn: async () => {
      const response = await axiosInstance.get<Reservation[]>("/reservations/my-reservations");
      return response.data;
    },
  });
};

// Update a reservation \\
export const useUpdateReservation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({ reservationId, data }: { reservationId: number; data: Partial<ReservationCreate> }) => {
      const response = await axiosInstance.put(`/reservations/${reservationId}`, data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reservations"] });
      queryClient.invalidateQueries({ queryKey: ["tables"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};

// Cancel a reservation \\
export const useCancelReservation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (reservationId: number) => {
      const response = await axiosInstance.post(`/reservations/${reservationId}/cancel`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reservations"] });
      queryClient.invalidateQueries({ queryKey: ["tables"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};