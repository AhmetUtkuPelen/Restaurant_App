

import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '@/Components/ui/card'
import { Button } from '@/Components/ui/button'
import { Badge } from '@/Components/ui/badge'
import { Separator } from '@/Components/ui/separator'
import { Input } from '@/Components/ui/input'
import { 
  Minus, 
  Plus, 
  Trash2, 
  ShoppingCart,
  CreditCard,
  Tag,
  ArrowLeft
} from 'lucide-react'
import { useCartStore } from '@/Zustand/Cart/CartState'

export const Cart = () => {
  const navigate = useNavigate()
  const [promoCode, setPromoCode] = useState('')

  // Get cart data and functions from Zustand store
  const cartItems = useCartStore((state) => state.items)
  const updateQuantity = useCartStore((state) => state.updateQuantity)
  const removeFromCart = useCartStore((state) => state.removeFromCart)
  const clearCart = useCartStore((state) => state.clearCart)
  const getTotalPrice = useCartStore((state) => state.getTotalPrice)

  // Calculate totals
  const subtotal = getTotalPrice()
  const tax = subtotal * 0.08
  const delivery = subtotal > 30 ? 0 : 4.99 // Free delivery over $30
  const total = subtotal + tax + delivery

  // Helper function to capitalize category
  const formatCategory = (category: string) => {
    return category.charAt(0).toUpperCase() + category.slice(1)
  }

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            onClick={() => navigate(-1)}
            className="text-slate-300 hover:text-white mb-4"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back
          </Button>
          <h1 className="text-3xl font-bold text-white flex items-center">
            <ShoppingCart className="h-8 w-8 mr-3 text-blue-400" />
            Shopping Cart
          </h1>
          <p className="text-slate-400 mt-2">
            {cartItems.length} {cartItems.length === 1 ? 'item' : 'items'} in your cart
          </p>
        </div>

        {cartItems.length === 0 ? (
          <Card className="bg-slate-800 border-slate-700">
            <CardContent className="p-12 text-center">
              <ShoppingCart className="h-16 w-16 text-slate-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Your cart is empty</h3>
              <p className="text-slate-400 mb-6">Add some delicious items to get started!</p>
              <Link to="/">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Continue Shopping
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {cartItems.map((item) => {
                const itemPrice = parseFloat(item.final_price || item.price)
                const itemTotal = itemPrice * item.quantity

                return (
                  <Card key={item.id} className="bg-slate-800 border-slate-700">
                    <CardContent className="p-6">
                      <div className="flex items-center space-x-4">
                        <img
                          src={item.image_url || "https://via.placeholder.com/80x80/1f2937/ffffff?text=Product"}
                          alt={item.name}
                          className="w-20 h-20 object-cover rounded-lg"
                        />
                        <div className="flex-1">
                          <div className="flex items-start justify-between">
                            <div>
                              <h3 className="text-lg font-semibold text-white">{item.name}</h3>
                              <Badge variant="secondary" className="bg-slate-700 text-slate-300 mt-1">
                                {formatCategory(item.category)}
                              </Badge>
                            </div>
                            <Button
                              variant="ghost"
                              size="sm"
                              onClick={() => removeFromCart(item.id)}
                              className="text-red-400 hover:text-red-300 hover:bg-red-900/20"
                            >
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                          
                          <div className="flex items-center justify-between mt-4">
                            <div className="flex items-center space-x-3">
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                                className="h-8 w-8 p-0 border-slate-600 text-slate-300 hover:bg-slate-700"
                              >
                                <Minus className="h-4 w-4" />
                              </Button>
                              <span className="text-white font-medium w-8 text-center">
                                {item.quantity}
                              </span>
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => updateQuantity(item.id, item.quantity + 1)}
                                className="h-8 w-8 p-0 border-slate-600 text-slate-300 hover:bg-slate-700"
                              >
                                <Plus className="h-4 w-4" />
                              </Button>
                            </div>
                            <div className="text-right">
                              <p className="text-lg font-semibold text-white">
                                ${itemTotal.toFixed(2)}
                              </p>
                              <p className="text-sm text-slate-400">
                                ${itemPrice.toFixed(2)} each
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )
              })}

              {/* Clear Cart Button */}
              <Button
                variant="outline"
                onClick={clearCart}
                className="w-full border-red-600 text-red-400 hover:bg-red-900/20 hover:text-red-300"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Clear Cart
              </Button>
            </div>

            {/* Order Summary */}
            <div className="space-y-6">
              {/* Promo Code */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white flex items-center">
                    <Tag className="h-5 w-5 mr-2 text-blue-400" />
                    Promo Code
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  <Input
                    placeholder="Enter promo code"
                    value={promoCode}
                    onChange={(e) => setPromoCode(e.target.value)}
                    className="bg-slate-700 border-slate-600 text-white placeholder-slate-400"
                  />
                  <Button 
                    variant="outline" 
                    className="w-full border-slate-600 text-slate-300 hover:bg-slate-700"
                  >
                    Apply Code
                  </Button>
                </CardContent>
              </Card>

              {/* Order Summary */}
              <Card className="bg-slate-800 border-slate-700">
                <CardHeader>
                  <CardTitle className="text-white">Order Summary</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="space-y-3">
                    <div className="flex justify-between text-slate-300">
                      <span>Subtotal</span>
                      <span>${subtotal.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Tax (8%)</span>
                      <span>${tax.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Delivery</span>
                      <span className="flex items-center gap-2">
                        {delivery === 0 ? (
                          <>
                            <span className="line-through text-slate-500">$4.99</span>
                            <span className="text-green-400 font-medium">FREE</span>
                          </>
                        ) : (
                          `$${delivery.toFixed(2)}`
                        )}
                      </span>
                    </div>
                    {subtotal < 30 && subtotal > 0 && (
                      <p className="text-xs text-slate-400">
                        Add ${(30 - subtotal).toFixed(2)} more for free delivery!
                      </p>
                    )}
                    <Separator className="bg-slate-700" />
                    <div className="flex justify-between text-lg font-semibold text-white">
                      <span>Total</span>
                      <span>${total.toFixed(2)}</span>
                    </div>
                  </div>

                  <Link to="/checkout">
                    <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white mt-6">
                      <CreditCard className="h-4 w-4 mr-2" />
                      Proceed to Checkout
                    </Button>
                  </Link>

                  <Link to="/">
                    <Button 
                      variant="outline" 
                      className="w-full border-slate-600 text-slate-300 hover:bg-slate-700"
                    >
                      Continue Shopping
                    </Button>
                  </Link>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
