import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/Components/ui/card";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Label } from "@/Components/ui/label";
import { Textarea } from "@/Components/ui/textarea";
import { Badge } from "@/Components/ui/badge";
import { Separator } from "@/Components/ui/separator";

import {
  ShoppingCart,
  Plus,
  Minus,
  Trash2,
  Star,
  Clock,
  Utensils,
  Coffee,
  Cookie,
  Salad,
  CheckCircle,
} from "lucide-react";

interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  image: string;
  category: string;
  rating: number;
  prepTime: string;
  ingredients: string[];
  popular: boolean;
}

interface CartItem extends Product {
  quantity: number;
}

interface OrderData {
  customerName: string;
  customerPhone: string;
  customerEmail: string;
  deliveryAddress: string;
  specialInstructions: string;
  paymentMethod: string;
}

const Order = () => {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [activeCategory, setActiveCategory] = useState("all");
  const [orderData, setOrderData] = useState<OrderData>({
    customerName: "",
    customerPhone: "",
    customerEmail: "",
    deliveryAddress: "",
    specialInstructions: "",
    paymentMethod: "card",
  });
  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Mock product data
  const products: Product[] = [
    // Kebabs
    {
      id: "kebab-1",
      name: "Chicken Shish Kebab",
      description: "Tender grilled chicken pieces with Mediterranean spices",
      price: 18.99,
      image:
        "https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba?w=400&h=300&fit=crop",
      category: "kebab",
      rating: 4.8,
      prepTime: "15-20 min",
      ingredients: ["Chicken", "Bell Peppers", "Onions", "Spices"],
      popular: true,
    },
    {
      id: "kebab-2",
      name: "Lamb Adana Kebab",
      description: "Spicy minced lamb kebab with traditional Turkish flavors",
      price: 22.99,
      image:
        "https://images.unsplash.com/photo-1544025162-d76694265947?w=400&h=300&fit=crop",
      category: "kebab",
      rating: 4.9,
      prepTime: "18-25 min",
      ingredients: ["Ground Lamb", "Spices", "Herbs", "Garlic"],
      popular: true,
    },
    // Doners
    {
      id: "doner-1",
      name: "Chicken Doner Wrap",
      description: "Sliced chicken doner in fresh lavash with vegetables",
      price: 12.99,
      image:
        "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400&h=300&fit=crop",
      category: "doner",
      rating: 4.6,
      prepTime: "8-12 min",
      ingredients: ["Chicken Doner", "Lavash", "Tomatoes", "Onions", "Sauce"],
      popular: false,
    },
    {
      id: "doner-2",
      name: "Mixed Doner Plate",
      description: "Combination of chicken and lamb doner with rice and salad",
      price: 16.99,
      image:
        "https://images.unsplash.com/photo-1574894709920-11b28e7367e3?w=400&h=300&fit=crop",
      category: "doner",
      rating: 4.7,
      prepTime: "12-15 min",
      ingredients: ["Chicken Doner", "Lamb Doner", "Rice", "Salad"],
      popular: true,
    },
    // Salads
    {
      id: "salad-1",
      name: "Mediterranean Salad",
      description: "Fresh mixed greens with feta cheese, olives, and olive oil",
      price: 11.99,
      image:
        "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400&h=300&fit=crop",
      category: "salad",
      rating: 4.5,
      prepTime: "5-8 min",
      ingredients: ["Mixed Greens", "Feta Cheese", "Olives", "Tomatoes"],
      popular: false,
    },
    {
      id: "salad-2",
      name: "Turkish Shepherd Salad",
      description:
        "Traditional chopped salad with tomatoes, cucumbers, and herbs",
      price: 9.99,
      image:
        "https://images.unsplash.com/photo-1540420773420-3366772f4999?w=400&h=300&fit=crop",
      category: "salad",
      rating: 4.4,
      prepTime: "5-8 min",
      ingredients: ["Tomatoes", "Cucumbers", "Onions", "Parsley", "Lemon"],
      popular: false,
    },
    // Desserts
    {
      id: "dessert-1",
      name: "Baklava",
      description: "Traditional Turkish pastry with nuts and honey syrup",
      price: 7.99,
      image:
        "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400&h=300&fit=crop",
      category: "dessert",
      rating: 4.9,
      prepTime: "2-5 min",
      ingredients: ["Phyllo Pastry", "Nuts", "Honey", "Butter"],
      popular: true,
    },
    {
      id: "dessert-2",
      name: "Turkish Delight",
      description: "Soft, chewy confection dusted with powdered sugar",
      price: 5.99,
      image:
        "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=400&h=300&fit=crop",
      category: "dessert",
      rating: 4.3,
      prepTime: "1-3 min",
      ingredients: ["Sugar", "Starch", "Flavorings", "Nuts"],
      popular: false,
    },
    // Drinks
    {
      id: "drink-1",
      name: "Turkish Tea",
      description: "Traditional black tea served in authentic Turkish glass",
      price: 3.99,
      image:
        "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop",
      category: "drink",
      rating: 4.6,
      prepTime: "3-5 min",
      ingredients: ["Black Tea", "Sugar (optional)"],
      popular: true,
    },
    {
      id: "drink-2",
      name: "Fresh Orange Juice",
      description: "Freshly squeezed orange juice, no additives",
      price: 4.99,
      image:
        "https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=400&h=300&fit=crop",
      category: "drink",
      rating: 4.4,
      prepTime: "2-4 min",
      ingredients: ["Fresh Oranges"],
      popular: false,
    },
  ];

  const categories = [
    { id: "all", name: "All Items", icon: Utensils },
    { id: "kebab", name: "Kebabs", icon: Utensils },
    { id: "doner", name: "Doner", icon: Utensils },
    { id: "salad", name: "Salads", icon: Salad },
    { id: "dessert", name: "Desserts", icon: Cookie },
    { id: "drink", name: "Drinks", icon: Coffee },
  ];

  const getFilteredProducts = () => {
    if (activeCategory === "all") return products;
    return products.filter((product) => product.category === activeCategory);
  };

  const addToCart = (product: Product) => {
    setCart((prevCart) => {
      const existingItem = prevCart.find((item) => item.id === product.id);
      if (existingItem) {
        return prevCart.map((item) =>
          item.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prevCart, { ...product, quantity: 1 }];
    });
  };

  const updateQuantity = (productId: string, newQuantity: number) => {
    if (newQuantity === 0) {
      removeFromCart(productId);
      return;
    }
    setCart((prevCart) =>
      prevCart.map((item) =>
        item.id === productId ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const removeFromCart = (productId: string) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== productId));
  };

  const getCartTotal = () => {
    return cart.reduce((total, item) => total + item.price * item.quantity, 0);
  };

  const getCartItemCount = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  const handleInputChange = (field: keyof OrderData, value: string) => {
    setOrderData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmitOrder = async () => {
    setIsLoading(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setIsLoading(false);
    setCurrentStep(3); // Success step
  };

  const isOrderValid = () => {
    return (
      cart.length > 0 &&
      orderData.customerName &&
      orderData.customerPhone &&
      orderData.customerEmail &&
      orderData.deliveryAddress
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {currentStep === 1 && (
        <div className="py-8">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                Order Online
              </h1>
              <p className="text-xl text-gray-600">
                Choose from our delicious menu
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
              {/* Menu Section */}
              <div className="lg:col-span-3">
                {/* Category Tabs */}
                <div className="mb-8">
                  <div className="flex flex-wrap gap-2">
                    {categories.map((category) => {
                      const IconComponent = category.icon;
                      return (
                        <Button
                          key={category.id}
                          variant={
                            activeCategory === category.id
                              ? "default"
                              : "outline"
                          }
                          onClick={() => setActiveCategory(category.id)}
                          className={`
                            ${
                              activeCategory === category.id
                                ? "bg-blue-600 hover:bg-blue-700 text-white"
                                : "border-gray-300 text-gray-700 hover:bg-gray-50"
                            }
                          `}
                        >
                          <IconComponent className="h-4 w-4 mr-2" />
                          {category.name}
                        </Button>
                      );
                    })}
                  </div>
                </div>

                {/* Products Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                  {getFilteredProducts().map((product) => (
                    <Card
                      key={product.id}
                      className="border-gray-200 shadow-sm hover:shadow-md transition-shadow"
                    >
                      <div className="relative">
                        <img
                          src={product.image}
                          alt={product.name}
                          className="w-full h-48 object-cover rounded-t-lg"
                        />
                        {product.popular && (
                          <Badge className="absolute top-2 left-2 bg-orange-500 text-white">
                            Popular
                          </Badge>
                        )}
                      </div>

                      <CardContent className="p-4">
                        <div className="flex justify-between items-start mb-2">
                          <h3 className="text-lg font-semibold text-gray-900">
                            {product.name}
                          </h3>
                          <span className="text-lg font-bold text-blue-600">
                            ${product.price}
                          </span>
                        </div>

                        <p className="text-gray-600 text-sm mb-3">
                          {product.description}
                        </p>

                        <div className="flex items-center justify-between mb-3">
                          <div className="flex items-center">
                            <Star className="h-4 w-4 text-yellow-400 fill-current" />
                            <span className="text-sm text-gray-600 ml-1">
                              {product.rating}
                            </span>
                          </div>
                          <div className="flex items-center text-gray-500">
                            <Clock className="h-4 w-4 mr-1" />
                            <span className="text-sm">{product.prepTime}</span>
                          </div>
                        </div>

                        <div className="flex flex-wrap gap-1 mb-4">
                          {product.ingredients
                            .slice(0, 3)
                            .map((ingredient, index) => (
                              <Badge
                                key={index}
                                variant="outline"
                                className="text-xs"
                              >
                                {ingredient}
                              </Badge>
                            ))}
                          {product.ingredients.length > 3 && (
                            <Badge variant="outline" className="text-xs">
                              +{product.ingredients.length - 3} more
                            </Badge>
                          )}
                        </div>

                        <Button
                          onClick={() => addToCart(product)}
                          className="w-full bg-blue-600 hover:bg-blue-700 text-white"
                        >
                          <Plus className="h-4 w-4 mr-2" />
                          Add to Cart
                        </Button>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </div>

              {/* Cart Sidebar */}
              <div className="lg:col-span-1">
                <Card className="border-gray-200 shadow-lg sticky top-8">
                  <CardHeader className="bg-blue-50 border-b border-blue-100">
                    <CardTitle className="text-xl text-gray-900 flex items-center">
                      <ShoppingCart className="h-5 w-5 mr-2" />
                      Your Order ({getCartItemCount()})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-4">
                    {cart.length === 0 ? (
                      <div className="text-center py-8">
                        <ShoppingCart className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                        <p className="text-gray-500">Your cart is empty</p>
                        <p className="text-sm text-gray-400">
                          Add items to get started
                        </p>
                      </div>
                    ) : (
                      <div className="space-y-4">
                        {cart.map((item) => (
                          <div
                            key={item.id}
                            className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
                          >
                            <img
                              src={item.image}
                              alt={item.name}
                              className="w-12 h-12 object-cover rounded"
                            />
                            <div className="flex-1 min-w-0">
                              <h4 className="text-sm font-medium text-gray-900 truncate">
                                {item.name}
                              </h4>
                              <p className="text-sm text-blue-600">
                                ${item.price}
                              </p>
                            </div>
                            <div className="flex items-center space-x-2">
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() =>
                                  updateQuantity(item.id, item.quantity - 1)
                                }
                                className="h-8 w-8 p-0"
                              >
                                <Minus className="h-3 w-3" />
                              </Button>
                              <span className="text-sm font-medium w-8 text-center">
                                {item.quantity}
                              </span>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() =>
                                  updateQuantity(item.id, item.quantity + 1)
                                }
                                className="h-8 w-8 p-0"
                              >
                                <Plus className="h-3 w-3" />
                              </Button>
                              <Button
                                size="sm"
                                variant="outline"
                                onClick={() => removeFromCart(item.id)}
                                className="h-8 w-8 p-0 text-red-600 hover:text-red-700"
                              >
                                <Trash2 className="h-3 w-3" />
                              </Button>
                            </div>
                          </div>
                        ))}

                        <Separator className="bg-gray-200" />

                        <div className="space-y-2">
                          <div className="flex justify-between text-sm">
                            <span>Subtotal:</span>
                            <span>${getCartTotal().toFixed(2)}</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span>Delivery Fee:</span>
                            <span>$3.99</span>
                          </div>
                          <div className="flex justify-between text-sm">
                            <span>Tax:</span>
                            <span>${(getCartTotal() * 0.08).toFixed(2)}</span>
                          </div>
                          <Separator className="bg-gray-200" />
                          <div className="flex justify-between font-semibold text-lg">
                            <span>Total:</span>
                            <span className="text-blue-600">
                              $
                              {(
                                getCartTotal() +
                                3.99 +
                                getCartTotal() * 0.08
                              ).toFixed(2)}
                            </span>
                          </div>
                        </div>

                        <Button
                          onClick={() => setCurrentStep(2)}
                          disabled={cart.length === 0}
                          className="w-full bg-blue-600 hover:bg-blue-700 text-white mt-4"
                        >
                          Proceed to Checkout
                        </Button>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      )}

      {currentStep === 2 && (
        <div className="py-8">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Checkout
              </h1>
              <p className="text-gray-600">Complete your order details</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2">
                <Card className="border-gray-200 shadow-lg">
                  <CardHeader className="bg-white border-b border-gray-100">
                    <CardTitle className="text-xl text-gray-900">
                      Delivery Information
                    </CardTitle>
                    <CardDescription className="text-gray-600">
                      Please provide your delivery details
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-6">
                    <div className="space-y-6">
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label
                            htmlFor="name"
                            className="text-gray-700 font-medium"
                          >
                            Full Name *
                          </Label>
                          <Input
                            id="name"
                            value={orderData.customerName}
                            onChange={(e) =>
                              handleInputChange("customerName", e.target.value)
                            }
                            className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                            placeholder="Enter your full name"
                          />
                        </div>

                        <div className="space-y-2">
                          <Label
                            htmlFor="phone"
                            className="text-gray-700 font-medium"
                          >
                            Phone Number *
                          </Label>
                          <Input
                            id="phone"
                            value={orderData.customerPhone}
                            onChange={(e) =>
                              handleInputChange("customerPhone", e.target.value)
                            }
                            className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                            placeholder="+1 (555) 123-4567"
                          />
                        </div>
                      </div>

                      <div className="space-y-2">
                        <Label
                          htmlFor="email"
                          className="text-gray-700 font-medium"
                        >
                          Email Address *
                        </Label>
                        <Input
                          id="email"
                          type="email"
                          value={orderData.customerEmail}
                          onChange={(e) =>
                            handleInputChange("customerEmail", e.target.value)
                          }
                          className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                          placeholder="your.email@example.com"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label
                          htmlFor="address"
                          className="text-gray-700 font-medium"
                        >
                          Delivery Address *
                        </Label>
                        <Textarea
                          id="address"
                          value={orderData.deliveryAddress}
                          onChange={(e) =>
                            handleInputChange("deliveryAddress", e.target.value)
                          }
                          className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 min-h-[80px]"
                          placeholder="Enter your complete delivery address"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label
                          htmlFor="instructions"
                          className="text-gray-700 font-medium"
                        >
                          Special Instructions (Optional)
                        </Label>
                        <Textarea
                          id="instructions"
                          value={orderData.specialInstructions}
                          onChange={(e) =>
                            handleInputChange(
                              "specialInstructions",
                              e.target.value
                            )
                          }
                          className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 min-h-[80px]"
                          placeholder="Any special delivery instructions or food preferences..."
                        />
                      </div>
                    </div>

                    <div className="flex justify-between mt-8">
                      <Button
                        onClick={() => setCurrentStep(1)}
                        variant="outline"
                        className="border-gray-300 text-gray-700 hover:bg-gray-50 px-8"
                      >
                        Back to Menu
                      </Button>
                      <Button
                        onClick={handleSubmitOrder}
                        disabled={!isOrderValid() || isLoading}
                        className="bg-blue-600 hover:bg-blue-700 text-white px-8"
                      >
                        {isLoading ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Processing...
                          </>
                        ) : (
                          "Place Order"
                        )}
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>

              {/* Order Summary */}
              <div>
                <Card className="border-gray-200 shadow-lg sticky top-8">
                  <CardHeader className="bg-blue-50 border-b border-blue-100">
                    <CardTitle className="text-xl text-gray-900">
                      Order Summary
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="p-4">
                    <div className="space-y-3">
                      {cart.map((item) => (
                        <div
                          key={item.id}
                          className="flex justify-between items-center"
                        >
                          <div className="flex-1">
                            <span className="text-sm font-medium">
                              {item.name}
                            </span>
                            <span className="text-xs text-gray-500 ml-2">
                              x{item.quantity}
                            </span>
                          </div>
                          <span className="text-sm font-medium">
                            ${(item.price * item.quantity).toFixed(2)}
                          </span>
                        </div>
                      ))}

                      <Separator className="bg-gray-200" />

                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span>Subtotal:</span>
                          <span>${getCartTotal().toFixed(2)}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Delivery Fee:</span>
                          <span>$3.99</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Tax:</span>
                          <span>${(getCartTotal() * 0.08).toFixed(2)}</span>
                        </div>
                        <Separator className="bg-gray-200" />
                        <div className="flex justify-between font-semibold text-lg">
                          <span>Total:</span>
                          <span className="text-blue-600">
                            $
                            {(
                              getCartTotal() +
                              3.99 +
                              getCartTotal() * 0.08
                            ).toFixed(2)}
                          </span>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>
        </div>
      )}

      {currentStep === 3 && (
        <div className="py-8">
          <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
            <Card className="border-green-200 shadow-lg">
              <CardContent className="p-12 text-center">
                <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-6" />
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Order Confirmed!
                </h2>
                <p className="text-xl text-gray-600 mb-6">
                  Thank you for your order
                </p>

                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">
                    Order Details
                  </h3>
                  <div className="space-y-2 text-left">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Order #:</span>
                      <span className="font-medium">
                        ORD-{Date.now().toString().slice(-6)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Total Amount:</span>
                      <span className="font-medium text-blue-600">
                        $
                        {(
                          getCartTotal() +
                          3.99 +
                          getCartTotal() * 0.08
                        ).toFixed(2)}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Estimated Delivery:</span>
                      <span className="font-medium">30-45 minutes</span>
                    </div>
                  </div>
                </div>

                <p className="text-gray-600 mb-6">
                  We've sent a confirmation email to {orderData.customerEmail}
                </p>

                <Button
                  onClick={() => {
                    setCurrentStep(1);
                    setCart([]);
                    setOrderData({
                      customerName: "",
                      customerPhone: "",
                      customerEmail: "",
                      deliveryAddress: "",
                      specialInstructions: "",
                      paymentMethod: "card",
                    });
                  }}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8"
                >
                  Order Again
                </Button>
              </CardContent>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

export default Order;
