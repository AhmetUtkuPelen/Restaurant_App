

import { useState } from 'react'
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
  Tag
} from 'lucide-react'

interface CartItem {
  id: string
  name: string
  category: string
  price: number
  quantity: number
  image: string
  description: string
}

export const Cart = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([
    {
      id: '1',
      name: 'Chicken Doner',
      category: 'Doner',
      price: 12.99,
      quantity: 2,
      image: 'https://images.unsplash.com/photo-1529193591184-b1d58069ecdd?w=300&h=200&fit=crop',
      description: 'Traditional chicken doner with fresh vegetables'
    },
    {
      id: '2',
      name: 'Baklava',
      category: 'Dessert',
      price: 8.50,
      quantity: 1,
      image: 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=300&h=200&fit=crop',
      description: 'Sweet pastry with nuts and honey'
    },
    {
      id: '3',
      name: 'Turkish Tea',
      category: 'Drink',
      price: 3.99,
      quantity: 3,
      image: 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=200&fit=crop',
      description: 'Traditional Turkish black tea'
    }
  ])

  const [promoCode, setPromoCode] = useState('')

  const updateQuantity = (id: string, newQuantity: number) => {
    if (newQuantity === 0) {
      removeItem(id)
      return
    }
    setCartItems(items =>
      items.map(item =>
        item.id === id ? { ...item, quantity: newQuantity } : item
      )
    )
  }

  const removeItem = (id: string) => {
    setCartItems(items => items.filter(item => item.id !== id))
  }

  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  const tax = subtotal * 0.08
  const delivery = 4.99
  const total = subtotal + tax + delivery

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
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
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                Continue Shopping
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2 space-y-4">
              {cartItems.map((item) => (
                <Card key={item.id} className="bg-slate-800 border-slate-700">
                  <CardContent className="p-6">
                    <div className="flex items-center space-x-4">
                      <img
                        src={item.image}
                        alt={item.name}
                        className="w-20 h-20 object-cover rounded-lg"
                      />
                      <div className="flex-1">
                        <div className="flex items-start justify-between">
                          <div>
                            <h3 className="text-lg font-semibold text-white">{item.name}</h3>
                            <Badge variant="secondary" className="bg-slate-700 text-slate-300 mt-1">
                              {item.category}
                            </Badge>
                            <p className="text-slate-400 text-sm mt-2">{item.description}</p>
                          </div>
                          <Button
                            variant="ghost"
                            size="sm"
                            onClick={() => removeItem(item.id)}
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
                              ${(item.price * item.quantity).toFixed(2)}
                            </p>
                            <p className="text-sm text-slate-400">
                              ${item.price.toFixed(2)} each
                            </p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              ))}
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
                      <span>Tax</span>
                      <span>${tax.toFixed(2)}</span>
                    </div>
                    <div className="flex justify-between text-slate-300">
                      <span>Delivery</span>
                      <span>${delivery.toFixed(2)}</span>
                    </div>
                    <Separator className="bg-slate-700" />
                    <div className="flex justify-between text-lg font-semibold text-white">
                      <span>Total</span>
                      <span>${total.toFixed(2)}</span>
                    </div>
                  </div>

                  <Button className="w-full bg-blue-600 hover:bg-blue-700 text-white mt-6">
                    <CreditCard className="h-4 w-4 mr-2" />
                    Proceed to Checkout
                  </Button>

                  <Button 
                    variant="outline" 
                    className="w-full border-slate-600 text-slate-300 hover:bg-slate-700"
                  >
                    Continue Shopping
                  </Button>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}