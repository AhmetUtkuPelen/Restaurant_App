import { useState } from "react";
import { Button } from "@/Components/ui/button";
import { Link, useParams } from "react-router-dom";
import { useDrink, useDrinks } from "@/hooks/useProducts";
import {
  Heart,
  ShoppingCart,
  Star,
  Plus,
  Minus,
  ArrowLeft,
  Coffee,
  Droplets,
} from "lucide-react";
import { useCartStore } from "@/Zustand/Cart/CartState";
import CommentSection from "@/Components/Comment/CommentSection";
import { useNavigate } from "react-router-dom";
import { useIsAuthenticated } from "@/Zustand/Auth/AuthState";
import { useMyFavourites, useAddFavourite, useRemoveFavourite } from "@/hooks/useFavourite";
import { toast } from "sonner";

const Drink = () => {
  const { id } = useParams();
  const [quantity, setQuantity] = useState(1);

  const navigate = useNavigate();
  const isAuthenticated = useIsAuthenticated();

  const { data: drink, isLoading, error } = useDrink(parseInt(id!));
  const { data: products = [] } = useDrinks();

  const addToCart = useCartStore((state) => state.addToCart);
  const { data: favouritesData = [] } = useMyFavourites();
  const addFavouriteMutation = useAddFavourite();
  const removeFavouriteMutation = useRemoveFavourite();

  const isFavourite = (productId: number) => {
    return favouritesData.some(fav => fav.product_id === productId);
  };

  const getFavouriteId = (productId: number) => {
    const fav = favouritesData.find(fav => fav.product_id === productId);
    return fav?.id;
  };

   const handleAddToCart = () => {
     if (!isAuthenticated) {
       toast.error("Please login to add items to cart !", {
         description: "You need to be logged in to add items to your cart !",
         action: {
           label: "Login",
           onClick: () => navigate("/login"),
         },
       });
       return;
     }

     addToCart(
       {
         id: drink!.id,
         name: drink!.name,
         price: drink!.price,
         final_price: drink!.final_price,
         image_url: drink!.image_url,
         category: "drink",
       },
       quantity
     );
     toast.success("Added to cart!", {
       description: `${quantity} x ${drink!.name} added to your cart.`,
     });
   };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      </div>
    );
  }

  if (error || !drink) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">
            Drink Not Found
          </h2>
          <Link to="/drinks" className="text-blue-400 hover:text-blue-300">
            Back to Drinks
          </Link>
        </div>
      </div>
    );
  }

  const finalPrice = parseFloat(drink.final_price);
  const relatedDrinks = products.filter((p) => p.id !== drink.id).slice(0, 3);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 py-4">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-2 text-sm">
            <Link to="/" className="text-gray-400 hover:text-blue-400">
              Home
            </Link>
            <span className="text-gray-600">/</span>
            <Link to="/drinks" className="text-gray-400 hover:text-blue-400">
              Drinks
            </Link>
            <span className="text-gray-600">/</span>
            <span className="text-white">{drink.name}</span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <Link
          to="/drinks"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Drinks
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <div className="relative mb-4">
              <img
                src={
                  drink.image_url ||
                  "https://via.placeholder.com/600x400/1f2937/ffffff?text=Drink"
                }
                alt={drink.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {drink.is_front_page && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
            </div>
          </div>

          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  {drink.name}
                </h1>
                <p className="text-gray-400 mb-4">Drinks</p>
              </div>
              <button
                onClick={async () => {
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
                  
                  try {
                    if (isFavourite(drink.id)) {
                      const favId = getFavouriteId(drink.id);
                      if (favId) {
                        await removeFavouriteMutation.mutateAsync(favId);
                        toast.success("Removed from favorites");
                      }
                    } else {
                      await addFavouriteMutation.mutateAsync({ product_id: drink.id });
                      toast.success("Added to favorites");
                    }
                  } catch (err) {
                    const error = err as { response?: { data?: { detail?: string } } };
                    toast.error(error?.response?.data?.detail || "Failed to update favorites");
                  }
                }}
                disabled={addFavouriteMutation.isPending || removeFavouriteMutation.isPending}
                className={`p-2 rounded-full transition-colors ${
                  isFavourite(drink.id)
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

            <div className="text-3xl font-bold text-blue-400 mb-6">
              ${finalPrice.toFixed(2)}
            </div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Coffee className="w-5 h-5 text-blue-400" />
                <span className="text-sm">{drink.size}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Droplets className="w-5 h-5 text-green-400" />
                <span className="text-sm">
                  {drink.is_acidic ? "Acidic" : "Non-Acidic"}
                </span>
              </div>
            </div>

            <p className="text-gray-300 mb-6 leading-relaxed">
              {drink.description}
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
                onClick={handleAddToCart}
                >
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart - ${(finalPrice * quantity).toFixed(2)}
              </Button>
            </div>

            <Button
              variant="outline"
              onClick={async () => {
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
                
                try {
                  if (isFavourite(drink.id)) {
                    const favId = getFavouriteId(drink.id);
                    if (favId) {
                      await removeFavouriteMutation.mutateAsync(favId);
                      toast.success("Removed from favorites");
                    }
                  } else {
                    await addFavouriteMutation.mutateAsync({ product_id: drink.id });
                    toast.success("Added to favorites");
                  }
                } catch (err) {
                  const error = err as { response?: { data?: { detail?: string } } };
                  toast.error(error?.response?.data?.detail || "Failed to update favorites");
                }
              }}
              disabled={addFavouriteMutation.isPending || removeFavouriteMutation.isPending}
              className={`w-full mb-8 transition-colors py-3 cursor-pointer ${
                isFavourite(drink.id)
                  ? "border-red-400 bg-red-400 text-white hover:bg-red-500"
                  : "border-red-400 text-red-400 hover:bg-red-400 hover:text-white"
              }`}
            >
              <Heart
                className={`w-5 h-5 mr-2 ${
                  isFavourite(drink.id) ? "fill-current" : ""
                }`}
              />
              {isFavourite(drink.id)
                ? "Remove from Favorites"
                : "Add to Favorites"}
            </Button>

            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-blue-400">
                Product Information
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-400">Size:</span>
                  <span className="text-white">{drink.size}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400">Type:</span>
                  <span className="text-white">
                    {drink.is_acidic ? "Acidic" : "Non-Acidic"}
                  </span>
                </div>
                {drink.tags && drink.tags.length > 0 && (
                  <div>
                    <span className="text-gray-400 block mb-2">Tags:</span>
                    <div className="flex flex-wrap gap-1">
                      {drink.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="bg-blue-600/20 text-blue-400 px-2 py-1 rounded text-xs"
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

        {/* Comments Section */}
        <CommentSection productId={drink.id} />

        {/* Related Products */}
        <div className="mt-16">
          <h2 className="text-2xl font-bold mb-8 text-blue-400">
            You Might Also Like
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {relatedDrinks.map((item) => (
              <Link
                key={item.id}
                to={`/drinks/${item.id}`}
                className="bg-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
              >
                <img
                  src={
                    item.image_url ||
                    "https://via.placeholder.com/200x150/1f2937/ffffff?text=Drink"
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

export default Drink;