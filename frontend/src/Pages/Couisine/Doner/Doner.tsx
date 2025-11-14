

import { useState } from "react";
import { Button } from "@/Components/ui/button";
import { Link } from "react-router-dom";
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
  Flame
} from "lucide-react";

const Doner = () => {
  // const { id } = useParams();
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [isFavorite, setIsFavorite] = useState(false);

  const doner = {
    id: 1,
    name: "Classic Chicken Doner",
    description: "Tender marinated chicken slowly cooked on a vertical rotisserie, served in fresh pita bread with crisp vegetables and our signature garlic yogurt sauce. A perfect blend of Mediterranean flavors.",
    price: 12.99,
    images: [
      "https://via.placeholder.com/600x400/1f2937/ffffff?text=Chicken+Doner+Main",
      "https://via.placeholder.com/600x400/1f2937/ffffff?text=Chicken+Doner+Side",
      "https://via.placeholder.com/600x400/1f2937/ffffff?text=Chicken+Doner+Close"
    ],
    rating: 4.8,
    reviews: 156,
    prepTime: "10 mins",
    serves: "1 person",
    calories: 520,
    spiceLevel: "Mild",
    isPopular: true,
    ingredients: [
      "Marinated chicken breast",
      "Fresh pita bread",
      "Tomatoes",
      "Red onions",
      "Lettuce",
      "Garlic yogurt sauce"
    ],
    nutritionFacts: {
      calories: 520,
      protein: "35g",
      carbs: "42g",
      fat: "22g",
      fiber: "4g"
    },
    allergens: ["Gluten", "Dairy"],
    category: "Doner Kebabs"
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Breadcrumb */}
      <div className="bg-gray-800 py-4">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-2 text-sm">
            <Link to="/" className="text-gray-400 hover:text-blue-400">Home</Link>
            <span className="text-gray-600">/</span>
            <Link to="/doners" className="text-gray-400 hover:text-blue-400">Doners</Link>
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
          {/* Product Images */}
          <div>
            <div className="relative mb-4">
              <img
                src={doner.images[selectedImage]}
                alt={doner.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {doner.isPopular && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
              <div className="absolute top-4 right-4 bg-orange-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                <Flame className="w-4 h-4" />
                {doner.spiceLevel}
              </div>
            </div>

            <div className="flex gap-2">
              {doner.images.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors ${
                    selectedImage === index ? 'border-blue-400' : 'border-gray-600'
                  }`}
                >
                  <img src={image} alt={`${doner.name} ${index + 1}`} className="w-full h-full object-cover" />
                </button>
              ))}
            </div>
          </div>

          {/* Product Details */}
          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">{doner.name}</h1>
                <p className="text-gray-400 mb-4">{doner.category}</p>
              </div>
              <button
                onClick={() => setIsFavorite(!isFavorite)}
                className={`p-2 rounded-full transition-colors ${
                  isFavorite ? 'text-red-400 bg-red-400/20' : 'text-gray-400 hover:text-red-400'
                }`}
              >
                <Heart className={`w-6 h-6 ${isFavorite ? 'fill-current' : ''}`} />
              </button>
            </div>

            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-5 h-5 ${
                      i < Math.floor(doner.rating)
                        ? 'text-yellow-400 fill-current'
                        : 'text-gray-600'
                    }`}
                  />
                ))}
              </div>
              <span className="text-gray-300">{doner.rating}</span>
              <span className="text-gray-400">({doner.reviews} reviews)</span>
            </div>

            <div className="text-3xl font-bold text-blue-400 mb-6">${doner.price}</div>

            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Clock className="w-5 h-5 text-blue-400" />
                <span className="text-sm">{doner.prepTime}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Users className="w-5 h-5 text-green-400" />
                <span className="text-sm">{doner.serves}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Utensils className="w-5 h-5 text-yellow-400" />
                <span className="text-sm">{doner.calories} cal</span>
              </div>
            </div>

            <p className="text-gray-300 mb-6 leading-relaxed">{doner.description}</p>

            <div className="flex items-center gap-4 mb-6">
              <span className="text-gray-300">Quantity:</span>
              <div className="flex items-center border border-gray-600 rounded-lg">
                <button
                  onClick={() => setQuantity(Math.max(1, quantity - 1))}
                  className="p-2 hover:bg-gray-700 transition-colors"
                >
                  <Minus className="w-4 h-4" />
                </button>
                <span className="px-4 py-2 border-x border-gray-600">{quantity}</span>
                <button
                  onClick={() => setQuantity(quantity + 1)}
                  className="p-2 hover:bg-gray-700 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="flex gap-4 mb-4">
              <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg">
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart - ${(doner.price * quantity).toFixed(2)}
              </Button>
              <Button variant="outline" className="px-6 border-gray-600 text-gray-300 hover:bg-gray-700">
                Buy Now
              </Button>
            </div>

            <Button 
              variant="outline" 
              className="w-full mb-8 border-red-400 text-red-400 hover:bg-red-400 hover:text-white transition-colors py-3"
            >
              <Heart className="w-5 h-5 mr-2" />
              Add to Favorites
            </Button>

            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-yellow-400">Allergen Information</h3>
              <div className="flex flex-wrap gap-2">
                {doner.allergens.map((allergen) => (
                  <span key={allergen} className="bg-yellow-600/20 text-yellow-400 px-2 py-1 rounded text-sm">
                    {allergen}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Doner;
