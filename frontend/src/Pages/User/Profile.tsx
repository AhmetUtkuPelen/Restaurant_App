import { useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/Components/ui/card";
import { Button } from "@/Components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/Components/ui/avatar";
import { Badge } from "@/Components/ui/badge";
import { Separator } from "@/Components/ui/separator";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/Components/ui/dialog";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/Components/ui/tabs";
import {
  User,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Settings,
  Edit3,
  Shield,
  AlertCircle,
  History as HistoryIcon,
} from "lucide-react";
import UserSettings from "./UserSettings";
import UserOrders from "../../Pages/User/UserOrders";
import { useUserProfile } from "@/hooks/useUser";

const Profile = () => {
  const { data: userProfile, isLoading, error } = useUserProfile();
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  const getStatusColor = (isActive: boolean) => {
    return isActive
      ? "bg-green-100 text-green-800 border-green-200"
      : "bg-red-100 text-red-800 border-red-200";
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !userProfile) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-8 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Error Loading Profile
            </h3>
            <p className="text-gray-600 mb-4">
              {error instanceof Error
                ? error.message
                : "Failed to load profile"}
            </p>
            <Button onClick={() => window.location.reload()}>Try Again</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>
            <p className="text-gray-600 mt-2">
              View and manage your account information
            </p>
          </div>

          <Dialog open={isSettingsOpen} onOpenChange={setIsSettingsOpen}>
            <DialogTrigger asChild>
              <Button variant="outline" className="bg-blue-600 hover:bg-white text-white hover:text-blue-500 cursor-pointer border-blue-500">
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
              <TabsList className="grid w-full grid-cols-2 text-blue-600">
                <TabsTrigger value="profile" className="flex items-center">
                  <User className="h-4 w-4 mr-2" />
                  Profile
                </TabsTrigger>
                <TabsTrigger value="orders" className="flex items-center">
                  <HistoryIcon className="h-4 w-4 mr-2" />
                  Order History
                </TabsTrigger>
              </TabsList>

              <TabsContent value="profile">
                <Card className="border-gray-200 shadow-sm">
                  <CardHeader className="bg-white border-b border-gray-100">
                    <div className="flex items-center justify-between">
                      <div>
                        <CardTitle className="text-xl text-gray-900">
                          Profile Information
                        </CardTitle>
                        <CardDescription className="text-gray-600">
                          Your personal account details
                        </CardDescription>
                      </div>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setIsSettingsOpen(true)}
                        className="border-gray-300 text-white hover:text-blue-500 hover:bg-gray-50 cursor-pointer bg-blue-600"
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
                            src={userProfile.image_url || ""}
                            alt="Profile picture"
                          />
                          <AvatarFallback className="bg-blue-100 text-blue-600 text-2xl font-semibold">
                            {userProfile.username.charAt(0).toUpperCase()}
                          </AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                          <h2 className="text-2xl font-semibold text-blue-700 uppercase">
                            {userProfile.username}
                          </h2>
                          <p className="text-gray-600">
                            User ID: {userProfile.id}
                          </p>
                          <Badge
                            className={`mt-2 ${getStatusColor(
                              userProfile.is_active
                            )}`}
                          >
                            <Shield className="h-3 w-3 mr-1" />
                            {userProfile.is_active ? "Active" : "Inactive"}
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
                              <p className="text-sm font-medium text-gray-700">
                                Email Address
                              </p>
                              <p className="text-gray-900">
                                {userProfile.email}
                              </p>
                            </div>
                          </div>

                          <div className="flex items-center space-x-3">
                            <div className="flex-shrink-0">
                              <Phone className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">
                                Phone Number
                              </p>
                              <p className="text-gray-900">
                                {userProfile.phone}
                              </p>
                            </div>
                          </div>
                        </div>

                        <div className="space-y-4">
                          <div className="flex items-start space-x-3">
                            <div className="flex-shrink-0 mt-1">
                              <MapPin className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">
                                Address
                              </p>
                              <p className="text-gray-900">
                                {userProfile.address || "Not provided"}
                              </p>
                            </div>
                          </div>

                          <div className="flex items-center space-x-3">
                            <div className="flex-shrink-0">
                              <Calendar className="h-5 w-5 text-gray-400" />
                            </div>
                            <div>
                              <p className="text-sm font-medium text-gray-700">
                                Member Since
                              </p>
                              <p className="text-gray-900">
                                {formatDate(userProfile.created_at)}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="orders">
                <UserOrders />
              </TabsContent>
            </Tabs>
          </div>

          {/* Account Statistics */}
          <div className="space-y-6">
            {/* Account Status Card */}
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-lg text-blue-600">
                  Account Status
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium text-gray-700">
                      Status
                    </span>
                    <Badge className={getStatusColor(userProfile.is_active)}>
                      {userProfile.is_active ? "Active" : "Inactive"}
                    </Badge>
                  </div>

                  <div className="flex items-center space-x-2">
                    <Shield className="h-4 w-4 text-gray-400" />
                    <div>
                      <p className="text-sm font-medium text-gray-700">Role</p>
                      <p className="text-sm text-gray-600 capitalize">
                        {userProfile.role}
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Order Statistics Card */}
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-lg text-gray-900">
                  Order Statistics
                </CardTitle>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-4">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600">
                      {userProfile.orders.length}
                    </div>
                    <p className="text-sm text-gray-600">Total Orders</p>
                  </div>

                  <Separator className="bg-gray-200" />

                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-600">
                      {userProfile.reservations.length}
                    </div>
                    <p className="text-sm text-gray-600">Reservations</p>
                  </div>

                  <Separator className="bg-gray-200" />

                  <div className="text-center">
                    <div className="text-3xl font-bold text-purple-600">
                      {userProfile.favourite_products.length}
                    </div>
                    <p className="text-sm text-gray-600">Favourites</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Profile;
