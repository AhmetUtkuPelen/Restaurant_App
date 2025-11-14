

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
  Flame,
  Clock,
  Users
} from "lucide-react";

const Kebab = () => {
  // const { id } = useParams();
  const [quantity, setQuantity] = useState(1);
  const [isFavorite, setIsFavorite] = useState(false);

  const kebab = {
    id: 1,
    name: "Adana Kebab",
    description: "Authentic Adana kebab made with hand-minced lamb, seasoned with traditional Turkish spices and grilled over charcoal. Served with fresh bread, grilled vegetables, and our signature sauces.",
    price: 16.99,
    image: "https://via.placeholder.com/600x400/1f2937/ffffff?text=Adana+Kebab",
    rating: 4.9,
    reviews: 203,
    prepTime: "20 mins",
    serves: "1-2 people",
    spiceLevel: "Hot",
    isPopular: true,
    ingredients: ["Minced lamb", "Red pepper flakes", "Garlic", "Onions", "Traditional spices"],
    category: "Grilled Kebabs"
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="bg-gray-800 py-4">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex items-center gap-2 text-sm">
            <Link to="/" className="text-gray-400 hover:text-blue-400">Home</Link>
            <span className="text-gray-600">/</span>
            <Link to="/kebabs" className="text-gray-400 hover:text-blue-400">Kebabs</Link>
            <span className="text-gray-600">/</span>
            <span className="text-white">{kebab.name}</span>
          </div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto px-4 py-8">
        <Link
          to="/kebabs"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-6 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Kebabs
        </Link>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <div className="relative mb-4">
              <img
                src={kebab.image}
                alt={kebab.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {kebab.isPopular && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
              <div className="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium flex items-center gap-1">
                <Flame className="w-4 h-4" />
                {kebab.spiceLevel}
              </div>
            </div>
          </div>

          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">{kebab.name}</h1>
                <p className="text-gray-400 mb-4">{kebab.category}</p>
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
                      i < Math.floor(kebab.rating)
                        ? 'text-yellow-400 fill-current'
                        : 'text-gray-600'
                    }`}
                  />
                ))}
              </div>
              <span className="text-gray-300">{kebab.rating}</span>
              <span className="text-gray-400">({kebab.reviews} reviews)</span>
            </div>

            <div className="text-3xl font-bold text-blue-400 mb-6">${kebab.price}</div>

            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Clock className="w-5 h-5 text-blue-400" />
                <span className="text-sm">{kebab.prepTime}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Users className="w-5 h-5 text-green-400" />
                <span className="text-sm">{kebab.serves}</span>
              </div>
            </div>

            <p className="text-gray-300 mb-6 leading-relaxed">{kebab.description}</p>

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
                Add to Cart - ${(kebab.price * quantity).toFixed(2)}
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
              <h3 className="font-semibold mb-2 text-blue-400">Main Ingredients</h3>
              <ul className="space-y-1">
                {kebab.ingredients.map((ingredient, index) => (
                  <li key={index} className="text-gray-300 text-sm">• {ingredient}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Kebab;