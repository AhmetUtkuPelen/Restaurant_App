

import { useState } from "react";
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
  Utensils
} from "lucide-react";

const Doners = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');

  const doners = [
    {
      id: 1,
      name: "Classic Chicken Doner",
      description: "Tender marinated chicken served in fresh pita bread with vegetables",
      price: 12.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Chicken+Doner",
      rating: 4.8,
      reviews: 156,
      isPopular: true,
      spiceLevel: "Mild",
      ingredients: ["Chicken", "Pita bread", "Tomatoes", "Onions", "Lettuce"]
    },
    {
      id: 2,
      name: "Lamb Doner Wrap",
      description: "Succulent lamb doner with traditional spices in a warm wrap",
      price: 15.99,
      originalPrice: 17.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Lamb+Doner",
      rating: 4.9,
      reviews: 203,
      isPopular: true,
      spiceLevel: "Medium",
      ingredients: ["Lamb", "Tortilla wrap", "Yogurt sauce", "Cucumber", "Red onion"]
    },
    {
      id: 3,
      name: "Mixed Doner Plate",
      description: "Combination of chicken and lamb doner with rice and salad",
      price: 18.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Mixed+Doner",
      rating: 4.7,
      reviews: 124,
      isPopular: false,
      spiceLevel: "Medium",
      ingredients: ["Chicken", "Lamb", "Rice", "Mixed salad", "Garlic sauce"]
    },
    {
      id: 4,
      name: "Vegetarian Doner",
      description: "Plant-based protein with fresh vegetables and tahini sauce",
      price: 11.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Veggie+Doner",
      rating: 4.5,
      reviews: 89,
      isPopular: false,
      spiceLevel: "Mild",
      ingredients: ["Plant protein", "Pita bread", "Tahini", "Vegetables", "Herbs"]
    },
    {
      id: 5,
      name: "Spicy Beef Doner",
      description: "Marinated beef with hot spices and fresh accompaniments",
      price: 14.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Beef+Doner",
      rating: 4.6,
      reviews: 167,
      isPopular: true,
      spiceLevel: "Hot",
      ingredients: ["Beef", "Pita bread", "Hot sauce", "Pickles", "Cabbage"]
    },
    {
      id: 6,
      name: "Doner Box",
      description: "Doner meat served over fries with special sauce",
      price: 13.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Doner+Box",
      rating: 4.4,
      reviews: 98,
      isPopular: false,
      spiceLevel: "Medium",
      ingredients: ["Mixed meat", "French fries", "Special sauce", "Cheese", "Jalapeños"]
    }
  ];

  const filteredDoners = doners.filter(doner =>
    doner.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getSpiceLevelColor = (level: string) => {
    switch (level) {
      case 'Mild': return 'text-green-400';
      case 'Medium': return 'text-yellow-400';
      case 'Hot': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Utensils className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl md:text-6xl font-bold text-blue-400">
              Doners
            </h1>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Savor our authentic doner kebabs made with premium meats, 
            traditional spices, and served with fresh accompaniments.
          </p>
        </div>
      </section>

      {/* Filters and Search */}
      <section className="py-8 bg-gray-800 border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder="Search doners..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-gray-900 border-gray-600 text-white placeholder-gray-400"
              />
            </div>

            {/* Sort and View Controls */}
            <div className="flex items-center gap-4">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
              >
                <option value="name">Sort by Name</option>
                <option value="price">Sort by Price</option>
                <option value="rating">Sort by Rating</option>
                <option value="popular">Popular First</option>
                <option value="spice">Sort by Spice Level</option>
              </select>

              <div className="flex border border-gray-600 rounded-lg overflow-hidden">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`p-2 ${viewMode === 'grid' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
                >
                  <Grid3X3 className="w-5 h-5" />
                </button>
                <button
                  onClick={() => setViewMode('list')}
                  className={`p-2 ${viewMode === 'list' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}`}
                >
                  <List className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Products Grid/List */}
      <section className="py-12 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
              : 'grid-cols-1'
          }`}>
            {filteredDoners.map((doner) => (
              <Card
                key={doner.id}
                className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-64 flex-shrink-0' : ''}`}>
                  <img
                    src={doner.image}
                    alt={doner.name}
                    className={`object-cover ${
                      viewMode === 'list' ? 'w-full h-full' : 'w-full h-48'
                    }`}
                  />
                  {doner.isPopular && (
                    <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Popular
                    </div>
                  )}
                  {doner.originalPrice && (
                    <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Sale
                    </div>
                  )}
                  <div className={`absolute bottom-2 left-2 px-2 py-1 rounded-full text-xs font-medium ${getSpiceLevelColor(doner.spiceLevel)} bg-gray-900/80`}>
                    🌶️ {doner.spiceLevel}
                  </div>
                </div>

                <CardContent className={`p-6 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-white">{doner.name}</h3>
                    <button className="text-gray-400 hover:text-red-400 transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </div>

                  <p className="text-gray-400 mb-3 text-sm">{doner.description}</p>

                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < Math.floor(doner.rating)
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-600'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-400">
                      {doner.rating} ({doner.reviews} reviews)
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-2xl font-bold text-blue-400">
                      ${doner.price}
                    </span>
                    {doner.originalPrice && (
                      <span className="text-lg text-gray-500 line-through">
                        ${doner.originalPrice}
                      </span>
                    )}
                  </div>

                  <div className="flex gap-2 mb-3">
                    <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      Add to Cart
                    </Button>
                    <Link
                      to={`/doners/${doner.id}`}
                      className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors text-center"
                    >
                      View Details
                    </Link>
                  </div>
                  
                  <Button 
                    variant="outline" 
                    className="w-full border-red-400 text-red-400 hover:bg-red-400 hover:text-white transition-colors"
                  >
                    <Heart className="w-4 h-4 mr-2" />
                    Add to Favorites
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Doners;
