/* eslint-disable @typescript-eslint/no-explicit-any */
import { Link } from "react-router-dom";
import { Button } from "@/Components/ui/button";
import { Card, CardContent } from "@/Components/ui/card";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { Heart, ShoppingCart, Star, Trash2, ArrowLeft, Loader2 } from "lucide-react";
import { useMyFavourites, useRemoveFavourite, useClearFavourites } from "@/hooks/useFavourite";
import { toast } from "sonner";

const FavouriteProducts = () => {
  const { data: favouritesData = [], isLoading, error } = useMyFavourites();
  const removeFavouriteMutation = useRemoveFavourite();
  const clearFavouritesMutation = useClearFavourites();
  const addToCart = useCartStore((state) => state.addToCart);

  const handleRemoveFavourite = async (favouriteId: number) => {
    try {
      await removeFavouriteMutation.mutateAsync(favouriteId);
      toast.success("Removed from favourites");
    } catch {
      toast.error("Failed to remove from favourites");
    }
  };

  const handleClearAll = async () => {
    try {
      await clearFavouritesMutation.mutateAsync();
      toast.success("All favourites cleared");
    } catch {
      toast.error("Failed to clear favourites");
    }
  };

  // Helper function to get product link based on category
  const getProductLink = (category: string, id: number) => {
    const categoryMap: { [key: string]: string } = {
      dessert: "desserts",
      doner: "doners",
      drink: "drinks",
      kebab: "kebabs",
      salad: "salads",
    };
    return `/${categoryMap[category] || category}/${id}`;
  };

  const handleAddToCart = (product: any) => {
    addToCart({
      id: product.id,
      name: product.name,
      price: product.price,
      final_price: product.final_price,
      image_url: product.image_url,
      category: product.category,
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-blue-400 animate-spin" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 text-xl mb-4">Failed to load favourites</p>
          <Button onClick={() => window.location.reload()}>Try Again</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header Section */}
      <section className="relative py-12 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-6 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Home
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <Heart className="w-10 h-10 text-red-400 fill-current" />
                <h1 className="text-4xl md:text-5xl font-bold text-blue-400">
                  My Favourites
                </h1>
              </div>
              <p className="text-xl text-gray-300">
                {favouritesData.length} {favouritesData.length === 1 ? "item" : "items"}{" "}
                saved
              </p>
            </div>
            {favouritesData.length > 0 && (
              <Button
                variant="outline"
                onClick={handleClearAll}
                disabled={clearFavouritesMutation.isPending}
                className="border-red-600 text-red-400 hover:bg-red-900/20 hover:text-red-300 cursor-pointer"
              >
                {clearFavouritesMutation.isPending ? (
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <Trash2 className="w-4 h-4 mr-2" />
                )}
                Clear All
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Favourites Grid */}
      <section className="py-12 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          {favouritesData.length === 0 ? (
            <div className="text-center py-20">
              <Heart className="w-24 h-24 text-gray-700 mx-auto mb-6" />
              <h2 className="text-2xl font-bold text-white mb-4">
                No Favourites Yet
              </h2>
              <p className="text-gray-400 mb-8 max-w-md mx-auto">
                Start adding your favourite dishes to see them here. Click the
                heart icon on any product to save it!
              </p>
              <Link to="/">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Browse Products
                </Button>
              </Link>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {favouritesData.map((favourite) => {
                const product = favourite.product;
                const hasDiscount =
                  parseFloat(product.final_price || "0") <
                  parseFloat(product.price || "0");
                const finalPrice = parseFloat(
                  product.final_price || product.price || "0"
                );
                const originalPrice = parseFloat(product.price || "0");

                return (
                  <Card
                    key={product.id}
                    className="bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
                  >
                    <div className="relative">
                      <Link to={getProductLink(product.category, product.id)}>
                        <img
                          src={
                            product.image_url ||
                            "https://via.placeholder.com/300x200/1f2937/ffffff?text=Product"
                          }
                          alt={product.name}
                          className="w-full h-48 object-cover"
                        />
                      </Link>
                      {hasDiscount && (
                        <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                          Sale
                        </div>
                      )}
                      <button
                        onClick={() => handleRemoveFavourite(favourite.id)}
                        disabled={removeFavouriteMutation.isPending}
                        className="absolute top-2 left-2 bg-red-500 hover:bg-red-600 text-white p-2 rounded-full transition-colors disabled:opacity-50"
                      >
                        {removeFavouriteMutation.isPending ? (
                          <Loader2 className="w-4 h-4 animate-spin" />
                        ) : (
                          <Heart className="w-4 h-4 fill-current" />
                        )}
                      </button>
                    </div>

                    <CardContent className="p-4">
                      <Link to={getProductLink(product.category, product.id)}>
                        <h3 className="text-lg font-semibold text-white mb-2 hover:text-blue-400 transition-colors">
                          {product.name}
                        </h3>
                      </Link>

                      {product.description && (
                        <p className="text-gray-400 text-sm mb-3 line-clamp-2">
                          {product.description}
                        </p>
                      )}

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
                        <span className="text-sm text-gray-400">4.5</span>
                      </div>

                      <div className="flex items-center gap-2 mb-4">
                        <span className="text-2xl font-bold text-blue-400">
                          ${finalPrice.toFixed(2)}
                        </span>
                        {hasDiscount && (
                          <span className="text-lg text-gray-500 line-through">
                            ${originalPrice.toFixed(2)}
                          </span>
                        )}
                      </div>

                      <div className="flex gap-2">
                        <Button
                          onClick={() => handleAddToCart(product)}
                          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white cursor-pointer"
                        >
                          <ShoppingCart className="w-4 h-4 mr-2" />
                          Add to Cart
                        </Button>
                        <Link
                          to={getProductLink(product.category, product.id)}
                          className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors text-center flex items-center"
                        >
                          View
                        </Link>
                      </div>
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

export default FavouriteProducts;
