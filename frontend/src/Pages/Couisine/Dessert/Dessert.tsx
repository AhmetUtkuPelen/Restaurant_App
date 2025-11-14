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
  ChefHat,
  Award,
} from "lucide-react";

const Dessert = () => {
  // const { id } = useParams();
  const [quantity, setQuantity] = useState(1);
  const [selectedImage, setSelectedImage] = useState(0);
  const [isFavorite, setIsFavorite] = useState(false);

  // Mock data - in real app, fetch based on id
  const dessert = {
    id: 1,
    name: "Baklava",
    description:
      "Traditional Turkish pastry made with layers of phyllo dough, filled with chopped nuts and sweetened with honey syrup. A perfect blend of crispy texture and rich flavors that will transport you to the Mediterranean.",
    price: 8.99,
    originalPrice: 10.99,
    images: [
      "https://via.placeholder.com/600x400/1f2937/ffffff?text=Baklava+Main",
      "https://via.placeholder.com/600x400/1f2937/ffffff?text=Baklava+Side",
      "https://via.placeholder.com/600x400/1f2937/ffffff?text=Baklava+Close",
    ],
    rating: 4.8,
    reviews: 124,
    prepTime: "15 mins",
    serves: "2-3 people",
    calories: 320,
    isPopular: true,
    ingredients: [
      "Phyllo dough",
      "Mixed nuts (pistachios, walnuts)",
      "Honey",
      "Butter",
      "Sugar syrup",
      "Cinnamon",
    ],
    nutritionFacts: {
      calories: 320,
      protein: "8g",
      carbs: "45g",
      fat: "14g",
      fiber: "3g",
    },
    allergens: ["Nuts", "Gluten", "Dairy"],
    category: "Traditional Desserts",
  };

  const relatedDesserts = [
    {
      id: 2,
      name: "Kunefe",
      price: 9.99,
      image: "https://via.placeholder.com/200x150/1f2937/ffffff?text=Kunefe",
      rating: 4.7,
    },
    {
      id: 3,
      name: "Rice Pudding",
      price: 6.99,
      image:
        "https://via.placeholder.com/200x150/1f2937/ffffff?text=Rice+Pudding",
      rating: 4.5,
    },
    {
      id: 4,
      name: "Tiramisu",
      price: 12.99,
      image: "https://via.placeholder.com/200x150/1f2937/ffffff?text=Tiramisu",
      rating: 4.9,
    },
  ];

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
          {/* Product Images */}
          <div>
            <div className="relative mb-4">
              <img
                src={dessert.images[selectedImage]}
                alt={dessert.name}
                className="w-full h-96 object-cover rounded-lg"
              />
              {dessert.isPopular && (
                <div className="absolute top-4 left-4 bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  Popular Choice
                </div>
              )}
              {dessert.originalPrice && (
                <div className="absolute top-4 right-4 bg-red-600 text-white px-3 py-1 rounded-full text-sm font-medium">
                  On Sale
                </div>
              )}
            </div>

            {/* Image Thumbnails */}
            <div className="flex gap-2">
              {dessert.images.map((image, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedImage(index)}
                  className={`w-20 h-20 rounded-lg overflow-hidden border-2 transition-colors ${
                    selectedImage === index
                      ? "border-blue-400"
                      : "border-gray-600"
                  }`}
                >
                  <img
                    src={image}
                    alt={`${dessert.name} ${index + 1}`}
                    className="w-full h-full object-cover"
                  />
                </button>
              ))}
            </div>
          </div>

          {/* Product Details */}
          <div>
            <div className="flex items-start justify-between mb-4">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">
                  {dessert.name}
                </h1>
                <p className="text-gray-400 mb-4">{dessert.category}</p>
              </div>
              <button
                onClick={() => setIsFavorite(!isFavorite)}
                className={`p-2 rounded-full transition-colors ${
                  isFavorite
                    ? "text-red-400 bg-red-400/20"
                    : "text-gray-400 hover:text-red-400"
                }`}
              >
                <Heart
                  className={`w-6 h-6 ${isFavorite ? "fill-current" : ""}`}
                />
              </button>
            </div>

            {/* Rating */}
            <div className="flex items-center gap-4 mb-6">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <Star
                    key={i}
                    className={`w-5 h-5 ${
                      i < Math.floor(dessert.rating)
                        ? "text-yellow-400 fill-current"
                        : "text-gray-600"
                    }`}
                  />
                ))}
              </div>
              <span className="text-gray-300">{dessert.rating}</span>
              <span className="text-gray-400">({dessert.reviews} reviews)</span>
            </div>

            {/* Price */}
            <div className="flex items-center gap-3 mb-6">
              <span className="text-3xl font-bold text-blue-400">
                ${dessert.price}
              </span>
              {dessert.originalPrice && (
                <span className="text-xl text-gray-500 line-through">
                  ${dessert.originalPrice}
                </span>
              )}
              {dessert.originalPrice && (
                <span className="bg-red-600 text-white px-2 py-1 rounded text-sm">
                  Save ${(dessert.originalPrice - dessert.price).toFixed(2)}
                </span>
              )}
            </div>

            {/* Quick Info */}
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="flex items-center gap-2 text-gray-400">
                <Clock className="w-5 h-5 text-blue-400" />
                <span className="text-sm">{dessert.prepTime}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-400">
                <Users className="w-5 h-5 text-green-400" />
                <span className="text-sm">{dessert.serves}</span>
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

            {/* Action Buttons */}
            <div className="flex gap-4 mb-4">
              <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-3 text-lg">
                <ShoppingCart className="w-5 h-5 mr-2" />
                Add to Cart - ${(dessert.price * quantity).toFixed(2)}
              </Button>
              <Button
                variant="outline"
                className="px-6 border-gray-600 text-gray-300 hover:bg-gray-700"
              >
                Buy Now
              </Button>
            </div>

            {/* Add to Favorites Button */}
            <Button 
              variant="outline" 
              className="w-full mb-8 border-red-400 text-red-400 hover:bg-red-400 hover:text-white transition-colors py-3"
            >
              <Heart className="w-5 h-5 mr-2" />
              Add to Favorites
            </Button>

            {/* Allergen Info */}
            <div className="bg-gray-800 rounded-lg p-4">
              <h3 className="font-semibold mb-2 text-yellow-400">
                Allergen Information
              </h3>
              <div className="flex flex-wrap gap-2">
                {dessert.allergens.map((allergen) => (
                  <span
                    key={allergen}
                    className="bg-yellow-600/20 text-yellow-400 px-2 py-1 rounded text-sm"
                  >
                    {allergen}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Tabs Section */}
        <div className="mt-16">
          <div className="border-b border-gray-700">
            <nav className="flex space-x-8">
              <button className="py-4 px-1 border-b-2 border-blue-400 text-blue-400 font-medium">
                Ingredients
              </button>
              <button className="py-4 px-1 text-gray-400 hover:text-white">
                Nutrition Facts
              </button>
              <button className="py-4 px-1 text-gray-400 hover:text-white">
                Reviews ({dessert.reviews})
              </button>
            </nav>
          </div>

          <div className="py-8">
            {/* Ingredients Tab */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div>
                <h3 className="text-xl font-semibold mb-4 text-blue-400">
                  Ingredients
                </h3>
                <ul className="space-y-2">
                  {dessert.ingredients.map((ingredient, index) => (
                    <li
                      key={index}
                      className="flex items-center gap-2 text-gray-300"
                    >
                      <ChefHat className="w-4 h-4 text-blue-400" />
                      {ingredient}
                    </li>
                  ))}
                </ul>
              </div>

              <div>
                <h3 className="text-xl font-semibold mb-4 text-blue-400">
                  Nutrition Facts
                </h3>
                <div className="bg-gray-800 rounded-lg p-4">
                  <div className="grid grid-cols-2 gap-4">
                    {Object.entries(dessert.nutritionFacts).map(
                      ([key, value]) => (
                        <div key={key} className="flex justify-between">
                          <span className="text-gray-400 capitalize">
                            {key}:
                          </span>
                          <span className="text-white font-medium">
                            {value}
                          </span>
                        </div>
                      )
                    )}
                  </div>
                </div>
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
            {relatedDesserts.map((item) => (
              <Link
                key={item.id}
                to={`/dessert/${item.id}`}
                className="bg-gray-800 rounded-lg overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
              >
                <img
                  src={item.image}
                  alt={item.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-4">
                  <h3 className="font-semibold mb-2">{item.name}</h3>
                  <div className="flex items-center justify-between">
                    <span className="text-blue-400 font-bold">
                      ${item.price}
                    </span>
                    <div className="flex items-center">
                      <Star className="w-4 h-4 text-yellow-400 fill-current" />
                      <span className="text-sm text-gray-400 ml-1">
                        {item.rating}
                      </span>
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
