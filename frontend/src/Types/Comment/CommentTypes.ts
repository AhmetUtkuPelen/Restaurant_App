// --- Base Types ---
interface CommentBase {
  /** Product ID the comment is for */
  product_id: number;
  /** Comment content (1-1000 characters) */
  content: string;
  /** Optional rating (1-5 stars) */
  rating?: number | null;
}

// --- Create Schema ---
interface CommentCreate {
  /** Product ID the comment is for */
  product_id: number;
  /** Comment content (1-1000 characters) */
  content: string;
  /** Optional rating (1-5 stars) */
  rating?: number | null;
}

// --- Update Schema ---
interface CommentUpdate {
  /** Comment content (1-1000 characters) */
  content?: string;
  /** Optional rating (1-5 stars) */
  rating?: number | null;
}

// --- Response Schemas ---
interface CommentRead extends CommentBase {
  /** Unique comment identifier */
  id: number;
  /** User ID who wrote the comment */
  user_id: number;
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** Whether the comment is active/visible */
  is_active: boolean;
}

interface CommentInDB extends CommentRead {
  /** Deletion timestamp (if soft-deleted) */
  deleted_at?: string | null;
}

// --- Extended Response with Relations ---
interface CommentWithUser extends CommentRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    image_url?: string | null;
  };
}

interface CommentWithProduct extends CommentRead {
  /** Product information */
  product?: {
    id: number;
    name: string;
    image_url?: string | null;
    category: string;
  };
}

interface CommentWithRelations extends CommentRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    image_url?: string | null;
  };
  /** Product information */
  product?: {
    id: number;
    name: string;
    image_url?: string | null;
    category: string;
  };
}

// --- Comment Statistics ---
interface CommentStats {
  /** Total number of comments */
  total_comments: number;
  /** Average rating */
  average_rating: number;
  /** Rating distribution */
  rating_distribution: {
    1: number;
    2: number;
    3: number;
    4: number;
    5: number;
  };
}

// --- Admin Operations ---
interface CommentModerationAction {
  /** Comment ID to moderate */
  comment_id: number;
  /** Action to take */
  action: "approve" | "reject" | "hide" | "delete";
  /** Optional reason for the action */
  reason?: string;
}

// Export all interfaces
export type {
  CommentBase,
  CommentCreate,
  CommentUpdate,
  CommentRead,
  CommentInDB,
  CommentWithUser,
  CommentWithProduct,
  CommentWithRelations,
  CommentStats,
  CommentModerationAction,
};
