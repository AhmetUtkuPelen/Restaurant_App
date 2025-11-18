import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/Components/ui/card";
import { Button } from "@/Components/ui/button";
import { Badge } from "@/Components/ui/badge";
import { Separator } from "@/Components/ui/separator";
import {
  ArrowLeft,
  ShoppingCart,
  CheckCircle,
  AlertCircle,
} from "lucide-react";
import { useCartStore } from "@/Zustand/Cart/CartState";
import { useOrderStore } from "@/Zustand/Order/OrderState";
import { useCreateOrder } from "@/hooks/useOrder";
import { axiosInstance } from "@/Axios/Axios";
import PaymentForm from "@/Components/Payment/PaymentForm";

const Checkout = () => {
  const navigate = useNavigate();
  const { items, getTotalPrice, clearCart } = useCartStore();
  const { createOrder } = useOrderStore();
  const createOrderMutation = useCreateOrder();

  const [step, setStep] = useState<"review" | "payment" | "success">("review");
  const [orderId, setOrderId] = useState<number | null>(null);

  const totalAmount = getTotalPrice();

  useEffect(() => {
    if (items.length === 0 && step === "review") {
      navigate("/cart");
    }
  }, [items, step, navigate]);

  const handleCreateOrder = async () => {
    try {
      const orderItems = items.map((item) => ({
        id: item.id,
        name: item.name,
        price:
          typeof item.price === "string" ? parseFloat(item.price) : item.price,
        quantity: item.quantity,
        image_url: item.image_url,
        category: item.category,
      }));

      createOrder(orderItems);

      // First, sync cart to backend
      // Clear backend cart first
      try {
        await axiosInstance.delete("/cart/clear");
      } catch {
        // Ignore if cart doesn't exist
      }

      // Add all items to backend cart
      for (const item of items) {
        await axiosInstance.post("/cart/items", {
          product_id: item.id,
          quantity: item.quantity,
        });
      }

      // Now create order from backend cart
      const result = await createOrderMutation.mutateAsync({});

      setOrderId(result.order.id);
      setStep("payment");
    } catch (error) {
      console.error("Failed to create order:", error);
      alert("Failed to create order. Please try again.");
    }
  };

  const handlePaymentSuccess = () => {
    setStep("success");
    clearCart();
  };

  const handlePaymentError = (error: string) => {
    alert(`Payment failed: ${error}`);
  };

  if (step === "success") {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="border-green-200 shadow-lg">
            <CardContent className="p-12 text-center">
              <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-6" />
              <h1 className="text-3xl font-bold text-gray-900 mb-4">
                Order Completed Successfully!
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Thank you for your purchase. Your order has been confirmed.
              </p>

              <div className="bg-gray-50 rounded-lg p-6 mb-8">
                <div className="text-left space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Order ID:</span>
                    <span className="font-medium">#{orderId}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Amount:</span>
                    <span className="font-medium">
                      ₺{totalAmount.toFixed(2)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Status:</span>
                    <Badge className="bg-green-100 text-green-800">
                      Completed
                    </Badge>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <Button
                  onClick={() => navigate("/user/orders")}
                  className="w-full bg-blue-600 hover:bg-blue-700"
                >
                  View My Orders
                </Button>
                <Button
                  onClick={() => navigate("/")}
                  variant="outline"
                  className="w-full"
                >
                  Continue Shopping
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <button
            onClick={() =>
              step === "payment" ? setStep("review") : navigate("/cart")
            }
            className="inline-flex items-center gap-2 text-gray-600 hover:text-blue-600 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            {step === "payment" ? "Back to Review" : "Back to Cart"}
          </button>

          <h1 className="text-3xl font-bold text-gray-900 flex items-center">
            <ShoppingCart className="h-8 w-8 mr-3 text-blue-600" />
            Checkout
          </h1>

          {/* Progress Steps */}
          <div className="flex items-center mt-6 space-x-8">
            <div className="flex items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step === "review"
                    ? "bg-blue-600 text-white"
                    : "bg-green-600 text-white"
                }`}
              >
                {step === "review" ? "1" : <CheckCircle className="w-5 h-5" />}
              </div>
              <span
                className={`ml-2 ${
                  step === "review"
                    ? "text-blue-600 font-medium"
                    : "text-green-600"
                }`}
              >
                Review Order
              </span>
            </div>

            <div
              className={`w-16 h-0.5 ${
                step === "payment" ? "bg-blue-600" : "bg-gray-300"
              }`}
            />

            <div className="flex items-center">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  step === "payment"
                    ? "bg-blue-600 text-white"
                    : "bg-gray-300 text-gray-600"
                }`}
              >
                2
              </div>
              <span
                className={`ml-2 ${
                  step === "payment"
                    ? "text-blue-600 font-medium"
                    : "text-gray-600"
                }`}
              >
                Payment
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {step === "review" && (
              <Card>
                <CardHeader>
                  <CardTitle>Review Your Order</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {items.map((item) => (
                      <div
                        key={item.id}
                        className="flex items-center space-x-4 p-4 border rounded-lg"
                      >
                        <img
                          src={item.image_url}
                          alt={item.name}
                          className="w-16 h-16 object-cover rounded"
                        />
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-900">
                            {item.name}
                          </h3>
                          <p className="text-sm text-gray-600 capitalize">
                            {item.category}
                          </p>
                          <div className="flex items-center justify-between mt-2">
                            <span className="text-sm text-gray-600">
                              Quantity: {item.quantity}
                            </span>
                            <span className="font-medium">
                              ₺
                              {(
                                (typeof item.price === "string"
                                  ? parseFloat(item.price)
                                  : item.price) * item.quantity
                              ).toFixed(2)}
                            </span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <Button
                    onClick={handleCreateOrder}
                    disabled={createOrderMutation.isPending}
                    className="w-full mt-6 bg-blue-600 hover:bg-blue-700"
                  >
                    {createOrderMutation.isPending ? (
                      <>
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Creating Order...
                      </>
                    ) : (
                      "Proceed to Payment"
                    )}
                  </Button>
                </CardContent>
              </Card>
            )}

            {step === "payment" && orderId && (
              <PaymentForm
                amount={totalAmount}
                orderId={orderId}
                paymentType="cart"
                onSuccess={handlePaymentSuccess}
                onError={handlePaymentError}
              />
            )}
          </div>

          {/* Order Summary */}
          <div>
            <Card className="sticky top-8">
              <CardHeader>
                <CardTitle>Order Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-600">
                      Items ({items.length}):
                    </span>
                    <span>₺{totalAmount.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Delivery:</span>
                    <span className="text-green-600">Free</span>
                  </div>
                  <Separator />
                  <div className="flex justify-between text-lg font-semibold">
                    <span>Total:</span>
                    <span className="text-blue-600">
                      ₺{totalAmount.toFixed(2)}
                    </span>
                  </div>
                </div>

                {step === "review" && (
                  <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-start space-x-2">
                      <AlertCircle className="w-5 h-5 text-blue-600 mt-0.5" />
                      <div className="text-sm text-blue-800">
                        <p className="font-medium">Secure Checkout</p>
                        <p>
                          Your payment information is protected with SSL
                          encryption.
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;
