
import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/Components/ui/card'
import { Button } from '@/Components/ui/button'
import { Avatar, AvatarFallback, AvatarImage } from '@/Components/ui/avatar'
import { Badge } from '@/Components/ui/badge'
import { Separator } from '@/Components/ui/separator'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/Components/ui/dialog'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/Components/ui/tabs'
import { 
  User, 
  Mail, 
  Phone, 
  MapPin, 
  Calendar, 
  Settings, 
  Edit3,
  Shield,
  Clock,
  History
} from 'lucide-react'
import UserSettings from './UserSettings'
import { OrderHistory } from './OrderHistory'

interface UserProfile {
  id: string
  username: string
  email: string
  phone: string
  address: string
  profilePicture: string
  joinDate: string
  lastLogin: string
  accountStatus: 'active' | 'inactive' | 'suspended'
  totalOrders: number
  totalSpent: number
}

const Profile = () => {
  const [userProfile] = useState<UserProfile>({
    id: '12345',
    username: 'john_doe',
    email: 'john.doe@example.com',
    phone: '+1 (555) 123-4567',
    address: '123 Main Street, City, State 12345',
    profilePicture: '',
    joinDate: '2023-01-15',
    lastLogin: '2024-01-10T14:30:00Z',
    accountStatus: 'active',
    totalOrders: 24,
    totalSpent: 1250.75
  })

  const [isSettingsOpen, setIsSettingsOpen] = useState(false)

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }

  const formatLastLogin = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 border-green-200'
      case 'inactive':
        return 'bg-gray-100 text-gray-800 border-gray-200'
      case 'suspended':
        return 'bg-red-100 text-red-800 border-red-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
            <p className="text-gray-600 mt-2">View and manage your account information</p>
          </div>
          
          <Dialog open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
            <DialogTrigger asChild>
              <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                <Settings className="h-4 w-4 mr-2" />
                Account Settings
              </Button>
            </DialogTrigger>
            <DialogContent className="max-w-5xl max-h-[90vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle>Account Settings</DialogTitle>
              </DialogHeader>
              <UserSettings />
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            <Tabs defaultValue="profile" className="space-y-6">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="profile" className="flex items-center">
                  <User className="h-4 w-4 mr-2" />
                  Profile
                </TabsTrigger>
                <TabsTrigger value="orders" className="flex items-center">
                  <History className="h-4 w-4 mr-2" />
                  Order History
                </TabsTrigger>
              </TabsList>

              <TabsContent value="profile">
                <Card className="border-gray-200 shadow-sm">
                  <CardHeader className="bg-white border-b border-gray-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="text-xl text-gray-900">Profile Information</CardTitle>
                        <CardDescription className="text-gray-600">
                          Your personal account details
                        </CardDescription>
                      </div>
                      <Button 
                        variant="outline" 
                        size="sm"
                        onClick={() => setIsSettingsOpen(true)}
                        className="border-gray-300 text-gray-700 hover:bg-gray-50"
                      >
                        <Edit3 className="h-4 w-4 mr-2" />
                        Edit
                      </Button>
                    </div>
                  </CardHeader>
                  <CardContent className="p-6 bg-white">
                    <div className="space-y-6">
                      {/* Profile Picture and Basic Info */}
                      <div className="flex items-center space-x-6">
                        <Avatar className="h-20 w-20 border-4 border-gray-200">
                          <AvatarImage 
                            src={userProfile.profilePicture} 
                            alt="Profile picture" 
                          />
                          <AvatarFallback className="bg-blue-100 text-blue-600 text-2xl font-semibold">
                            {userProfile.username.charAt(0).toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <h2 className="text-2xl font-semibold text-gray-900">
                            {userProfile.username}
                          </h2>
                          <p className="text-gray-600">User ID: {userProfile.id}</p>
                          <Badge 
                            className={`mt-2 ${getStatusColor(userProfile.accountStatus)}`}
                          >
                            <Shield className="h-3 w-3 mr-1" />
                            {userProfile.accountStatus.charAt(0).toUpperCase() + userProfile.accountStatus.slice(1)}
                          </Badge>
                        </div>
                      </div>

                      <Separator className="bg-gray-200" />

                      {/* Contact Information */}
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="space-y-4">
                          <div className="flex items-center space-x-3">
                            <div className="flex-shrink-0">
                              <Mail className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">Email Address</p>
                              <p className="text-gray-900">{userProfile.email}</p>
                            </div>
                          </div>

                          <div className="flex items-center space-x-3">
                            <div className="flex-shrink-0">
                              <Phone className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">Phone Number</p>
                              <p className="text-gray-900">{userProfile.phone}</p>
                            </div>
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div className="flex items-start space-x-3">
                            <div className="flex-shrink-0 mt-1">
                              <MapPin className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">Address</p>
                              <p className="text-gray-900">{userProfile.address}</p>
                            </div>
                          </div>

                          <div className="flex items-center space-x-3">
                            <div className="flex-shrink-0">
                              <Calendar className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">Member Since</p>
                              <p className="text-gray-900">{formatDate(userProfile.joinDate)}</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="orders">
                <OrderHistory />
              </TabsContent>
            </Tabs>
          </div>

          {/* Account Statistics */}
          <div className="space-y-6">
            {/* Account Status Card */}
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-lg text-gray-900">Account Status</CardTitle>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">Status</span>
                    <Badge className={getStatusColor(userProfile.accountStatus)}>
                      {userProfile.accountStatus.charAt(0).toUpperCase() + userProfile.accountStatus.slice(1)}
                    </Badge>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    <Clock className="h-4 w-4 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-700">Last Login</p>
                      <p className="text-sm text-gray-600">{formatLastLogin(userProfile.lastLogin)}</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Order Statistics Card */}
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-lg text-gray-900">Order Statistics</CardTitle>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">{userProfile.totalOrders}</div>
                    <p className="text-sm text-gray-600">Total Orders</p>
                  </div>
                  
                  <Separator className="bg-gray-200" />
                  
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">
                      ${userProfile.totalSpent.toFixed(2)}
                    </div>
                    <p className="text-sm text-gray-600">Total Spent</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Actions Card */}
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-lg text-gray-900">Quick Actions</CardTitle>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-3">
                  <Button 
                    variant="outline" 
                    className="w-full justify-start border-gray-300 text-gray-700 hover:bg-gray-50"
                    onClick={() => setIsSettingsOpen(true)}
                  >
                    <Settings className="h-4 w-4 mr-2" />
                    Account Settings
                  </Button>
                  
                  <Button 
                    variant="outline" 
                    className="w-full justify-start border-gray-300 text-gray-700 hover:bg-gray-50"
                  >
                    <User className="h-4 w-4 mr-2" />
                    View Order History
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Profile
