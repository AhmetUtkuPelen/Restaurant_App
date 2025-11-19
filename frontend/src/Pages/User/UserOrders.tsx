import { Link } from "react-router-dom";
import { Card, CardContent } from "@/Components/ui/card";
import { Button } from "@/Components/ui/button";
import { Badge } from "@/Components/ui/badge";
import {
  ShoppingBag,
  AlertCircle,
  CheckCircle,
  Clock,
  XCircle,
  ArrowLeft,
  Package,
  Loader2,
} from "lucide-react";
import { useMyOrders, useCancelOrder } from "@/hooks/useOrder";
import { toast } from "sonner";
import { useState } from "react";

const UserOrders = () => {
  const { data: ordersData, isLoading, error } = useMyOrders();
  const cancelOrderMutation = useCancelOrder();
  const [cancellingOrderId, setCancellingOrderId] = useState<number | null>(null);

  const handleCancelOrder = async (orderId: number) => {
    toast.warning("Are you sure you want to cancel this order?", {
      description: "This action cannot be undone.",
      action: {
        label: "Yes, Cancel Order",
        onClick: async () => {
          setCancellingOrderId(orderId);
          try {
            await cancelOrderMutation.mutateAsync(orderId);
            toast.success("Order cancelled successfully", {
              description: `Order #${orderId} has been cancelled.`,
            });
          } catch (err) {
            const error = err as { response?: { data?: { detail?: string } } };
            toast.error(error?.response?.data?.detail || "Failed to cancel order");
          } finally {
            setCancellingOrderId(null);
          }
        },
      },
      cancel: {
        label: "Keep Order",
        onClick: () => {
          toast.info("Order cancellation cancelled");
        },
      },
    });
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return "bg-green-100 text-green-800";
      case "pending":
        return "bg-yellow-100 text-yellow-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return <CheckCircle className="h-4 w-4" />;
      case "pending":
        return <Clock className="h-4 w-4" />;
      case "cancelled":
        return <XCircle className="h-4 w-4" />;
      default:
        return <Package className="h-4 w-4" />;
    }
  };

  const formatDate = (dateString: string) => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    } catch {
      return "Invalid date";
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <Card className="bg-gray-800 border-gray-700 max-w-md">
          <CardContent className="p-8 text-center">
            <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">
              Error Loading Orders
            </h3>
            <p className="text-gray-400 mb-4">
              {error instanceof Error ? error.message : "Failed to load orders"}
            </p>
            <Button
              onClick={() => window.location.reload()}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const orders = ordersData?.orders || [];

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Home
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white flex items-center">
                <ShoppingBag className="h-8 w-8 mr-3 text-blue-400" />
                My Orders
              </h1>
              <p className="text-gray-400 mt-2">
                View and track your order history
              </p>
            </div>
          </div>
        </div>

        {/* Empty State */}
        {orders.length === 0 ? (
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <ShoppingBag className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">
                No Orders Yet
              </h3>
              <p className="text-gray-400 mb-6">
                You haven't placed any orders. Start shopping to see your orders
                here!
              </p>
              <Link to="/">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Start Shopping
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {orders.map((order) => (
              <Card
                key={order.id}
                className="bg-gray-800 border-gray-700 hover:border-gray-600 transition-colors"
              >
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-3 mb-2">
                        <h3 className="text-lg font-semibold text-white">
                          Order #{order.id}
                        </h3>
                        <Badge
                          className={`${getStatusColor(
                            order.status
                          )} flex items-center gap-1`}
                        >
                          {getStatusIcon(order.status)}
                          {order.status}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-400">
                        Placed on {formatDate(order.created_at)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-400">Total Amount</p>
                      <p className="text-2xl font-bold text-blue-400">
                        ₺{Number(order.total_amount).toFixed(2)}
                      </p>
                    </div>
                  </div>

                  {order.delivery_address && (
                    <div className="bg-gray-700/50 rounded-lg p-3 mb-4">
                      <p className="text-xs text-gray-400 mb-1">
                        Delivery Address:
                      </p>
                      <p className="text-sm text-gray-300">
                        {order.delivery_address}
                      </p>
                    </div>
                  )}

                  {order.special_instructions && (
                    <div className="bg-gray-700/50 rounded-lg p-3 mb-4">
                      <p className="text-xs text-gray-400 mb-1">
                        Special Instructions:
                      </p>
                      <p className="text-sm text-gray-300">
                        {order.special_instructions}
                      </p>
                    </div>
                  )}

                  <div className="flex items-center justify-between pt-4 border-t border-gray-700">
                    <span className="text-xs text-gray-500">
                      {order.items_count || 0} item(s)
                    </span>
                    <div className="flex items-center gap-3">
                      {order.completed_at && (
                        <span className="text-xs text-gray-500">
                          Completed: {formatDate(order.completed_at)}
                        </span>
                      )}
                      {order.status.toLowerCase() === "pending" && (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleCancelOrder(order.id)}
                          disabled={cancellingOrderId === order.id}
                          className="border-red-600 text-red-400 hover:bg-red-900/20 hover:text-red-300 cursor-pointer"
                        >
                          {cancellingOrderId === order.id ? (
                            <>
                              <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                              Cancelling...
                            </>
                          ) : (
                            <>
                              <XCircle className="h-4 w-4 mr-2" />
                              Cancel Order
                            </>
                          )}
                        </Button>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Summary Stats */}
        {orders.length > 0 && (
          <Card className="bg-gray-800 border-gray-700 mt-8">
            <CardContent className="p-6">
              <h3 className="text-lg font-semibold text-white mb-4">
                Order Summary
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-gray-700/50 rounded-lg p-4">
                  <p className="text-sm text-gray-400 mb-1">Total Orders</p>
                  <p className="text-2xl font-bold text-white">
                    {ordersData?.total || 0}
                  </p>
                </div>
                <div className="bg-gray-700/50 rounded-lg p-4">
                  <p className="text-sm text-gray-400 mb-1">Completed</p>
                  <p className="text-2xl font-bold text-green-400">
                    {orders.filter((o) => o.status === "completed").length}
                  </p>
                </div>
                <div className="bg-gray-700/50 rounded-lg p-4">
                  <p className="text-sm text-gray-400 mb-1">Pending</p>
                  <p className="text-2xl font-bold text-yellow-400">
                    {orders.filter((o) => o.status === "pending").length}
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default UserOrders;
