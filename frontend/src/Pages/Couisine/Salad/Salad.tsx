import { useState } from "react";
import { Button } from "@/Components/ui/button";
import { Link, useParams } from "react-router-dom";
import { useSalad, useSalads } from "@/hooks/useProducts";
import {
  Heart,
  ShoppingCart,
  Star,
  Plus,
  Minus,
  ArrowLeft,
  Leaf,
  Award,
} from "lucide-react";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useFavouriteStore } from "@/Zustand/FavouriteProduct/FavouriteProductState";

const Salad = () => {
  const { id } = useParams();
  const [quantity, setQuantity] = useState(1);

  const { data: salad, isLoading, error } = useSalad(parseInt(id!));
  const { data: products = [] } = useSalads();

  const addToCart = useCartStore((state) => state.addToCart);
  const addToFavourites = useFavouriteStore((state) => state.addToFavourites);
  const removeFromFavourites = useFavouriteStore(
    (state) => state.removeFromFavourites
  );
  const isFavourite = useFavouriteStore((state) => state.isFavourite);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      </div>
    );
  }

  if (error || !salad) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            Salad Not Found
          </h2>
          <Link to="/salads" className="text-blue-400 hover:text-blue-300">
            Back to Salads
          </Link>
        </div>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      </div>
    );
  }

  if (error || !salad) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            Salad Not Found
          </h2>
          <Link to="/salads" className="text-blue-400 hover:text-blue-300">
            Back to Salads
          </Link>
        </div>
      </div>
    );
  }

  const hasDiscount = parseFloat(salad.discount_percentage || "0") > 0;
  const price = parseFloat(salad.price || "0");
  const finalPrice = parseFloat(salad.final_price || salad.price || "0");
  const relatedSalads = products.filter((p) => p.id !== salad.id).slice(0, 3);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 py-4">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-2 text-sm">
            <Link to="/" className="text-gray-400 hover:text-blue-400">
              Home
            </Link>
            <span className="text-gray-600">/</span>
            <Link to="/salads" className="text-gray-400 hover:text-blue-400">
              Salads
            </Link>
            <span className="text-gray-600">/</span>
            <span className="text-white">{salad.name}</span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <Link
          to="/salads"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Salads
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <div className="relative mb-4">
              <img
                src={
                  salad.image_url ||
                  "https://via.placeholder.com/600x400/1f2937/ffffff?text=Salad"
                }
                alt={salad.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {salad.is_front_page && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
              {salad.is_vegan ? (
                <div className="absolute top-4 right-4 bg-green-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Vegan
                </div>
              ) : (
                <div className="absolute top-4 right-4 bg-orange-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Vegetarian
                </div>
              )}
            </div>
          </div>

          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  {salad.name}
                </h1>
                <p className="text-gray-400 mb-4">Fresh Salads</p>
              </div>
              <button
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
                      description: salad.description,
                    });
                  }
                }}
                className={`p-2 rounded-full transition-colors ${
                  isFavourite(salad.id)
                    ? "text-red-400 bg-red-400/20"
                    : "text-gray-400 hover:text-red-400"
                }`}
              >
                <Heart
                  className={`w-6 h-6 ${
                    isFavourite(salad.id) ? "fill-current" : ""
                  }`}
                />
              </button>
            </div>

            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-5 h-5 ${
                      i < 4 ? "text-yellow-400 fill-current" : "text-gray-600"
                    }`}
                  />
                ))}
              </div>
              <span className="text-gray-300">4.5</span>
              <span className="text-gray-400">(0 reviews)</span>
            </div>

            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl font-bold text-blue-400">
                ${finalPrice.toFixed(2)}
              </span>
              {hasDiscount && (
                <>
                  <span className="text-xl text-gray-500 line-through">
                    ${price.toFixed(2)}
                  </span>
                  <span className="bg-red-600 text-white px-2 py-1 rounded text-sm">
                    Save ${(price - finalPrice).toFixed(2)}
                  </span>
                </>
              )}
            </div>

            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Leaf className="w-5 h-5 text-green-400" />
                <span className="text-sm">Fresh & Healthy</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Award className="w-5 h-5 text-yellow-400" />
                <span className="text-sm">{salad.calories} calories</span>
              </div>
            </div>

            <p className="text-gray-300 mb-6 leading-relaxed">
              {salad.description}
            </p>

            <div className="flex items-center gap-4 mb-6">
              <span className="text-gray-300">Quantity:</span>
              <div className="flex items-center border border-gray-600 rounded-lg">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2 hover:bg-gray-700 transition-colors"
                >
                  <Minus className="w-4 h-4" />
                </button>
                <span className="px-4 py-2 border-x border-gray-600">
                  {quantity}
                </span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="p-2 hover:bg-gray-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="flex gap-4 mb-4">
              <Button
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg"
                onClick={() =>
                  addToCart(
                    {
                      id: salad.id,
                      name: salad.name,
                      price: salad.price,
                      final_price: salad.final_price,
                      image_url: salad.image_url,
                      category: "salad",
                    },
                    quantity
                  )
                }
              >
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart - ${(finalPrice * quantity).toFixed(2)}
              </Button>
              <Button
                variant="outline"
                className="px-6 border-gray-600 text-gray-300 hover:bg-gray-700"
              >
                Buy Now
              </Button>
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
                    description: salad.description,
                  });
                }
              }}
              className={`w-full mb-8 transition-colors py-3 ${
                isFavourite(salad.id)
                  ? "border-red-400 bg-red-400 text-white hover:bg-red-500"
                  : "border-red-400 text-red-400 hover:bg-red-400 hover:text-white"
              }`}
            >
              <Heart
                className={`w-5 h-5 mr-2 ${
                  isFavourite(salad.id) ? "fill-current" : ""
                }`}
              />
              {isFavourite(salad.id)
                ? "Remove from Favorites"
                : "Add to Favorites"}
            </Button>

            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-green-400">
                Product Information
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-400">Calories:</span>
                  <span className="text-white">{salad.calories} cal</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Vegan:</span>
                  <span className="text-white">
                    {salad.is_vegan ? "Yes" : "No"}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Allergens:</span>
                  <span className="text-white">
                    {salad.is_alergic ? "Yes" : "No"}
                  </span>
                </div>
                {salad.tags && salad.tags.length > 0 && (
                  <div>
                    <span className="text-gray-400 block mb-2">Tags:</span>
                    <div className="flex flex-wrap gap-1">
                      {salad.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="bg-green-600/20 text-green-400 px-2 py-1 rounded text-xs"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Related Products */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold mb-8 text-blue-400">
            You Might Also Like
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {relatedSalads.map((item) => (
              <Link
                key={item.id}
                to={`/salads/${item.id}`}
                className="bg-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
              >
                <img
                  src={
                    item.image_url ||
                    "https://via.placeholder.com/200x150/1f2937/ffffff?text=Salad"
                  }
                  alt={item.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="font-semibold mb-2">{item.name}</h3>
                  <div className="flex items-center justify-between">
                    <span className="text-blue-400 font-bold">
                      ${parseFloat(item.final_price).toFixed(2)}
                    </span>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      <span className="text-sm text-gray-400 ml-1">4.5</span>
                    </div>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Salad;
