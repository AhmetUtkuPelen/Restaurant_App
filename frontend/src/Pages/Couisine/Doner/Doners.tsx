

import { useState } from "react";
import { useDoners } from "@/hooks/useProducts";
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
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useFavouriteStore } from "@/Zustand/FavouriteProduct/FavouriteProductState";

const Doners = () => {
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('name');

  const { data: doners = [], isLoading, error } = useDoners();
  const addToCart = useCartStore((state) => state.addToCart);
  const addToFavourites = useFavouriteStore((state) => state.addToFavourites);
  const removeFromFavourites = useFavouriteStore((state) => state.removeFromFavourites);
  const isFavourite = useFavouriteStore((state) => state.isFavourite);

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
          {isLoading && (
            <div className="flex justify-center items-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
            </div>
          )}

          {error && (
            <div className="bg-red-900/50 border border-red-500 text-red-200 px-4 py-3 rounded mb-6">
              {error instanceof Error ? error.message : "Failed to load doners"}
            </div>
          )}

          {!isLoading && !error && filteredDoners.length === 0 && (
            <div className="text-center py-20">
              <p className="text-gray-400 text-lg">No doners found</p>
            </div>
          )}

          {!isLoading && !error && filteredDoners.length > 0 && (
          <div className={`grid gap-6 ${
            viewMode === 'grid' 
              ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
              : 'grid-cols-1'
          }`}>
            {filteredDoners.map((doner) => {
              const donerData = doner as typeof doner & { discount_percentage?: string; final_price?: string; image_url?: string; image?: string; is_front_page?: boolean; isPopular?: boolean; originalPrice?: number; comments?: unknown[]; reviews?: number; spiceLevel?: string };
              const hasDiscount = donerData.discount_percentage && parseFloat(donerData.discount_percentage) > 0;
              const price = parseFloat(String(doner.price || "0"));
              const finalPrice = parseFloat(donerData.final_price || String(doner.price || "0"));
              const spiceLevel = (doner as typeof doner & { spice_level?: string }).spice_level || donerData.spiceLevel || "MEDIUM";
              
              return (
              <Card
                key={doner.id}
                className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                  viewMode === 'list' ? 'flex' : ''
                }`}
              >
                <div className={`relative ${viewMode === 'list' ? 'w-64 flex-shrink-0' : ''}`}>
                  <img
                    src={donerData.image_url || donerData.image || "https://via.placeholder.com/300x200/1f2937/ffffff?text=Doner"}
                    alt={doner.name}
                    className={`object-cover ${
                      viewMode === 'list' ? 'w-full h-full' : 'w-full h-48'
                    }`}
                  />
                  {(donerData.is_front_page || donerData.isPopular) && (
                    <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Popular
                    </div>
                  )}
                  {(hasDiscount || donerData.originalPrice) && (
                    <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Sale
                    </div>
                  )}
                  <div className={`absolute bottom-2 left-2 px-2 py-1 rounded-full text-xs font-medium ${getSpiceLevelColor(spiceLevel)} bg-gray-900/80`}>
                    🌶️ {spiceLevel}
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
                            i < 4
                              ? 'text-yellow-400 fill-current'
                              : 'text-gray-600'
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-400">
                      4.5 ({(donerData.comments as unknown[])?.length || donerData.reviews || 0} reviews)
                    </span>
                  </div>

                  <div className="flex items-center gap-2 mb-4">
                    <span className="text-2xl font-bold text-blue-400">
                      ${finalPrice.toFixed(2)}
                    </span>
                    {hasDiscount && (
                      <span className="text-lg text-gray-500 line-through">
                        ${price.toFixed(2)}
                      </span>
                    )}
                  </div>

                  <div className="flex gap-2 mb-3">
                    <Button 
                      className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
                      onClick={() => addToCart({
                        id: doner.id,
                        name: doner.name,
                        price: doner.price,
                        final_price: doner.final_price,
                        image_url: doner.image_url,
                        category: "doner"
                      })}
                    >
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
                          description: doner.description
                        });
                      }
                    }}
                    className={`w-full transition-colors ${
                      isFavourite(doner.id)
                        ? "border-red-400 bg-red-400 text-white hover:bg-red-500"
                        : "border-red-400 text-red-400 hover:bg-red-400 hover:text-white"
                    }`}
                  >
                    <Heart className={`w-4 h-4 mr-2 ${isFavourite(doner.id) ? "fill-current" : ""}`} />
                    {isFavourite(doner.id) ? "Remove from Favorites" : "Add to Favorites"}
                  </Button>
                </CardContent>
              </Card>
            )})}
          </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Doners;
