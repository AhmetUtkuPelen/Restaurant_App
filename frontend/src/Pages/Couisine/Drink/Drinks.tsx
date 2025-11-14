

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
  Coffee
} from "lucide-react";

const Drinks = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');

  const drinks = [
    {
      id: 1,
      name: "Turkish Tea",
      description: "Traditional black tea served in authentic tulip glasses",
      price: 3.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Turkish+Tea",
      rating: 4.7,
      reviews: 89,
      isPopular: true,
      category: "Hot Drinks",
      size: "Regular"
    },
    {
      id: 2,
      name: "Fresh Orange Juice",
      description: "Freshly squeezed orange juice, no added sugar",
      price: 5.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Orange+Juice",
      rating: 4.8,
      reviews: 124,
      isPopular: false,
      category: "Fresh Juices",
      size: "Large"
    },
    {
      id: 3,
      name: "Ayran",
      description: "Traditional yogurt drink with salt and mint",
      price: 4.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Ayran",
      rating: 4.6,
      reviews: 67,
      isPopular: true,
      category: "Traditional",
      size: "Regular"
    },
    {
      id: 4,
      name: "Turkish Coffee",
      description: "Rich and aromatic coffee prepared in traditional style",
      price: 6.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Turkish+Coffee",
      rating: 4.9,
      reviews: 156,
      isPopular: true,
      category: "Hot Drinks",
      size: "Small"
    },
    {
      id: 5,
      name: "Pomegranate Juice",
      description: "Antioxidant-rich pomegranate juice, freshly made",
      price: 7.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Pomegranate",
      rating: 4.5,
      reviews: 78,
      isPopular: false,
      category: "Fresh Juices",
      size: "Regular"
    },
    {
      id: 6,
      name: "Mint Lemonade",
      description: "Refreshing lemonade with fresh mint leaves",
      price: 5.49,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Mint+Lemonade",
      rating: 4.4,
      reviews: 92,
      isPopular: false,
      category: "Cold Drinks",
      size: "Large"
    }
  ];

  const filteredDrinks = drinks.filter(drink =>
    drink.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Coffee className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl md:text-6xl font-bold text-blue-400">Drinks</h1>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Refresh yourself with our selection of traditional and modern beverages, 
            from authentic Turkish tea to fresh fruit juices.
          </p>
        </div>
      </section>

      <section className="py-8 bg-gray-800 border-b border-gray-700">
        <div className="max-w-6xl mx-auto px-4">
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <Input
                type="text"
                placeholder="Search drinks..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-gray-900 border-gray-600 text-white placeholder-gray-400"
              />
            </div>
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
      </section>

      <section className="py-12 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
              : 'grid-cols-1'
          }`}>
            {filteredDrinks.map((drink) => (
              <Card
                key={drink.id}
                className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-64 flex-shrink-0' : ''}`}>
                  <img
                    src={drink.image}
                    alt={drink.name}
                    className={`object-cover ${
                      viewMode === 'list' ? 'w-full h-full' : 'w-full h-48'
                    }`}
                  />
                  {drink.isPopular && (
                    <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Popular
                    </div>
                  )}
                  <div className="absolute bottom-2 left-2 bg-gray-900/80 text-white px-2 py-1 rounded-full text-xs">
                    {drink.size}
                  </div>
                </div>

                <CardContent className={`p-6 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-white">{drink.name}</h3>
                    <button className="text-gray-400 hover:text-red-400 transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </div>

                  <p className="text-gray-400 mb-3 text-sm">{drink.description}</p>
                  <p className="text-blue-400 text-sm mb-3">{drink.category}</p>

                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < Math.floor(drink.rating)
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-600'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-400">
                      {drink.rating} ({drink.reviews} reviews)
                    </span>
                  </div>

                  <div className="text-2xl font-bold text-blue-400 mb-4">${drink.price}</div>

                  <div className="flex gap-2 mb-3">
                    <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      Add to Cart
                    </Button>
                    <Link
                      to={`/drinks/${drink.id}`}
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

export default Drinks;