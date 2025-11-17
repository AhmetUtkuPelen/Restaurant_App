

import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/Components/ui/card'
import { Button } from '@/Components/ui/button'
import { Badge } from '@/Components/ui/badge'
import { Separator } from '@/Components/ui/separator'
import { 
  Clock,
  Package,
  CheckCircle,
  XCircle,
  Truck,
  Receipt,
  Calendar,
  DollarSign,
  Eye,
  RotateCcw
} from 'lucide-react'

interface OrderItem {
  id: string
  name: string
  quantity: number
  price: number
}

interface Order {
  id: string
  orderNumber: string
  date: string
  status: 'pending' | 'confirmed' | 'preparing' | 'ready' | 'delivered' | 'cancelled'
  items: OrderItem[]
  total: number
  deliveryAddress: string
  paymentMethod: string
}

export const OrderHistory = () => {
  const [orders] = useState<Order[]>([
    {
      id: '1',
      orderNumber: 'ORD-2024-001',
      date: '2024-01-10T18:30:00Z',
      status: 'delivered',
      items: [
        { id: '1', name: 'Chicken Doner', quantity: 2, price: 12.99 },
        { id: '2', name: 'Turkish Tea', quantity: 1, price: 3.99 }
      ],
      total: 29.97,
      deliveryAddress: '123 Main St, Apt 4B',
      paymentMethod: 'Credit Card'
    },
    {
      id: '2',
      orderNumber: 'ORD-2024-002',
      date: '2024-01-08T14:15:00Z',
      status: 'delivered',
      items: [
        { id: '3', name: 'Lamb Kebab', quantity: 1, price: 16.99 },
        { id: '4', name: 'Baklava', quantity: 2, price: 8.50 },
        { id: '5', name: 'Turkish Coffee', quantity: 1, price: 4.99 }
      ],
      total: 38.98,
      deliveryAddress: '123 Main St, Apt 4B',
      paymentMethod: 'Debit Card'
    },
    {
      id: '3',
      orderNumber: 'ORD-2024-003',
      date: '2024-01-05T20:45:00Z',
      status: 'preparing',
      items: [
        { id: '6', name: 'Mixed Salad', quantity: 1, price: 9.99 },
        { id: '7', name: 'Ayran', quantity: 2, price: 2.99 }
      ],
      total: 15.97,
      deliveryAddress: '123 Main St, Apt 4B',
      paymentMethod: 'Cash'
    },
    {
      id: '4',
      orderNumber: 'ORD-2024-004',
      date: '2024-01-03T12:20:00Z',
      status: 'cancelled',
      items: [
        { id: '8', name: 'Beef Doner', quantity: 1, price: 13.99 }
      ],
      total: 13.99,
      deliveryAddress: '123 Main St, Apt 4B',
      paymentMethod: 'Credit Card'
    }
  ])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pending':
        return <Clock className="h-4 w-4" />
      case 'confirmed':
        return <CheckCircle className="h-4 w-4" />
      case 'preparing':
        return <Package className="h-4 w-4" />
      case 'ready':
        return <CheckCircle className="h-4 w-4" />
      case 'delivered':
        return <Truck className="h-4 w-4" />
      case 'cancelled':
        return <XCircle className="h-4 w-4" />
      default:
        return <Clock className="h-4 w-4" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending':
        return 'bg-yellow-900/20 text-yellow-300 border-yellow-800'
      case 'confirmed':
        return 'bg-blue-900/20 text-blue-300 border-blue-800'
      case 'preparing':
        return 'bg-orange-900/20 text-orange-300 border-orange-800'
      case 'ready':
        return 'bg-purple-900/20 text-purple-300 border-purple-800'
      case 'delivered':
        return 'bg-green-900/20 text-green-300 border-green-800'
      case 'cancelled':
        return 'bg-red-900/20 text-red-300 border-red-800'
      default:
        return 'bg-gray-900/20 text-gray-300 border-gray-800'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const totalSpent = orders
    .filter(order => order.status === 'delivered')
    .reduce((sum, order) => sum + order.total, 0)

  return (
    <div className="space-y-6">
      {/* Header Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-900/20 rounded-lg">
                <Receipt className="h-5 w-5 text-blue-400" />
              </div>
              <div>
                <p className="text-sm text-slate-400">Total Orders</p>
                <p className="text-2xl font-bold text-white">{orders.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-900/20 rounded-lg">
                <DollarSign className="h-5 w-5 text-green-400" />
              </div>
              <div>
                <p className="text-sm text-slate-400">Total Spent</p>
                <p className="text-2xl font-bold text-white">${totalSpent.toFixed(2)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-900/20 rounded-lg">
                <Calendar className="h-5 w-5 text-purple-400" />
              </div>
              <div>
                <p className="text-sm text-slate-400">This Month</p>
                <p className="text-2xl font-bold text-white">
                  {orders.filter(order => 
                    new Date(order.date).getMonth() === new Date().getMonth()
                  ).length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Orders List */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Order History</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {orders.length === 0 ? (
            <div className="p-8 text-center">
              <Receipt className="h-12 w-12 text-slate-600 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">No orders yet</h3>
              <p className="text-slate-400">Your order history will appear here once you place your first order.</p>
            </div>
          ) : (
            <div className="divide-y divide-slate-700">
              {orders.map((order) => (
                <div key={order.id} className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center space-x-3 mb-2">
                        <h3 className="text-lg font-semibold text-white">
                          {order.orderNumber}
                        </h3>
                        <Badge className={getStatusColor(order.status)}>
                          {getStatusIcon(order.status)}
                          <span className="ml-1 capitalize">{order.status}</span>
                        </Badge>
                      </div>
                      <p className="text-slate-400 text-sm flex items-center">
                        <Calendar className="h-4 w-4 mr-1" />
                        {formatDate(order.date)}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xl font-bold text-white">${order.total.toFixed(2)}</p>
                      <p className="text-slate-400 text-sm">{order.items.length} items</p>
                    </div>
                  </div>

                  {/* Order Items */}
                  <div className="space-y-2 mb-4">
                    {order.items.map((item) => (
                      <div key={item.id} className="flex justify-between text-sm">
                        <span className="text-slate-300">
                          {item.quantity}x {item.name}
                        </span>
                        <span className="text-slate-400">
                          ${(item.price * item.quantity).toFixed(2)}
                        </span>
                      </div>
                    ))}
                  </div>

                  <Separator className="bg-slate-700 mb-4" />

                  {/* Order Details */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm mb-4">
                    <div>
                      <p className="text-slate-400">Delivery Address:</p>
                      <p className="text-slate-300">{order.deliveryAddress}</p>
                    </div>
                    <div>
                      <p className="text-slate-400">Payment Method:</p>
                      <p className="text-slate-300">{order.paymentMethod}</p>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex space-x-3">
                    <Button 
                      variant="outline" 
                      size="sm"
                      className="border-slate-600 text-slate-300 hover:bg-slate-700"
                    >
                      <Eye className="h-4 w-4 mr-2" />
                      View Details
                    </Button>
                    {order.status === 'delivered' && (
                      <Button 
                        variant="outline" 
                        size="sm"
                        className="border-slate-600 text-slate-300 hover:bg-slate-700"
                      >
                        <RotateCcw className="h-4 w-4 mr-2" />
                        Reorder
                      </Button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
