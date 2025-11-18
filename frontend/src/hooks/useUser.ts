import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";

// Types
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

// Get current user profile
export const useUserProfile = () => {
  return useQuery({
    queryKey: ["user", "profile"],
    queryFn: async () => {
      const response = await axiosInstance.get<UserProfile>("/users/me");
      return response.data;
    },
  });
};

// Update user profile
export const useUpdateProfile = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: UpdateProfileData) => {
      const response = await axiosInstance.put("/users/me", data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};

// Change password
export const useChangePassword = () => {
  return useMutation({
    mutationFn: async (data: ChangePasswordData) => {
      const response = await axiosInstance.post("/users/me/change-password", {
        current_password: data.current_password,
        new_password: data.new_password,
      });
      return response.data;
    },
  });
};
