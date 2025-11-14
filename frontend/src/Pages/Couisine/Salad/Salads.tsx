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
  Leaf,
} from "lucide-react";

const Salads = () => {
  const [viewMode, setViewMode] = useState<"grid" | "list">("grid");
  const [searchTerm, setSearchTerm] = useState("");

  const salads = [
    {
      id: 1,
      name: "Mediterranean Salad",
      description:
        "Fresh mixed greens with olives, feta cheese, and olive oil dressing",
      price: 9.99,
      image:
        "https://via.placeholder.com/300x200/1f2937/ffffff?text=Mediterranean+Salad",
      rating: 4.7,
      reviews: 124,
      isPopular: true,
      isVegan: false,
      calories: 280,
    },
    {
      id: 2,
      name: "Shepherd's Salad",
      description:
        "Traditional Turkish salad with tomatoes, cucumbers, and herbs",
      price: 8.99,
      image:
        "https://via.placeholder.com/300x200/1f2937/ffffff?text=Shepherds+Salad",
      rating: 4.6,
      reviews: 89,
      isPopular: false,
      isVegan: true,
      calories: 150,
    },
    {
      id: 3,
      name: "Quinoa Power Bowl",
      description:
        "Nutritious quinoa with roasted vegetables and tahini dressing",
      price: 12.99,
      image:
        "https://via.placeholder.com/300x200/1f2937/ffffff?text=Quinoa+Bowl",
      rating: 4.8,
      reviews: 156,
      isPopular: true,
      isVegan: true,
      calories: 420,
    },
    {
      id: 4,
      name: "Grilled Chicken Salad",
      description:
        "Fresh greens topped with grilled chicken breast and avocado",
      price: 13.99,
      image:
        "https://via.placeholder.com/300x200/1f2937/ffffff?text=Chicken+Salad",
      rating: 4.5,
      reviews: 98,
      isPopular: false,
      isVegan: false,
      calories: 380,
    },
  ];

  const filteredSalads = salads.filter((salad) =>
    salad.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <section className="relative py-20 bg-gradient-to-r from-gray-800 to-gray-900">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-6">
            <Leaf className="w-12 h-12 text-blue-400" />
            <h1 className="text-5xl md:text-6xl font-bold text-blue-400">
              Salads
            </h1>
          </div>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto">
            Fresh, healthy, and delicious salads made with the finest
            ingredients. Perfect for a light meal or as a healthy side dish.
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
                placeholder="Search salads..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-gray-900 border-gray-600 text-white placeholder-gray-400"
              />
            </div>
            <div className="flex border border-gray-600 rounded-lg overflow-hidden">
              <button
                onClick={() => setViewMode("grid")}
                className={`p-2 ${
                  viewMode === "grid"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-700 text-gray-300"
                }`}
              >
                <Grid3X3 className="w-5 h-5" />
              </button>
              <button
                onClick={() => setViewMode("list")}
                className={`p-2 ${
                  viewMode === "list"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-700 text-gray-300"
                }`}
              >
                <List className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </section>

      <section className="py-12 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <div
            className={`grid gap-6 ${
              viewMode === "grid"
                ? "grid-cols-1 md:grid-cols-2 lg:grid-cols-3"
                : "grid-cols-1"
            }`}
          >
            {filteredSalads.map((salad) => (
              <Card
                key={salad.id}
                className={`bg-gray-800 border-gray-700 hover:border-blue-500 overflow-hidden hover:transform hover:scale-105 transition-all duration-300 ${
                  viewMode === "list" ? "flex" : ""
                }`}
              >
                <div
                  className={`relative ${
                    viewMode === "list" ? "w-64 flex-shrink-0" : ""
                  }`}
                >
                  <img
                    src={salad.image}
                    alt={salad.name}
                    className={`object-cover ${
                      viewMode === "list" ? "w-full h-full" : "w-full h-48"
                    }`}
                  />
                  {salad.isPopular && (
                    <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Popular
                    </div>
                  )}
                  {salad.isVegan && (
                    <div className="absolute top-2 right-2 bg-green-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                      Vegan
                    </div>
                  )}
                  <div className="absolute bottom-2 left-2 bg-gray-900/80 text-white px-2 py-1 rounded-full text-xs">
                    {salad.calories} cal
                  </div>
                </div>

                <CardContent
                  className={`p-6 ${viewMode === "list" ? "flex-1" : ""}`}
                >
                  <div className="flex items-start justify-between mb-2">
                    <h3 className="text-xl font-semibold text-white">
                      {salad.name}
                    </h3>
                    <button className="text-gray-400 hover:text-red-400 transition-colors">
                      <Heart className="w-5 h-5" />
                    </button>
                  </div>

                  <p className="text-gray-400 mb-3 text-sm">
                    {salad.description}
                  </p>

                  <div className="flex items-center gap-2 mb-3">
                    <div className="flex items-center">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          className={`w-4 h-4 ${
                            i < Math.floor(salad.rating)
                              ? "text-yellow-400 fill-current"
                              : "text-gray-600"
                          }`}
                        />
                      ))}
                    </div>
                    <span className="text-sm text-gray-400">
                      {salad.rating} ({salad.reviews} reviews)
                    </span>
                  </div>

                  <div className="text-2xl font-bold text-blue-400 mb-4">
                    ${salad.price}
                  </div>

                  <div className="flex gap-2 mb-3">
                    <Button className="flex-1 bg-blue-600 hover:bg-blue-700 text-white">
                      <ShoppingCart className="w-4 h-4 mr-2" />
                      Add to Cart
                    </Button>
                    <Link
                      to={`/salads/${salad.id}`}
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

export default Salads;
