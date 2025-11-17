import { useState } from "react";
import { useSalads } from "@/hooks/useProducts";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Card, CardContent } from "@/Components/ui/card";
import { Link } from "react-router-dom";
import {
  Heart,
  ShoppingCart,
  Star,
  Search,
  Grid3X3,
  List,
  Leaf,
} from "lucide-react";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useFavouriteStore } from "@/Zustand/FavouriteProduct/FavouriteProductState";

const Salads = () => {
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [searchTerm, setSearchTerm] = useState("");

  const { data: salads = [], isLoading, error } = useSalads();
  const addToCart = useCartStore((state) => state.addToCart);
  const addToFavourites = useFavouriteStore((state) => state.addToFavourites);
  const removeFromFavourites = useFavouriteStore((state) => state.removeFromFavourites);
  const isFavourite = useFavouriteStore((state) => state.isFavourite);

  const filteredSalads = salads.filter((salad) =>
    salad.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Leaf className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl md:text-6xl font-bold text-blue-400">
              Salads
            </h1>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Fresh, healthy, and delicious salads made with the finest
            ingredients. Perfect for a light meal or as a healthy side dish.
          </p>
        </div>
      </section>

      <section className="py-8 bg-gray-800 border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder="Search salads..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-gray-900 border-gray-600 text-white placeholder-gray-400"
              />
            </div>
            <div className="flex border border-gray-600 rounded-lg overflow-hidden">
              <button
                onClick={() => setViewMode("grid")}
                className={`p-2 ${
                  viewMode === "grid"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-700 text-gray-300"
                }`}
              >
                <Grid3X3 className="w-5 h-5" />
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`p-2 ${
                  viewMode === "list"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-700 text-gray-300"
                }`}
              >
                <List className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="py-12 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          {isLoading && (
            <div className="flex justify-center items-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
            </div>
          )}

          {error && (
            <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
              {error instanceof Error ? error.message : "Failed to load salads"}
            </div>
          )}

          {!isLoading && !error && filteredSalads.length === 0 && (
            <div className="text-center py-20">
              <p className="text-gray-400 text-lg">No salads found</p>
            </div>
          )}

          {!isLoading && !error && filteredSalads.length > 0 && (
            <div
              className={`grid gap-6 ${
                viewMode === "grid"
                  ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
                  : "grid-cols-1"
              }`}
            >
              {filteredSalads.map((salad) => {
                const saladData = salad as typeof salad & {
                  image_url?: string;
                  image?: string;
                  is_front_page?: boolean;
                  isPopular?: boolean;
                  isVegan?: boolean;
                  comments?: unknown[];
                  reviews?: number;
                  final_price?: string;
                };
                const hasDiscount =
                  (salad as typeof salad & { discount_percentage?: string })
                    .discount_percentage &&
                  parseFloat(
                    (salad as typeof salad & { discount_percentage?: string })
                      .discount_percentage || "0"
                  ) > 0;
                const price = parseFloat(String(salad.price || "0"));
                const finalPrice = parseFloat(
                  saladData.final_price || String(salad.price || "0")
                );

                return (
                  <Card
                    key={salad.id}
                    className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                      viewMode === "list" ? "flex" : ""
                    }`}
                  >
                    <div
                      className={`relative ${
                        viewMode === "list" ? "w-64 flex-shrink-0" : ""
                      }`}
                    >
                      <img
                        src={
                          saladData.image_url ||
                          saladData.image ||
                          "https://via.placeholder.com/300x200/1f2937/ffffff?text=Salad"
                        }
                        alt={salad.name}
                        className={`object-cover ${
                          viewMode === "list" ? "w-full h-full" : "w-full h-48"
                        }`}
                      />
                      {(saladData.is_front_page || saladData.isPopular) && (
                        <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                          Popular
                        </div>
                      )}
                      {((salad as typeof salad & { is_vegan?: boolean })
                        .is_vegan ||
                        saladData.isVegan) && (
                        <div className="absolute top-2 right-2 bg-green-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                          Vegan
                        </div>
                      )}
                      {hasDiscount && (
                        <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                          Sale
                        </div>
                      )}
                      <div className="absolute bottom-2 left-2 bg-gray-900/80 text-white px-2 py-1 rounded-full text-xs">
                        {salad.calories} cal
                      </div>
                    </div>

                    <CardContent
                      className={`p-6 ${viewMode === "list" ? "flex-1" : ""}`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="text-xl font-semibold text-white">
                          {salad.name}
                        </h3>
                        <button className="text-gray-400 hover:text-red-400 transition-colors">
                          <Heart className="w-5 h-5" />
                        </button>
                      </div>

                      <p className="text-gray-400 mb-3 text-sm">
                        {salad.description}
                      </p>

                      <div className="flex items-center gap-2 mb-3">
                        <div className="flex items-center">
                          {[...Array(5)].map((_, i) => (
                            <Star
                              key={i}
                              className={`w-4 h-4 ${
                                i < 4
                                  ? "text-yellow-400 fill-current"
                                  : "text-gray-600"
                              }`}
                            />
                          ))}
                        </div>
                        <span className="text-sm text-gray-400">
                          4.5 (
                          {(salad as typeof salad & { comments?: unknown[] })
                            .comments?.length ||
                            saladData.reviews ||
                            0}{" "}
                          reviews)
                        </span>
                      </div>

                      <div className="flex items-center gap-2 mb-4">
                        <span className="text-2xl font-bold text-blue-400">
                          ${finalPrice.toFixed(2)}
                        </span>
                        {hasDiscount && (
                          <span className="text-lg text-gray-500 line-through">
                            ${price.toFixed(2)}
                          </span>
                        )}
                      </div>

                      <div className="flex gap-2 mb-3">
                        <Button 
                          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
                          onClick={() => addToCart({
                            id: salad.id,
                            name: salad.name,
                            price: salad.price,
                            final_price: salad.final_price,
                            image_url: salad.image_url,
                            category: "salad"
                          })}
                        >
                          <ShoppingCart className="w-4 h-4 mr-2" />
                          Add to Cart
                        </Button>
                        <Link
                          to={`/salads/${salad.id}`}
                          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors text-center"
                        >
                          View Details
                        </Link>
                      </div>

                      <Button
                        variant="outline"
                        onClick={() => {
                          if (isFavourite(salad.id)) {
                            removeFromFavourites(salad.id);
                          } else {
                            addToFavourites({
                              id: salad.id,
                              name: salad.name,
                              price: salad.price,
                              final_price: salad.final_price,
                              image_url: salad.image_url,
                              category: "salad",
                              description: salad.description
                            });
                          }
                        }}
                        className={`w-full transition-colors ${
                          isFavourite(salad.id)
                            ? "border-red-400 bg-red-400 text-white hover:bg-red-500"
                            : "border-red-400 text-red-400 hover:bg-red-400 hover:text-white"
                        }`}
                      >
                        <Heart className={`w-4 h-4 mr-2 ${isFavourite(salad.id) ? "fill-current" : ""}`} />
                        {isFavourite(salad.id) ? "Remove from Favorites" : "Add to Favorites"}
                      </Button>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Salads;
