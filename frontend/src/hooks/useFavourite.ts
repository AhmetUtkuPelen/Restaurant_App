import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";

// Types
export interface FavouriteProduct {
  id: number;
  user_id: number;
  product_id: number;
  created_at: string;
  product: {
    id: number;
    name: string;
    price: string;
    final_price: string;
    image_url: string;
    category: string;
    description?: string;
  };
}

export interface FavouriteProductCreate {
  product_id: number;
}

// Get user's favourite products
export const useMyFavourites = () => {
  return useQuery({
    queryKey: ["favourites", "my"],
    queryFn: async () => {
      const response = await axiosInstance.get<FavouriteProduct[]>("/favourites/my-favourites");
      return response.data;
    },
  });
};

// Add product to favourites
export const useAddFavourite = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: FavouriteProductCreate) => {
      const response = await axiosInstance.post("/favourites/", data);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["favourites"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};

// Remove product from favourites
export const useRemoveFavourite = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (favouriteId: number) => {
      const response = await axiosInstance.delete(`/favourites/${favouriteId}`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["favourites"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};

// Clear all favourites
export const useClearFavourites = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async () => {
      const response = await axiosInstance.delete("/favourites/");
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["favourites"] });
      queryClient.invalidateQueries({ queryKey: ["user", "profile"] });
    },
  });
};
