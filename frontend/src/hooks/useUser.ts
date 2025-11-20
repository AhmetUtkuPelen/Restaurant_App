import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";
import type { ChangePasswordData, UpdateProfileData, UserProfile } from "@/Types/User/UserTypes";

// Get current user profile \\
export const useUserProfile = () => {
  return useQuery({
    queryKey: ["user", "profile"],
    queryFn: async () => {
      const response = await axiosInstance.get<UserProfile>("/users/me");
      return response.data;
    },
  });
};

// Update user profile \\
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

// Change password \\
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