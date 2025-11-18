import { useState } from "react";
import { Button } from "@/Components/ui/button";
import { Link, useParams } from "react-router-dom";
import { useDoner, useDoners } from "@/hooks/useProducts";
import {
  Heart,
  ShoppingCart,
  Star,
  Plus,
  Minus,
  ArrowLeft,
  Clock,
  Users,
  Utensils,
  Flame,
} from "lucide-react";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useFavouriteStore } from "@/Zustand/FavouriteProduct/FavouriteProductState";
import CommentSection from "@/Components/Comment/CommentSection";

const Doner = () => {
  const { id } = useParams();
  const [quantity, setQuantity] = useState(1);

  const { data: doner, isLoading, error } = useDoner(parseInt(id!));
  const { data: products = [] } = useDoners();

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

  if (error || !doner) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            Doner Not Found
          </h2>
          <Link to="/doners" className="text-blue-400 hover:text-blue-300">
            Back to Doners
          </Link>
        </div>
      </div>
    );
  }

  const hasDiscount = parseFloat(doner.discount_percentage || "0") > 0;
  const price = parseFloat(doner.price || "0");
  const finalPrice = parseFloat(doner.final_price || doner.price || "0");
  const relatedDoners = products.filter((p) => p.id !== doner.id).slice(0, 3);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Breadcrumb */}
      <div className="bg-gray-800 py-4">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-2 text-sm">
            <Link to="/" className="text-gray-400 hover:text-blue-400">
              Home
            </Link>
            <span className="text-gray-600">/</span>
            <Link to="/doners" className="text-gray-400 hover:text-blue-400">
              Doners
            </Link>
            <span className="text-gray-600">/</span>
            <span className="text-white">{doner.name}</span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <Link
          to="/doners"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Doners
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Product Image */}
          <div>
            <div className="relative">
              <img
                src={
                  doner.image_url ||
                  "https://via.placeholder.com/600x400/1f2937/ffffff?text=Doner"
                }
                alt={doner.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {doner.is_front_page && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
              <div className="absolute top-4 right-4 bg-orange-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                <Flame className="w-4 h-4" />
                {doner.spice_level}
              </div>
            </div>
          </div>

          {/* Product Details */}
          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  {doner.name}
                </h1>
                <p className="text-gray-400 mb-4">Doner Kebabs</p>
              </div>
              <button
                onClick={() => {
                  if (isFavourite(doner.id)) {
                    removeFromFavourites(doner.id);
                  } else {
                    addToFavourites({
                      id: doner.id,
                      name: doner.name,
                      price: doner.price,
                      final_price: doner.final_price,
                      image_url: doner.image_url,
                      category: "doner",
                      description: doner.description,
                    });
                  }
                }}
                className={`p-2 rounded-full transition-colors ${
                  isFavourite(doner.id)
                    ? "text-red-400 bg-red-400/20"
                    : "text-gray-400 hover:text-red-400"
                }`}
              >
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

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Clock className="w-5 h-5 text-blue-400" />
                <span className="text-sm">10 mins</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Users className="w-5 h-5 text-green-400" />
                <span className="text-sm">1 person</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Utensils className="w-5 h-5 text-yellow-400" />
                <span className="text-sm">{doner.size}</span>
              </div>
            </div>

            <p className="text-gray-300 mb-6 leading-relaxed">
              {doner.description}
            </p>

            <div className="flex items-center gap-4 mb-6">
              <span className="text-gray-300">Quantity:</span>
              <div className="flex items-center border border-gray-600 rounded-lg">
                <Button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2 hover:text-blue-500 transition-colors cursor-pointer"
                >
                  <Minus className="w-4 h-4" />
                </Button>
                <span className="px-4 py-2 border-x border-gray-600">
                  {quantity}
                </span>
                <Button
                  onClick={() => setQuantity(quantity + 1)}
                  className="p-2 hover:text-blue-500 transition-colors cursor-pointer"
                >
                  <Plus className="w-4 h-4" />
                </Button>
              </div>
            </div>

            <div className="flex gap-4 mb-4">
              <Button
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg cursor-pointer"
                onClick={() =>
                  addToCart(
                    {
                      id: doner.id,
                      name: doner.name,
                      price: doner.price,
                      final_price: doner.final_price,
                      image_url: doner.image_url,
                      category: "doner",
                    },
                    quantity
                  )
                }
              >
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart - ${(finalPrice * quantity).toFixed(2)}
              </Button>
            </div>

            <Button
              variant="outline"
              onClick={() => {
                if (isFavourite(doner.id)) {
                  removeFromFavourites(doner.id);
                } else {
                  addToFavourites({
                    id: doner.id,
                    name: doner.name,
                    price: doner.price,
                    final_price: doner.final_price,
                    image_url: doner.image_url,
                    category: "doner",
                    description: doner.description,
                  });
                }
              }}
              className={`w-full mb-8 transition-colors py-3 cursor-pointer ${
                isFavourite(doner.id)
                  ? "border-red-400 bg-red-400 text-white hover:bg-red-500"
                  : "border-red-400 text-red-400 hover:bg-red-400 hover:text-white"
              }`}
            >
              <Heart
                className={`w-5 h-5 mr-2 ${
                  isFavourite(doner.id) ? "fill-current" : ""
                }`}
              />
              {isFavourite(doner.id)
                ? "Remove from Favorites"
                : "Add to Favorites"}
            </Button>

            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-yellow-400">
                Product Information
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-400">Size:</span>
                  <span className="text-white">{doner.size}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Meat Type:</span>
                  <span className="text-white">{doner.meat_type}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Spice Level:</span>
                  <span className="text-white">{doner.spice_level}</span>
                </div>
                <div className="flex flex-wrap gap-2 mt-3">
                  {doner.is_vegan && (
                    <span className="bg-green-600/20 text-green-400 px-2 py-1 rounded text-sm">
                      Vegan
                    </span>
                  )}
                  {doner.is_alergic && (
                    <span className="bg-yellow-600/20 text-yellow-400 px-2 py-1 rounded text-sm">
                      Contains Allergens
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Comments Section */}
        <CommentSection productId={doner.id} />

        {/* Related Products */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold mb-8 text-blue-400">
            You Might Also Like
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {relatedDoners.map((item) => (
              <Link
                key={item.id}
                to={`/doners/${item.id}`}
                className="bg-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
              >
                <img
                  src={
                    item.image_url ||
                    "https://via.placeholder.com/200x150/1f2937/ffffff?text=Doner"
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

export default Doner;
