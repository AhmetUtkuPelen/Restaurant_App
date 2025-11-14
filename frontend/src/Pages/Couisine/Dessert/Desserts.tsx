

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
  ChefHat
} from "lucide-react";

const Desserts = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');

  const desserts = [
    {
      id: 1,
      name: "Baklava",
      description: "Traditional Turkish pastry with honey and nuts",
      price: 8.99,
      originalPrice: 10.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Baklava",
      rating: 4.8,
      reviews: 124,
      isPopular: true,
      ingredients: ["Phyllo dough", "Honey", "Pistachios", "Walnuts"]
    },
    {
      id: 2,
      name: "Tiramisu",
      description: "Classic Italian coffee-flavored dessert",
      price: 12.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Tiramisu",
      rating: 4.9,
      reviews: 89,
      isPopular: false,
      ingredients: ["Mascarpone", "Coffee", "Ladyfingers", "Cocoa"]
    },
    {
      id: 3,
      name: "Kunefe",
      description: "Sweet cheese pastry soaked in syrup",
      price: 9.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Kunefe",
      rating: 4.7,
      reviews: 156,
      isPopular: true,
      ingredients: ["Cheese", "Kadayif", "Sugar syrup", "Pistachios"]
    },
    {
      id: 4,
      name: "Chocolate Lava Cake",
      description: "Warm chocolate cake with molten center",
      price: 11.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Lava+Cake",
      rating: 4.6,
      reviews: 203,
      isPopular: false,
      ingredients: ["Dark chocolate", "Butter", "Eggs", "Vanilla"]
    },
    {
      id: 5,
      name: "Rice Pudding",
      description: "Creamy traditional rice pudding with cinnamon",
      price: 6.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Rice+Pudding",
      rating: 4.5,
      reviews: 78,
      isPopular: false,
      ingredients: ["Rice", "Milk", "Sugar", "Cinnamon"]
    },
    {
      id: 6,
      name: "Cheesecake",
      description: "New York style cheesecake with berry compote",
      price: 13.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Cheesecake",
      rating: 4.8,
      reviews: 167,
      isPopular: true,
      ingredients: ["Cream cheese", "Graham crackers", "Berries", "Sugar"]
    }
  ];

  const filteredDesserts = desserts.filter(dessert =>
    dessert.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Hero Section */}
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <ChefHat className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl md:text-6xl font-bold text-blue-400">
              Desserts
            </h1>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Indulge in our exquisite collection of traditional and modern desserts, 
            crafted with the finest ingredients and authentic recipes.
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
                placeholder="Search desserts..."
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
            {filteredDesserts.map((dessert) => (
              <Card
                key={dessert.id}
                className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-64 flex-shrink-0' : ''}`}>
                  <img
                    src={dessert.image}
                    alt={dessert.name}
                    className={`object-cover ${
                      viewMode === 'list' ? 'w-full h-full' : 'w-full h-48'
                    }`}
                  />
                  {dessert.isPopular && (
                    <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Popular
                    </div>
                  )}
                  {dessert.originalPrice && (
                    <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Sale
                    </div>
                  )}
                </div>

                <CardContent className={`p-6 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-white">{dessert.name}</h3>
                    <button className="text-gray-400 hover:text-red-400 transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </div>

                  <p className="text-gray-400 mb-3 text-sm">{dessert.description}</p>

                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < Math.floor(dessert.rating)
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-600'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-400">
                      {dessert.rating} ({dessert.reviews} reviews)
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-2xl font-bold text-blue-400">
                      ${dessert.price}
                    </span>
                    {dessert.originalPrice && (
                      <span className="text-lg text-gray-500 line-through">
                        ${dessert.originalPrice}
                      </span>
                    )}
                  </div>

                  <div className="flex gap-2 mb-3">
                    <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      Add to Cart
                    </Button>
                    <Link
                      to={`/desserts/${dessert.id}`}
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

export default Desserts;