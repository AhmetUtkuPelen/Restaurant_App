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