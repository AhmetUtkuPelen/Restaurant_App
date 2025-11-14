import { Button } from "@/Components/ui/button";
import { Card, CardContent } from "@/Components/ui/card";
import { ChefHat, Clock, MapPin, Phone, Star, Utensils } from "lucide-react";
import RestaurantImg from "../../assets/restaurant.png";

const Home = () => {
  const features = [
    {
      icon: <Utensils className="w-8 h-8" />,
      title: "Online Order",
      description: "Order your favorite meals online with ease",
    },
    {
      icon: <Clock className="w-8 h-8" />,
      title: "Online Reservation",
      description: "Book your table in advance",
    },
    {
      icon: <ChefHat className="w-8 h-8" />,
      title: "Fresh Ingredients",
      description: "We use only the freshest ingredients",
    },
    {
      icon: <Star className="w-8 h-8" />,
      title: "Premium Quality",
      description: "Exceptional quality in every dish",
    },
  ];

  const products = [
    {
      name: "Desserts",
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Desserts",
    },
    {
      name: "Drinks",
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Drinks",
    },
    {
      name: "Salads",
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Salads",
    },
    {
      name: "Doners",
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Doners",
    },
    {
      name: "Kebabs",
      image: "https://via.placeholder.com/300x200/1f2937/ffffff?text=Kebabs",
    },
  ];

  const carouselItems = [
    {
      name: "Special Kebab",
      image:
        "https://via.placeholder.com/400x300/1f2937/ffffff?text=Special+Kebab",
      price: "$24.99",
    },
    {
      name: "Fresh Salad",
      image:
        "https://via.placeholder.com/400x300/1f2937/ffffff?text=Fresh+Salad",
      price: "$12.99",
    },
    {
      name: "Premium Dessert",
      image:
        "https://via.placeholder.com/400x300/1f2937/ffffff?text=Premium+Dessert",
      price: "$8.99",
    },
    {
      name: "Refreshing Drink",
      image:
        "https://via.placeholder.com/400x300/1f2937/ffffff?text=Refreshing+Drink",
      price: "$5.99",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Hero Section */}
      <section
        className="relative h-screen flex items-center justify-center bg-cover bg-center"
        style={{
          backgroundImage: `linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url(${RestaurantImg})`,
        }}
      >
        <div className="text-center max-w-4xl mx-auto px-4">
          <h1 className="text-6xl md:text-8xl font-bold mb-6 text-blue-400">
            Delicious Bites
          </h1>
          <p className="text-xl md:text-2xl mb-4 text-gray-300">
            Authentic Mediterranean Cuisine
          </p>
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-8 text-gray-400">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5" />
              <span>123 Food Street, City Center</span>
            </div>
            <div className="flex items-center gap-2">
              <Phone className="w-5 h-5" />
              <span>+1 (555) 123-4567</span>
            </div>
          </div>
          <div className="flex gap-4 justify-center">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg">
              Order Now
            </Button>
            <Button
              variant="outline"
              className="border-blue-400 text-blue-400 hover:bg-blue-400 hover:text-white px-8 py-3 text-lg"
            >
              Make Reservation
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Why Choose Us
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card
                key={index}
                className="text-center bg-gray-900 border-gray-700 hover:bg-gray-700 transition-colors"
              >
                <CardContent className="pt-6">
                  <div className="text-blue-400 mb-4 flex justify-center">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-white">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Products Section */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Our Menu Categories
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {products.map((product, index) => (
              <Card key={index} className="group cursor-pointer bg-gray-800 border-gray-700 hover:bg-gray-700 transition-colors overflow-hidden">
                <div className="relative">
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                </div>
                <CardContent className="p-4">
                  <h3 className="text-lg font-semibold text-center text-blue-400">
                    {product.name}
                  </h3>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Carousel Section */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Featured Dishes
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {carouselItems.map((item, index) => (
              <Card
                key={index}
                className="bg-gray-900 border-gray-700 overflow-hidden hover:transform hover:scale-105 transition-all duration-300"
              >
                <div className="relative">
                  <img
                    src={item.image}
                    alt={item.name}
                    className="w-full h-48 object-cover"
                  />
                </div>
                <CardContent className="p-4">
                  <h3 className="text-lg font-semibold mb-2 text-white">{item.name}</h3>
                  <p className="text-blue-400 font-bold text-xl mb-3">
                    {item.price}
                  </p>
                  <Button className="w-full bg-blue-600 hover:bg-blue-700">
                    Add to Cart
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

export default Home;
