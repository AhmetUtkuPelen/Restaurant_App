

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/Components/ui/card'
import { Button } from '@/Components/ui/button'
import { Badge } from '@/Components/ui/badge'
import { Input } from '@/Components/ui/input'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/Components/ui/select'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/Components/ui/table'
import { Progress } from '@/Components/ui/progress'
import { 
  Package, 
  Search, 
  AlertTriangle, 
  TrendingUp, 
  TrendingDown,
  RefreshCw,
  Download,
  Eye,
  Plus
} from 'lucide-react'
import { Avatar, AvatarFallback, AvatarImage } from '@/Components/ui/avatar'

// Mock stock data
const mockStockData = [
  {
    id: 1,
    name: 'Chicken Breast',
    category: 'Ingredients',
    currentStock: 25,
    minStock: 20,
    maxStock: 100,
    unit: 'kg',
    supplier: 'Fresh Meat Co.',
    supplierContact: '+1 234-567-8900',
    lastRestocked: '2024-10-10',
    expiryDate: '2024-10-20',
    cost: 8.50,
    image: 'https://images.unsplash.com/photo-1604503468506-a8da13d82791?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 2,
    name: 'Tomatoes',
    category: 'Ingredients',
    currentStock: 15,
    minStock: 10,
    maxStock: 50,
    unit: 'kg',
    supplier: 'Green Gardens',
    supplierContact: '+1 234-567-8901',
    lastRestocked: '2024-10-12',
    expiryDate: '2024-10-18',
    cost: 3.20,
    image: 'https://images.unsplash.com/photo-1546470427-e26264be0b0d?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 3,
    name: 'Coca Cola',
    category: 'Drinks',
    currentStock: 48,
    minStock: 30,
    maxStock: 120,
    unit: 'bottles',
    supplier: 'Beverage Plus',
    supplierContact: '+1 234-567-8902',
    lastRestocked: '2024-10-11',
    expiryDate: '2025-03-15',
    cost: 1.50,
    image: 'https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 4,
    name: 'Orange Juice',
    category: 'Drinks',
    currentStock: 8,
    minStock: 15,
    maxStock: 60,
    unit: 'bottles',
    supplier: 'Fresh Juice Co.',
    supplierContact: '+1 234-567-8903',
    lastRestocked: '2024-10-08',
    expiryDate: '2024-10-25',
    cost: 2.80,
    image: 'https://images.unsplash.com/photo-1621506289937-a8e4df240d0b?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 5,
    name: 'Chocolate Cake',
    category: 'Desserts',
    currentStock: 6,
    minStock: 8,
    maxStock: 20,
    unit: 'pieces',
    supplier: 'Sweet Delights',
    supplierContact: '+1 234-567-8904',
    lastRestocked: '2024-10-13',
    expiryDate: '2024-10-16',
    cost: 12.00,
    image: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 6,
    name: 'Baklava',
    category: 'Desserts',
    currentStock: 12,
    minStock: 10,
    maxStock: 30,
    unit: 'pieces',
    supplier: 'Turkish Sweets',
    supplierContact: '+1 234-567-8905',
    lastRestocked: '2024-10-12',
    expiryDate: '2024-10-19',
    cost: 4.50,
    image: 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 7,
    name: 'Lettuce',
    category: 'Ingredients',
    currentStock: 5,
    minStock: 12,
    maxStock: 40,
    unit: 'heads',
    supplier: 'Green Gardens',
    supplierContact: '+1 234-567-8901',
    lastRestocked: '2024-10-09',
    expiryDate: '2024-10-17',
    cost: 1.80,
    image: 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?w=100&h=100&fit=crop&crop=center'
  },
  {
    id: 8,
    name: 'Sparkling Water',
    category: 'Drinks',
    currentStock: 35,
    minStock: 25,
    maxStock: 80,
    unit: 'bottles',
    supplier: 'Pure Water Co.',
    supplierContact: '+1 234-567-8906',
    lastRestocked: '2024-10-11',
    expiryDate: '2025-06-30',
    cost: 1.20,
    image: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=100&h=100&fit=crop&crop=center'
  }
]

const AdminStock = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [categoryFilter, setCategoryFilter] = useState('all')
  const [stockFilter, setStockFilter] = useState('all')

  const getStockStatus = (current: number, min: number) => {
    const percentage = (current / min) * 100
    if (percentage <= 50) return { status: 'critical', color: 'bg-red-500', textColor: 'text-red-600' }
    if (percentage <= 100) return { status: 'low', color: 'bg-yellow-500', textColor: 'text-yellow-600' }
    return { status: 'good', color: 'bg-green-500', textColor: 'text-green-600' }
  }

  const getStockPercentage = (current: number, max: number) => {
    return Math.min((current / max) * 100, 100)
  }

  const filteredStock = mockStockData.filter(item => {
    const matchesSearch = item.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.supplier.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesCategory = categoryFilter === 'all' || item.category === categoryFilter
    
    let matchesStockFilter = true
    if (stockFilter === 'low') {
      matchesStockFilter = item.currentStock <= item.minStock
    } else if (stockFilter === 'critical') {
      matchesStockFilter = item.currentStock <= item.minStock * 0.5
    }
    
    return matchesSearch && matchesCategory && matchesStockFilter
  })

  const lowStockItems = mockStockData.filter(item => item.currentStock <= item.minStock).length
  const criticalStockItems = mockStockData.filter(item => item.currentStock <= item.minStock * 0.5).length
  const totalValue = mockStockData.reduce((sum, item) => sum + (item.currentStock * item.cost), 0)

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Stock Management</h1>
          <p className="text-gray-600 dark:text-gray-400">Monitor and manage your inventory levels</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Items</CardTitle>
              <Package className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{mockStockData.length}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400">Active inventory items</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Low Stock</CardTitle>
              <TrendingDown className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-yellow-600">{lowStockItems}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400">Items need restocking</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-red-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Critical Stock</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-red-600">{criticalStockItems}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400">Urgent attention needed</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Value</CardTitle>
              <TrendingUp className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">${totalValue.toFixed(2)}</div>
              <p className="text-xs text-gray-600 dark:text-gray-400">Current inventory value</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters and Actions */}
        <Card className="mb-6">
          <CardHeader>
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
              <div>
                <CardTitle>Inventory Overview</CardTitle>
                <CardDescription>Track stock levels and supplier information</CardDescription>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <div className="relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
                  <Input
                    placeholder="Search items or suppliers..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-10 w-64"
                  />
                </div>
                <Select value={categoryFilter} onValueChange={setCategoryFilter}>
                  <SelectTrigger className="w-40">
                    <SelectValue placeholder="Category" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Categories</SelectItem>
                    <SelectItem value="Ingredients">Ingredients</SelectItem>
                    <SelectItem value="Drinks">Drinks</SelectItem>
                    <SelectItem value="Desserts">Desserts</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={stockFilter} onValueChange={setStockFilter}>
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Stock Level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Stock</SelectItem>
                    <SelectItem value="low">Low Stock</SelectItem>
                    <SelectItem value="critical">Critical</SelectItem>
                  </SelectContent>
                </Select>
                <Button variant="outline" size="icon">
                  <RefreshCw className="h-4 w-4" />
                </Button>
                <Button variant="outline" size="icon">
                  <Download className="h-4 w-4" />
                </Button>
                <Button className="bg-blue-600 hover:bg-blue-700">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Item
                </Button>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Item</TableHead>
                    <TableHead>Category</TableHead>
                    <TableHead>Stock Level</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Supplier</TableHead>
                    <TableHead>Last Restocked</TableHead>
                    <TableHead>Expiry</TableHead>
                    <TableHead>Value</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredStock.map((item) => {
                    const stockStatus = getStockStatus(item.currentStock, item.minStock)
                    const stockPercentage = getStockPercentage(item.currentStock, item.maxStock)
                    const isExpiringSoon = new Date(item.expiryDate) <= new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
                    
                    return (
                      <TableRow key={item.id}>
                        <TableCell>
                          <div className="flex items-center space-x-3">
                            <Avatar className="h-10 w-10">
                              <AvatarImage src={item.image} alt={item.name} />
                              <AvatarFallback>{item.name.charAt(0)}</AvatarFallback>
                            </Avatar>
                            <div>
                              <div className="font-medium">{item.name}</div>
                              <div className="text-sm text-gray-500">{item.unit}</div>
                            </div>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">{item.category}</Badge>
                        </TableCell>
                        <TableCell>
                          <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                              <span>{item.currentStock}/{item.maxStock}</span>
                              <span className={stockStatus.textColor}>
                                {Math.round((item.currentStock / item.maxStock) * 100)}%
                              </span>
                            </div>
                            <Progress value={stockPercentage} className="h-2" />
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            <div className={`w-2 h-2 rounded-full ${stockStatus.color}`}></div>
                            <span className={`text-sm font-medium ${stockStatus.textColor}`}>
                              {stockStatus.status.charAt(0).toUpperCase() + stockStatus.status.slice(1)}
                            </span>
                            {stockStatus.status === 'critical' && (
                              <AlertTriangle className="h-4 w-4 text-red-500" />
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div>
                            <div className="font-medium text-sm">{item.supplier}</div>
                            <div className="text-xs text-gray-500">{item.supplierContact}</div>
                          </div>
                        </TableCell>
                        <TableCell className="text-sm">{item.lastRestocked}</TableCell>
                        <TableCell>
                          <div className={`text-sm ${isExpiringSoon ? 'text-red-600 font-medium' : 'text-gray-600'}`}>
                            {item.expiryDate}
                            {isExpiringSoon && (
                              <div className="text-xs text-red-500">Expires soon!</div>
                            )}
                          </div>
                        </TableCell>
                        <TableCell className="font-medium">
                          ${(item.currentStock * item.cost).toFixed(2)}
                        </TableCell>
                        <TableCell>
                          <div className="flex items-center space-x-2">
                            <Button variant="ghost" size="icon">
                              <Eye className="h-4 w-4" />
                            </Button>
                            <Button 
                              variant="outline" 
                              size="sm"
                              className={stockStatus.status === 'critical' ? 'border-red-500 text-red-600 hover:bg-red-50' : ''}
                            >
                              Restock
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    )
                  })}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card className="border-l-4 border-l-red-500">
            <CardHeader>
              <CardTitle className="text-red-600 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Critical Items
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {mockStockData
                  .filter(item => item.currentStock <= item.minStock * 0.5)
                  .slice(0, 3)
                  .map(item => (
                    <div key={item.id} className="flex justify-between items-center p-2 bg-red-50 dark:bg-red-900/20 rounded">
                      <span className="text-sm font-medium">{item.name}</span>
                      <Badge variant="destructive">{item.currentStock}</Badge>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader>
              <CardTitle className="text-yellow-600 flex items-center gap-2">
                <TrendingDown className="h-5 w-5" />
                Low Stock
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {mockStockData
                  .filter(item => item.currentStock <= item.minStock && item.currentStock > item.minStock * 0.5)
                  .slice(0, 3)
                  .map(item => (
                    <div key={item.id} className="flex justify-between items-center p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded">
                      <span className="text-sm font-medium">{item.name}</span>
                      <Badge variant="secondary">{item.currentStock}</Badge>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader>
              <CardTitle className="text-orange-600 flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Expiring Soon
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {mockStockData
                  .filter(item => new Date(item.expiryDate) <= new Date(Date.now() + 7 * 24 * 60 * 60 * 1000))
                  .slice(0, 3)
                  .map(item => (
                    <div key={item.id} className="flex justify-between items-center p-2 bg-orange-50 dark:bg-orange-900/20 rounded">
                      <span className="text-sm font-medium">{item.name}</span>
                      <span className="text-xs text-orange-600">{item.expiryDate}</span>
                    </div>
                  ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default AdminStock