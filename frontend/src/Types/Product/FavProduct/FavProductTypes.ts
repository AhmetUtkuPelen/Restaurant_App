// Base Types \\
// interface FavouriteProductBase {
//   user_id: number;
//   product_id: number;
// }

// // Create Schema \\
// interface FavouriteProductCreate {
//   product_id: number;
// }

// // Read Schema \\
// interface FavouriteProductRead extends FavouriteProductBase {
//   id: number;
//   created_at: string;
//   updated_at?: string | null;
// }

// // In DB Schema \\
// interface FavouriteProductInDB extends FavouriteProductRead {
//   deleted_at?: string | null;
// }

// // Extended Response with Relations \\
// interface FavouriteProductWithUser extends FavouriteProductRead {
//   user?: {
//     id: number;
//     username: string;
//     email: string;
//   };
// }

// interface FavouriteProductWithProduct extends FavouriteProductRead {
//   // Product information \\
//   product?: {
//     id: number;
//     name: string;
//     category: string;
//     price: string;
//     final_price: string;
//     image_url: string;
//     is_active: boolean;
//   };
// }

// interface FavouriteProductWithRelations extends FavouriteProductRead {
//   // User information \\
//   user?: {
//     id: number;
//     username: string;
//     email: string;
//   };
//   // Product information \\
//   product?: {
//     id: number;
//     name: string;
//     category: string;
//     price: string;
//     final_price: string;
//     image_url: string;
//     is_active: boolean;
//   };
// }

// // User's Favorite Products List \\
// interface UserFavoritesList {
//   total: number;
//   favorites: FavouriteProductWithProduct[];
// }

// export type {
//   FavouriteProductBase,
//   FavouriteProductCreate,
//   FavouriteProductRead,
//   FavouriteProductInDB,
//   FavouriteProductWithUser,
//   FavouriteProductWithProduct,
//   FavouriteProductWithRelations,
//   UserFavoritesList
// };


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