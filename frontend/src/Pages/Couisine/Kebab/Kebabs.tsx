

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
  Flame
} from "lucide-react";

const Kebabs = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');

  const kebabs = [
    {
      id: 1,
      name: "Adana Kebab",
      description: "Spicy minced lamb kebab grilled on skewers with traditional spices",
      price: 16.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Adana+Kebab",
      rating: 4.9,
      reviews: 203,
      isPopular: true,
      spiceLevel: "Hot"
    },
    {
      id: 2,
      name: "Shish Kebab",
      description: "Tender cubes of marinated lamb with vegetables on skewers",
      price: 18.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Shish+Kebab",
      rating: 4.8,
      reviews: 156,
      isPopular: true,
      spiceLevel: "Medium"
    },
    {
      id: 3,
      name: "Chicken Kebab",
      description: "Marinated chicken breast grilled to perfection with herbs",
      price: 14.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Chicken+Kebab",
      rating: 4.7,
      reviews: 124,
      isPopular: false,
      spiceLevel: "Mild"
    },
    {
      id: 4,
      name: "Mixed Grill",
      description: "Combination of lamb, chicken, and beef kebabs with rice",
      price: 22.99,
      originalPrice: 25.99,
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Mixed+Grill",
      rating: 4.8,
      reviews: 189,
      isPopular: true,
      spiceLevel: "Medium"
    }
  ];

  const filteredKebabs = kebabs.filter(kebab =>
    kebab.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Flame className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl md:text-6xl font-bold text-blue-400">Kebabs</h1>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Experience the authentic flavors of our premium kebabs, grilled to perfection 
            with traditional spices and served with fresh accompaniments.
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
                placeholder="Search kebabs..."
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
            {filteredKebabs.map((kebab) => (
              <Card
                key={kebab.id}
                className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-64 flex-shrink-0' : ''}`}>
                  <img
                    src={kebab.image}
                    alt={kebab.name}
                    className={`object-cover ${
                      viewMode === 'list' ? 'w-full h-full' : 'w-full h-48'
                    }`}
                  />
                  {kebab.isPopular && (
                    <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Popular
                    </div>
                  )}
                  {kebab.originalPrice && (
                    <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Sale
                    </div>
                  )}
                </div>

                <CardContent className={`p-6 ${viewMode === 'list' ? 'flex-1' : ''}`}>
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-white">{kebab.name}</h3>
                    <button className="text-gray-400 hover:text-red-400 transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </div>

                  <p className="text-gray-400 mb-3 text-sm">{kebab.description}</p>

                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < Math.floor(kebab.rating)
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-600'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-400">
                      {kebab.rating} ({kebab.reviews} reviews)
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-2xl font-bold text-blue-400">${kebab.price}</span>
                    {kebab.originalPrice && (
                      <span className="text-lg text-gray-500 line-through">${kebab.originalPrice}</span>
                    )}
                  </div>

                  <div className="flex gap-2 mb-3">
                    <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      Add to Cart
                    </Button>
                    <Link
                      to={`/kebabs/${kebab.id}`}
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

export default Kebabs;