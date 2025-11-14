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
import { Avatar, AvatarFallback, AvatarImage } from "@/Components/ui/avatar";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/Components/ui/tabs";
import { Separator } from "@/Components/ui/separator";
import { Camera, Save, Eye, EyeOff } from "lucide-react";

interface UserData {
  username: string;
  email: string;
  address: string;
  phone: string;
  profilePicture: string;
}

const UserSettings = () => {
  const [userData, setUserData] = useState<UserData>({
    username: "john_doe",
    email: "john.doe@example.com",
    address: "123 Main Street, City, State 12345",
    phone: "+1 (555) 123-4567",
    profilePicture: "",
  });

  const [passwords, setPasswords] = useState({
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
  });

  const [showPasswords, setShowPasswords] = useState({
    current: false,
    new: false,
    confirm: false,
  });

  const [isLoading, setIsLoading] = useState(false);

  const handleInputChange = (field: keyof UserData, value: string) => {
    setUserData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handlePasswordChange = (
    field: keyof typeof passwords,
    value: string
  ) => {
    setPasswords((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleProfilePictureChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        setUserData((prev) => ({
          ...prev,
          profilePicture: e.target?.result as string,
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSaveProfile = async () => {
    setIsLoading(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsLoading(false);
    // Handle success/error states here
  };

  const handleChangePassword = async () => {
    if (passwords.newPassword !== passwords.confirmPassword) {
      alert("New passwords do not match");
      return;
    }
    setIsLoading(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setIsLoading(false);
    setPasswords({ currentPassword: "", newPassword: "", confirmPassword: "" });
    // Handle success/error states here
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Account Settings</h1>
          <p className="text-gray-600 mt-2">
            Manage your account information and preferences
          </p>
        </div>

        <Tabs defaultValue="profile" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2 bg-white border border-gray-200">
            <TabsTrigger
              value="profile"
              className="data-[state=active]:bg-blue-600 data-[state=active]:text-white"
            >
              Profile Information
            </TabsTrigger>
            <TabsTrigger
              value="security"
              className="data-[state=active]:bg-blue-600 data-[state=active]:text-white"
            >
              Security
            </TabsTrigger>
          </TabsList>

          <TabsContent value="profile">
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-xl text-gray-900">
                  Profile Information
                </CardTitle>
                <CardDescription className="text-gray-600">
                  Update your personal information and profile picture
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-6">
                  {/* Profile Picture Section */}
                  <div className="flex items-center space-x-6">
                    <div className="relative">
                      <Avatar className="h-24 w-24 border-4 border-gray-200">
                        <AvatarImage
                          src={userData.profilePicture}
                          alt="Profile picture"
                        />
                        <AvatarFallback className="bg-blue-100 text-blue-600 text-xl font-semibold">
                          {userData.username.charAt(0).toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <label
                        htmlFor="profile-picture"
                        className="absolute -bottom-2 -right-2 bg-blue-600 hover:bg-blue-700 text-white p-2 rounded-full cursor-pointer transition-colors shadow-lg"
                      >
                        <Camera className="h-4 w-4" />
                        <input
                          id="profile-picture"
                          type="file"
                          accept="image/*"
                          onChange={handleProfilePictureChange}
                          className="hidden"
                        />
                      </label>
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">
                        Profile Picture
                      </h3>
                      <p className="text-sm text-gray-600">
                        Click the camera icon to upload a new profile picture
                      </p>
                    </div>
                  </div>

                  <Separator className="bg-gray-200" />

                  {/* Form Fields */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label
                        htmlFor="username"
                        className="text-gray-700 font-medium"
                      >
                        Username
                      </Label>
                      <Input
                        id="username"
                        value={userData.username}
                        onChange={(e) =>
                          handleInputChange("username", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label
                        htmlFor="email"
                        className="text-gray-700 font-medium"
                      >
                        Email Address
                      </Label>
                      <Input
                        id="email"
                        type="email"
                        value={userData.email}
                        onChange={(e) =>
                          handleInputChange("email", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label
                        htmlFor="phone"
                        className="text-gray-700 font-medium"
                      >
                        Phone Number
                      </Label>
                      <Input
                        id="phone"
                        value={userData.phone}
                        onChange={(e) =>
                          handleInputChange("phone", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                      />
                    </div>

                    <div className="space-y-2 md:col-span-2">
                      <Label
                        htmlFor="address"
                        className="text-gray-700 font-medium"
                      >
                        Address
                      </Label>
                      <Textarea
                        id="address"
                        value={userData.address}
                        onChange={(e) =>
                          handleInputChange("address", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 min-h-[100px]"
                        placeholder="Enter your full address"
                      />
                    </div>
                  </div>

                  <div className="flex justify-end pt-4">
                    <Button
                      onClick={handleSaveProfile}
                      disabled={isLoading}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6"
                    >
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Saving...
                        </>
                      ) : (
                        <>
                          <Save className="h-4 w-4 mr-2" />
                          Save Changes
                        </>
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="security">
            <Card className="border-gray-200 shadow-sm">
              <CardHeader className="bg-white border-b border-gray-100">
                <CardTitle className="text-xl text-gray-900">
                  Change Password
                </CardTitle>
                <CardDescription className="text-gray-600">
                  Update your password to keep your account secure
                </CardDescription>
              </CardHeader>
              <CardContent className="p-6 bg-white">
                <div className="space-y-6 max-w-md">
                  <div className="space-y-2">
                    <Label
                      htmlFor="current-password"
                      className="text-gray-700 font-medium"
                    >
                      Current Password
                    </Label>
                    <div className="relative">
                      <Input
                        id="current-password"
                        type={showPasswords.current ? "text" : "password"}
                        value={passwords.currentPassword}
                        onChange={(e) =>
                          handlePasswordChange(
                            "currentPassword",
                            e.target.value
                          )
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 pr-10"
                      />
                      <button
                        type="button"
                        onClick={() =>
                          setShowPasswords((prev) => ({
                            ...prev,
                            current: !prev.current,
                          }))
                        }
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPasswords.current ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label
                      htmlFor="new-password"
                      className="text-gray-700 font-medium"
                    >
                      New Password
                    </Label>
                    <div className="relative">
                      <Input
                        id="new-password"
                        type={showPasswords.new ? "text" : "password"}
                        value={passwords.newPassword}
                        onChange={(e) =>
                          handlePasswordChange("newPassword", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 pr-10"
                      />
                      <button
                        type="button"
                        onClick={() =>
                          setShowPasswords((prev) => ({
                            ...prev,
                            new: !prev.new,
                          }))
                        }
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPasswords.new ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <Label
                      htmlFor="confirm-password"
                      className="text-gray-700 font-medium"
                    >
                      Confirm New Password
                    </Label>
                    <div className="relative">
                      <Input
                        id="confirm-password"
                        type={showPasswords.confirm ? "text" : "password"}
                        value={passwords.confirmPassword}
                        onChange={(e) =>
                          handlePasswordChange(
                            "confirmPassword",
                            e.target.value
                          )
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 pr-10"
                      />
                      <button
                        type="button"
                        onClick={() =>
                          setShowPasswords((prev) => ({
                            ...prev,
                            confirm: !prev.confirm,
                          }))
                        }
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPasswords.confirm ? (
                          <EyeOff className="h-4 w-4" />
                        ) : (
                          <Eye className="h-4 w-4" />
                        )}
                      </button>
                    </div>
                  </div>

                  <div className="flex justify-end pt-4">
                    <Button
                      onClick={handleChangePassword}
                      disabled={
                        isLoading ||
                        !passwords.currentPassword ||
                        !passwords.newPassword ||
                        !passwords.confirmPassword
                      }
                      className="bg-blue-600 hover:bg-blue-700 text-white px-6"
                    >
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Updating...
                        </>
                      ) : (
                        "Update Password"
                      )}
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default UserSettings;
