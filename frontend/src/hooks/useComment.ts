import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";

// Types
export interface Comment {
  id: number;
  user_id: number;
  product_id: number;
  content: string;
  rating: number | null;
  created_at: string;
  updated_at: string | null;
  is_active: boolean;
  username?: string;
  product_name?: string;
}

export interface CommentCreate {
  product_id: number;
  content: string;
  rating?: number;
}

export interface CommentUpdate {
  content?: string;
  rating?: number;
}

export interface ProductCommentsResponse {
  product_id: number;
  product_name: string;
  total_comments: number;
  average_rating: number | null;
  skip: number;
  limit: number;
  comments: Comment[];
}

// Get comments for a product
export const useProductComments = (productId: number) => {
  return useQuery({
    queryKey: ["comments", "product", productId],
    queryFn: async () => {
      const response = await axiosInstance.get<ProductCommentsResponse>(
        `/comments/product/${productId}`
      );
      return response.data;
    },
    enabled: !!productId,
  });
};

// Get user's own comments
export const useMyComments = (includeInactive = false) => {
  return useQuery({
    queryKey: ["comments", "my", includeInactive],
    queryFn: async () => {
      const response = await axiosInstance.get<Comment[]>(
        `/comments/my-comments/all?include_inactive=${includeInactive}`
      );
      return response.data;
    },
  });
};

// Create comment
export const useCreateComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CommentCreate) => {
      const response = await axiosInstance.post("/comments/", data);
      return response.data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({
        queryKey: ["comments", "product", variables.product_id],
      });
      queryClient.invalidateQueries({ queryKey: ["comments", "my"] });
    },
  });
};

// Update comment
export const useUpdateComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async ({
      commentId,
      data,
    }: {
      commentId: number;
      data: CommentUpdate;
    }) => {
      const response = await axiosInstance.put(`/comments/${commentId}`, data);
      return response.data;
    },
    onSuccess: (data) => {
      queryClient.invalidateQueries({
        queryKey: ["comments", "product", data.comment.product_id],
      });
      queryClient.invalidateQueries({ queryKey: ["comments", "my"] });
    },
  });
};

// Delete comment (soft delete)
export const useDeleteComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (commentId: number) => {
      const response = await axiosInstance.delete(`/comments/${commentId}`);
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["comments"] });
    },
  });
};

// Permanently delete comment
export const usePermanentlyDeleteComment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (commentId: number) => {
      const response = await axiosInstance.delete(
        `/comments/${commentId}/permanent`
      );
      return response.data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["comments"] });
    },
  });
};
