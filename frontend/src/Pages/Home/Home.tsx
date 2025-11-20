import { Button } from "@/Components/ui/button";
import { Card, CardContent } from "@/Components/ui/card";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from "@/Components/ui/carousel";
import { Beef, ChefHat, Clock, Dessert, Drumstick, GlassWater, MapPin, Phone, Salad, Star, Utensils } from "lucide-react";
import RestaurantImg from "../../assets/restaurant.png";
import { useFrontPageProducts } from "@/hooks/useProducts";
import { Link } from "react-router-dom";

const Home = () => {
  const { data: frontPageProducts = [], isLoading } = useFrontPageProducts();

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

  type Product_Categories_Links_Names_Icons = {
    name : string;
    Icon : React.ElementType;
    link : string;
  }
  
  const products : Product_Categories_Links_Names_Icons[] = [
    {
      name: "Desserts",
      Icon: Dessert,
      link: "/desserts",
    },
    {
      name: "Drinks",
      Icon: GlassWater,
      link: "/drinks",
    },
    {
      name: "Salads",
      Icon: Salad,
      link: "/salads",
    },
    {
      name: "Doners",
      Icon : Beef,
      link: "/doners",
    },
    {
      name: "Kebabs",
      Icon : Drumstick,
      link: "/kebabs",
    },
  ];

  // Get product link based on categories \\
  const getProductLink = (category: string, id: number) => {
    const categoryMap: { [key: string]: string } = {
      dessert: "desserts",
      doner: "doners",
      drink: "drinks",
      kebab: "kebabs",
      salad: "salads",
    };
    return `/${categoryMap[category] || category}/${id}`;
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">

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
            Authentic Cuisine
          </p>
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-8 text-gray-400">
            <div className="flex items-center gap-2">
              <MapPin className="w-5 h-5" />
              <span>123 Food Street, City Center</span>
            </div>
            <div className="flex items-center gap-2">
              <Phone className="w-5 h-5" />
              <span>+1 (111) 111-11 11</span>
            </div>
          </div>
          <div className="flex gap-4 justify-center">
            <Button className="bg-blue-600  hover:text-blue-600 text-white px-8 py-3 text-lg"
            variant="outline"
            >
              <Link to="/cart">
                Order Now
              </Link>
            </Button>
    <Link to="/reservation">
                    <Button
              variant="outline"
              className="bg-blue-600 hover:text-blue-600 text-white px-8 py-3 text-lg"
            >
              <Link to="/reservation">
                Make A Reservation
              </Link>
            </Button>
    </Link>
          </div>
        </div>
      </section>

      {/* Features */}
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
                  <h3 className="text-xl font-semibold mb-2 text-white">
                    {feature.title}
                  </h3>
                  <p className="text-gray-400">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Products */}
      <section className="py-20 bg-gray-900">
        <div className="max-w-6xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Our Menu Categories
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
{products.map((product, index) => {
  const Icon = product.Icon;

  return (
    <Link key={index} to={product.link}>
      <Card className="group cursor-pointer bg-gray-800 border-gray-700 hover:bg-gray-700 transition-colors overflow-hidden p-6 flex flex-col items-center space-y-4">
        
        <Icon className="w-12 h-12 text-blue-200 group-hover:scale-110 transition-transform" />

        <CardContent className="p-0">
          <h3 className="text-lg font-semibold text-center text-blue-500 uppercase">
            {product.name}
          </h3>
        </CardContent>

      </Card>
    </Link>
  );
})}
          </div>
        </div>
      </section>

      {/* Featured Dishes */}
      <section className="py-20 bg-gray-800">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-16 text-blue-400">
            Featured Dishes
          </h2>

          {isLoading && (
            <div className="flex justify-center items-center py-20">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
            </div>
          )}

          {!isLoading && frontPageProducts.length === 0 && (
            <div className="text-center py-20">
              <p className="text-gray-400 text-lg">
                No featured dishes available at the moment
              </p>
            </div>
          )}

          {/* Featured Products Carousel */}
          {!isLoading && frontPageProducts.length > 0 && (
            <Carousel
              opts={{
                align: "start",
                loop: true,
              }}
              className="w-full"
            >
              <CarouselContent className="-ml-2 md:-ml-4">
                {frontPageProducts.map((product) => {
                  const hasDiscount =
                    parseFloat(product.discount_percentage || "0") > 0;
                  const finalPrice = parseFloat(
                    product.final_price || product.price || "0"
                  );
                  const originalPrice = parseFloat(product.price || "0");

                  return (
                    <CarouselItem
                      key={product.id}
                      className="pl-2 md:pl-4 md:basis-1/2 lg:basis-1/3 xl:basis-1/4"
                    >
                      <Card className="bg-gray-900 border-gray-700 overflow-hidden hover:transform hover:scale-105 transition-all duration-300">
                        <Link to={getProductLink(product.category, product.id)}>
                          <div className="relative">
                            <img
                              src={
                                product.image_url ||
                                "https://via.placeholder.com/400x300/1f2937/ffffff?text=Product"
                              }
                              alt={product.name}
                              className="w-full h-48 object-cover"
                            />
                            {hasDiscount && (
                              <div className="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                                Sale
                              </div>
                            )}
                            <div className="absolute top-2 left-2 bg-blue-600 text-white px-2 py-1 rounded-full text-xs font-medium">
                              Featured
                            </div>
                          </div>
                          <CardContent className="p-4">
                            <h3 className="text-lg font-semibold mb-2 text-white truncate">
                              {product.name}
                            </h3>
                            <p className="text-gray-400 text-sm mb-3 line-clamp-2">
                              {product.description}
                            </p>
                            <div className="flex items-center gap-2 mb-3">
                              <p className="text-blue-400 font-bold text-xl">
                                ${finalPrice.toFixed(2)}
                              </p>
                              {hasDiscount && (
                                <p className="text-gray-500 line-through text-sm">
                                  ${originalPrice.toFixed(2)}
                                </p>
                              )}
                            </div>
                            <Button className="w-full bg-blue-600 hover:bg-blue-700">
                              View Details
                            </Button>
                          </CardContent>
                        </Link>
                      </Card>
                    </CarouselItem>
                  );
                })}
              </CarouselContent>
              <CarouselPrevious className="hidden md:flex -left-12 bg-gray-900 border-gray-700 text-white hover:bg-gray-700" />
              <CarouselNext className="hidden md:flex -right-12 bg-gray-900 border-gray-700 text-white hover:bg-gray-700" />
            </Carousel>
          )}
        </div>
      </section>
    </div>
  );
};

export default Home;