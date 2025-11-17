import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface FavouriteProduct {
  id: number;
  name: string;
  price: string;
  final_price: string;
  image_url: string;
  category: string;
  description?: string;
}

interface FavouriteProductState {
  favourites: FavouriteProduct[];
  addToFavourites: (product: FavouriteProduct) => void;
  removeFromFavourites: (productId: number) => void;
  isFavourite: (productId: number) => boolean;
  clearFavourites: () => void;
  getTotalFavourites: () => number;
}

export const useFavouriteStore = create<FavouriteProductState>()(
  persist(
    (set, get) => ({
      favourites: [],

      addToFavourites: (product) => {
        set((state) => {
          const exists = state.favourites.find((fav) => fav.id === product.id);
          
          if (exists) {
            // If already in favourites, don't add again
            return state;
          }

          return {
            favourites: [...state.favourites, product],
          };
        });
      },

      removeFromFavourites: (productId) => {
        set((state) => ({
          favourites: state.favourites.filter((fav) => fav.id !== productId),
        }));
      },

      isFavourite: (productId) => {
        return get().favourites.some((fav) => fav.id === productId);
      },

      clearFavourites: () => {
        set({ favourites: [] });
      },

      getTotalFavourites: () => {
        return get().favourites.length;
      },
    }),
    {
      name: "favourites-storage", // localStorage key
    }
  )
);
