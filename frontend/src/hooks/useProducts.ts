import { useQuery } from "@tanstack/react-query";
import { axiosInstance } from "@/Axios/Axios";
import type {
  DessertRead,
  DonerRead,
  DrinkRead,
  KebabRead,
  SaladRead,
  ProductBaseRead,
} from "@/Types/Product";

// Dessert Hooks \\
export const useDesserts = () => {
  return useQuery({
    queryKey: ["desserts"],
    queryFn: async () => {
      const response = await axiosInstance.get<{ desserts: DessertRead[] }>("/desserts");
      return response.data.desserts;
    },
  });
};

export const useDessert = (id: number) => {
  return useQuery({
    queryKey: ["desserts", id],
    queryFn: async () => {
      const response = await axiosInstance.get<DessertRead>(`/desserts/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};

// Doner Hooks \\
export const useDoners = () => {
  return useQuery({
    queryKey: ["doners"],
    queryFn: async () => {
      const response = await axiosInstance.get<{ doners: DonerRead[] }>("/doners");
      return response.data.doners;
    },
  });
};

export const useDoner = (id: number) => {
  return useQuery({
    queryKey: ["doners", id],
    queryFn: async () => {
      const response = await axiosInstance.get<DonerRead>(`/doners/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};

// Drink Hooks \\
export const useDrinks = () => {
  return useQuery({
    queryKey: ["drinks"],
    queryFn: async () => {
      const response = await axiosInstance.get<{ drinks: DrinkRead[] }>("/drinks");
      return response.data.drinks;
    },
  });
};

export const useDrink = (id: number) => {
  return useQuery({
    queryKey: ["drinks", id],
    queryFn: async () => {
      const response = await axiosInstance.get<DrinkRead>(`/drinks/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};

// Kebab Hooks \\
export const useKebabs = () => {
  return useQuery({
    queryKey: ["kebabs"],
    queryFn: async () => {
      const response = await axiosInstance.get<{ kebabs: KebabRead[] }>("/kebabs");
      return response.data.kebabs;
    },
  });
};

export const useKebab = (id: number) => {
  return useQuery({
    queryKey: ["kebabs", id],
    queryFn: async () => {
      const response = await axiosInstance.get<KebabRead>(`/kebabs/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};

// Salad Hooks \\
export const useSalads = () => {
  return useQuery({
    queryKey: ["salads"],
    queryFn: async () => {
      const response = await axiosInstance.get<{ salads: SaladRead[] }>("/salads");
      return response.data.salads;
    },
  });
};

export const useSalad = (id: number) => {
  return useQuery({
    queryKey: ["salads", id],
    queryFn: async () => {
      const response = await axiosInstance.get<SaladRead>(`/salads/${id}`);
      return response.data;
    },
    enabled: !!id,
  });
};

// All Products Hook \\
export const useAllProducts = () => {
  return useQuery({
    queryKey: ["products"],
    queryFn: async () => {
      const response = await axiosInstance.get<ProductBaseRead[]>("/products");
      return response.data;
    },
  });
};

export const useProduct = (id: number) => {
  return useQuery({
    queryKey: ["products", id],
    queryFn: async () => {
      const response = await axiosInstance.get<ProductBaseRead>(
        `/products/${id}`
      );
      return response.data;
    },
    enabled: !!id,
  });
};

// Home - Landing Page  Products Hook - fetches products from all categories with is_front_page=true \\
export const useFrontPageProducts = () => {
  return useQuery({
    queryKey: ["frontPageProducts"],
    queryFn: async () => {
      const [desserts, doners, drinks, kebabs, salads] = await Promise.all([
        axiosInstance.get<{ desserts: DessertRead[] }>("/desserts"),
        axiosInstance.get<{ doners: DonerRead[] }>("/doners"),
        axiosInstance.get<{ drinks: DrinkRead[] }>("/drinks"),
        axiosInstance.get<{ kebabs: KebabRead[] }>("/kebabs"),
        axiosInstance.get<{ salads: SaladRead[] }>("/salads"),
      ]);

      const allProducts: ProductBaseRead[] = [
        ...desserts.data.desserts,
        ...doners.data.doners,
        ...drinks.data.drinks,
        ...kebabs.data.kebabs,
        ...salads.data.salads,
      ];

      // Filter for front page products and shuffle them randomly
      const frontPageProducts = allProducts.filter((product) => product.is_front_page);

      // Shuffle the array to display products in random order
      return frontPageProducts.sort(() => Math.random() - 0.5);
    },
  });
};