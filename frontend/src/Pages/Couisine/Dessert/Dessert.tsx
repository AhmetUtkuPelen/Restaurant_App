import { useState } from "react";
import { Button } from "@/Components/ui/button";
import { Link, useParams, useNavigate } from "react-router-dom";
import { useDessert, useDesserts } from "@/hooks/useProducts";
import {
  Heart,
  ShoppingCart,
  Star,
  Plus,
  Minus,
  ArrowLeft,
  Clock,
  Users,
  Award,
} from "lucide-react";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useFavouriteStore } from "@/Zustand/FavouriteProduct/FavouriteProductState";
import { useIsAuthenticated } from "@/Zustand/Auth/AuthState";
import { toast } from "sonner";
import CommentSection from "@/Components/Comment/CommentSection";

const Dessert = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [quantity, setQuantity] = useState(1);

  const { data: dessert, isLoading, error } = useDessert(parseInt(id!));
  const { data: products = [] } = useDesserts();

  const addToCart = useCartStore((state) => state.addToCart);
  const addToFavourites = useFavouriteStore((state) => state.addToFavourites);
  const removeFromFavourites = useFavouriteStore(
    (state) => state.removeFromFavourites
  );
  const isFavourite = useFavouriteStore((state) => state.isFavourite);
  const isAuthenticated = useIsAuthenticated();

  const handleAddToCart = () => {
    if (!isAuthenticated) {
      toast.error("Please login to add items to cart", {
        description: "You need to be logged in to add items to your cart.",
        action: {
          label: "Login",
          onClick: () => navigate("/login"),
        },
      });
      return;
    }

    addToCart(
      {
        id: dessert!.id,
        name: dessert!.name,
        price: dessert!.price,
        final_price: dessert!.final_price,
        image_url: dessert!.image_url,
        category: "dessert",
      },
      quantity
    );
    toast.success("Added to cart!", {
      description: `${quantity} x ${dessert!.name} added to your cart.`,
    });
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      </div>
    );
  }

  if (error || !dessert) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            Dessert Not Found
          </h2>
          <Link to="/desserts" className="text-blue-400 hover:text-blue-300">
            Back to Desserts
          </Link>
        </div>
      </div>
    );
  }

  const hasDiscount = parseFloat(dessert.discount_percentage || "0") > 0;
  const price = parseFloat(dessert.price || "0");
  const finalPrice = parseFloat(dessert.final_price || dessert.price || "0");
  const relatedDesserts = products
    .filter((p) => p.id !== dessert.id)
    .slice(0, 3);

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
            <Link to="/desserts" className="text-gray-400 hover:text-blue-400">
              Desserts
            </Link>
            <span className="text-gray-600">/</span>
            <span className="text-white">{dessert.name}</span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        {/* Back Button */}
        <Link
          to="/desserts"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Desserts
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Product Image */}
          <div>
            <div className="relative">
              <img
                src={
                  dessert.image_url ||
                  "https://via.placeholder.com/600x400/1f2937/ffffff?text=Dessert"
                }
                alt={dessert.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {dessert.is_front_page && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
              {hasDiscount && (
                <div className="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  On Sale
                </div>
              )}
            </div>
          </div>

          {/* Product Details */}
          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  {dessert.name}
                </h1>
                <p className="text-gray-400 mb-4">Desserts</p>
              </div>
              <button
                onClick={() => {
                  if (!isAuthenticated) {
                    toast.error("Please login to manage favorites", {
                      description: "You need to be logged in to add items to your favorites.",
                      action: {
                        label: "Login",
                        onClick: () => navigate("/login"),
                      },
                    });
                    return;
                  }
                  
                  if (isFavourite(dessert.id)) {
                    removeFromFavourites(dessert.id);
                    toast.success("Removed from favorites");
                  } else {
                    addToFavourites({
                      id: dessert.id,
                      name: dessert.name,
                      price: dessert.price,
                      final_price: dessert.final_price,
                      image_url: dessert.image_url,
                      category: "dessert",
                      description: dessert.description,
                    });
                    toast.success("Added to favorites");
                  }
                }}
                className={`p-2 rounded-full transition-colors ${
                  isFavourite(dessert.id)
                    ? "text-red-400 bg-red-400/20"
                    : "text-gray-400 hover:text-red-400"
                }`}
              >
              </button>
            </div>

            {/* Rating */}
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

            {/* Price */}
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl font-bold text-blue-400">
                ${finalPrice.toFixed(2)}
              </span>
              {hasDiscount && (
                <span className="text-xl text-gray-500 line-through">
                  ${price.toFixed(2)}
                </span>
              )}
              {hasDiscount && (
                <span className="bg-red-600 text-white px-2 py-1 rounded text-sm">
                  Save ${(price - finalPrice).toFixed(2)}
                </span>
              )}
            </div>

            {/* Quick Info */}
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Clock className="w-5 h-5 text-blue-400" />
                <span className="text-sm">15 mins</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Users className="w-5 h-5 text-green-400" />
                <span className="text-sm">2-3 people</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Award className="w-5 h-5 text-yellow-400" />
                <span className="text-sm">{dessert.calories} cal</span>
              </div>
            </div>

            {/* Description */}
            <p className="text-gray-300 mb-6 leading-relaxed">
              {dessert.description}
            </p>

            {/* Quantity Selector */}
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

            {/* Action Buttons */}
            <div className="flex gap-4 mb-4">
              <Button
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg cursor-pointer"
                onClick={handleAddToCart}
              >
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart - ${(finalPrice * quantity).toFixed(2)}
              </Button>
            </div>

            {/* Add to Favorites Button */}
            <Button
              variant="outline"
              onClick={() => {
                if (!isAuthenticated) {
                  toast.error("Please login to manage favorites", {
                    description: "You need to be logged in to add items to your favorites.",
                    action: {
                      label: "Login",
                      onClick: () => navigate("/login"),
                    },
                  });
                  return;
                }
                
                if (isFavourite(dessert.id)) {
                  removeFromFavourites(dessert.id);
                  toast.success("Removed from favorites");
                } else {
                  addToFavourites({
                    id: dessert.id,
                    name: dessert.name,
                    price: dessert.price,
                    final_price: dessert.final_price,
                    image_url: dessert.image_url,
                    category: "dessert",
                    description: dessert.description,
                  });
                  toast.success("Added to favorites");
                }
              }}
              className={`w-full mb-8 transition-colors py-3 cursor-pointer ${
                isFavourite(dessert.id)
                  ? "border-red-400 bg-red-400 text-white hover:bg-red-500"
                  : "border-red-400 text-red-400 hover:bg-red-400 hover:text-white"
              }`}
            >
              <Heart
                className={`w-5 h-5 mr-2 ${
                  isFavourite(dessert.id) ? "fill-current" : ""
                }`}
              />
              {isFavourite(dessert.id)
                ? "Remove from Favorites"
                : "Add to Favorites"}
            </Button>

            {/* Allergen Info */}
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-yellow-400">
                Product Information
              </h3>
              <div className="flex flex-wrap gap-2">
                {dessert.is_vegan && (
                  <span className="bg-green-600/20 text-green-400 px-2 py-1 rounded text-sm">
                    Vegan
                  </span>
                )}
                {dessert.is_alergic && (
                  <span className="bg-yellow-600/20 text-yellow-400 px-2 py-1 rounded text-sm">
                    Contains Allergens
                  </span>
                )}
                <span className="bg-blue-600/20 text-blue-400 px-2 py-1 rounded text-sm">
                  {dessert.dessert_type}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Tabs Section */}
        <div className="mt-16">
          <div className="py-8">
            {/* Ingredients Tab */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold mb-4 text-blue-400">
                  Product Details
                </h3>
                <div className="bg-gray-800 rounded-lg p-4 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Type:</span>
                    <span className="text-white font-medium">
                      {dessert.dessert_type}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Calories:</span>
                    <span className="text-white font-medium">
                      {dessert.calories} cal
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Vegan:</span>
                    <span className="text-white font-medium">
                      {dessert.is_vegan ? "Yes" : "No"}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Allergens:</span>
                    <span className="text-white font-medium">
                      {dessert.is_alergic ? "Yes" : "No"}
                    </span>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4 text-blue-400">
                  Tags
                </h3>
                <div className="flex flex-wrap gap-2">
                  {dessert.tags && dessert.tags.length > 0 ? (
                    dessert.tags.map((tag, index) => (
                      <span
                        key={index}
                        className="bg-gray-800 text-gray-300 px-3 py-1 rounded-full text-sm"
                      >
                        {tag}
                      </span>
                    ))
                  ) : (
                    <span className="text-gray-400 text-sm">
                      No tags available
                    </span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Comments Section */}
        <CommentSection productId={dessert.id} />

        {/* Related Products */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold mb-8 text-blue-400">
            You Might Also Like
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {relatedDesserts.map((item) => (
              <Link
                key={item.id}
                to={`/desserts/${item.id}`}
                className="bg-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
              >
                <img
                  src={
                    item.image_url ||
                    "https://via.placeholder.com/200x150/1f2937/ffffff?text=Dessert"
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

export default Dessert;
