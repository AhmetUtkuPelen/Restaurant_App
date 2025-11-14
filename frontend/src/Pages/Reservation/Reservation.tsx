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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/Components/ui/select";
import { Badge } from "@/Components/ui/badge";
import { Separator } from "@/Components/ui/separator";
import {
  Calendar,
  Clock,
  Users,
  MapPin,
  Mail,
  CheckCircle,
} from "lucide-react";

interface TableOption {
  id: string;
  name: string;
  capacity: number;
  location: string;
  price: number;
  image: string;
  features: string[];
  available: boolean;
}

interface ReservationData {
  date: string;
  time: string;
  guests: number;
  tableId: string;
  customerName: string;
  customerEmail: string;
  customerPhone: string;
  specialRequests: string;
}

const Reservation = () => {
  const [reservationData, setReservationData] = useState<ReservationData>({
    date: "",
    time: "",
    guests: 2,
    tableId: "",
    customerName: "",
    customerEmail: "",
    customerPhone: "",
    specialRequests: "",
  });

  const [currentStep, setCurrentStep] = useState(1);
  const [isLoading, setIsLoading] = useState(false);

  // Mock table data
  const tableOptions: TableOption[] = [
    {
      id: "table-1",
      name: "Romantic Corner",
      capacity: 2,
      location: "Window Side",
      price: 25,
      image:
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop",
      features: ["Window View", "Intimate Setting", "Candlelit"],
      available: true,
    },
    {
      id: "table-2",
      name: "Family Table",
      capacity: 6,
      location: "Main Hall",
      price: 40,
      image:
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&h=300&fit=crop",
      features: ["Spacious", "Family Friendly", "Central Location"],
      available: true,
    },
    {
      id: "table-3",
      name: "Business Booth",
      capacity: 4,
      location: "Quiet Section",
      price: 35,
      image:
        "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=400&h=300&fit=crop",
      features: ["Private", "Business Friendly", "Power Outlets"],
      available: false,
    },
    {
      id: "table-4",
      name: "Garden Terrace",
      capacity: 8,
      location: "Outdoor",
      price: 50,
      image:
        "https://images.unsplash.com/photo-1578474846511-04ba529f0b88?w=400&h=300&fit=crop",
      features: ["Outdoor Dining", "Garden View", "Fresh Air"],
      available: true,
    },
    {
      id: "table-5",
      name: "Chef's Counter",
      capacity: 3,
      location: "Kitchen View",
      price: 45,
      image:
        "https://images.unsplash.com/photo-1551218808-94e220e084d2?w=400&h=300&fit=crop",
      features: ["Kitchen View", "Interactive", "Premium Experience"],
      available: true,
    },
    {
      id: "table-6",
      name: "VIP Lounge",
      capacity: 10,
      location: "Private Room",
      price: 75,
      image:
        "https://images.unsplash.com/photo-1559329007-40df8a9345d8?w=400&h=300&fit=crop",
      features: ["Private Room", "Luxury Setting", "Dedicated Service"],
      available: true,
    },
  ];

  // Available time slots
  const timeSlots = [
    "11:00 AM",
    "11:30 AM",
    "12:00 PM",
    "12:30 PM",
    "1:00 PM",
    "1:30 PM",
    "2:00 PM",
    "2:30 PM",
    "6:00 PM",
    "6:30 PM",
    "7:00 PM",
    "7:30 PM",
    "8:00 PM",
    "8:30 PM",
    "9:00 PM",
    "9:30 PM",
  ];

  const handleInputChange = (
    field: keyof ReservationData,
    value: string | number
  ) => {
    setReservationData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleNextStep = () => {
    if (currentStep < 3) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const handleSubmitReservation = async () => {
    setIsLoading(true);
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));
    setIsLoading(false);
    setCurrentStep(4); // Success step
  };

  const getAvailableTables = () => {
    return tableOptions.filter(
      (table) => table.available && table.capacity >= reservationData.guests
    );
  };

  const selectedTable = tableOptions.find(
    (table) => table.id === reservationData.tableId
  );

  const getTotalPrice = () => {
    return selectedTable ? selectedTable.price : 0;
  };

  const isStepValid = (step: number) => {
    switch (step) {
      case 1:
        return (
          reservationData.date &&
          reservationData.time &&
          reservationData.guests > 0
        );
      case 2:
        return reservationData.tableId;
      case 3:
        return (
          reservationData.customerName &&
          reservationData.customerEmail &&
          reservationData.customerPhone
        );
      default:
        return false;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Make a Reservation
          </h1>
          <p className="text-xl text-gray-600">
            Reserve your perfect dining experience
          </p>
        </div>

        {/* Progress Steps */}
        <div className="mb-8">
          <div className="flex items-center justify-center space-x-8">
            {[1, 2, 3].map((step) => (
              <div key={step} className="flex items-center">
                <div
                  className={`
                  flex items-center justify-center w-10 h-10 rounded-full border-2 font-semibold
                  ${
                    currentStep >= step
                      ? "bg-blue-600 border-blue-600 text-white"
                      : "bg-white border-gray-300 text-gray-400"
                  }
                `}
                >
                  {currentStep > step ? (
                    <CheckCircle className="h-6 w-6" />
                  ) : (
                    step
                  )}
                </div>
                <span
                  className={`ml-2 font-medium ${
                    currentStep >= step ? "text-blue-600" : "text-gray-400"
                  }`}
                >
                  {step === 1 && "Date & Time"}
                  {step === 2 && "Select Table"}
                  {step === 3 && "Your Details"}
                </span>
                {step < 3 && (
                  <div
                    className={`w-16 h-0.5 ml-4 ${
                      currentStep > step ? "bg-blue-600" : "bg-gray-300"
                    }`}
                  />
                )}
              </div>
            ))}
          </div>
        </div>

        {currentStep === 1 && (
          <Card className="border-gray-200 shadow-lg">
            <CardHeader className="bg-white border-b border-gray-100">
              <CardTitle className="text-2xl text-gray-900 flex items-center">
                <Calendar className="h-6 w-6 mr-2 text-blue-600" />
                Select Date & Time
              </CardTitle>
              <CardDescription className="text-gray-600">
                Choose your preferred date, time, and number of guests
              </CardDescription>
            </CardHeader>
            <CardContent className="p-8 bg-white">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="space-y-4">
                  <Label
                    htmlFor="date"
                    className="text-lg font-medium text-gray-700"
                  >
                    Reservation Date
                  </Label>
                  <Input
                    id="date"
                    type="date"
                    value={reservationData.date}
                    onChange={(e) => handleInputChange("date", e.target.value)}
                    min={new Date().toISOString().split("T")[0]}
                    className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 text-lg p-3"
                  />
                </div>

                <div className="space-y-4">
                  <Label className="text-lg font-medium text-gray-700">
                    Preferred Time
                  </Label>
                  <Select
                    value={reservationData.time}
                    onValueChange={(value) => handleInputChange("time", value)}
                  >
                    <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 text-lg p-3">
                      <SelectValue placeholder="Select time" />
                    </SelectTrigger>
                    <SelectContent>
                      {timeSlots.map((time) => (
                        <SelectItem key={time} value={time}>
                          <div className="flex items-center">
                            <Clock className="h-4 w-4 mr-2" />
                            {time}
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-4">
                  <Label className="text-lg font-medium text-gray-700">
                    Number of Guests
                  </Label>
                  <Select
                    value={reservationData.guests.toString()}
                    onValueChange={(value) =>
                      handleInputChange("guests", parseInt(value))
                    }
                  >
                    <SelectTrigger className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 text-lg p-3">
                      <SelectValue placeholder="Select guests" />
                    </SelectTrigger>
                    <SelectContent>
                      {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                        <SelectItem key={num} value={num.toString()}>
                          <div className="flex items-center">
                            <Users className="h-4 w-4 mr-2" />
                            {num} {num === 1 ? "Guest" : "Guests"}
                          </div>
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="flex justify-end mt-8">
                <Button
                  onClick={handleNextStep}
                  disabled={!isStepValid(1)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg"
                >
                  Continue to Table Selection
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {currentStep === 2 && (
          <Card className="border-gray-200 shadow-lg">
            <CardHeader className="bg-white border-b border-gray-100">
              <CardTitle className="text-2xl text-gray-900 flex items-center">
                <MapPin className="h-6 w-6 mr-2 text-blue-600" />
                Choose Your Table
              </CardTitle>
              <CardDescription className="text-gray-600">
                Select from available tables for {reservationData.guests} guests
                on {reservationData.date} at {reservationData.time}
              </CardDescription>
            </CardHeader>
            <CardContent className="p-8 bg-white">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {getAvailableTables().map((table) => (
                  <div
                    key={table.id}
                    className={`
                      relative border-2 rounded-lg overflow-hidden cursor-pointer transition-all duration-200
                      ${
                        reservationData.tableId === table.id
                          ? "border-blue-600 ring-2 ring-blue-200"
                          : "border-gray-200 hover:border-gray-300"
                      }
                    `}
                    onClick={() => handleInputChange("tableId", table.id)}
                  >
                    <div className="aspect-video relative">
                      <img
                        src={table.image}
                        alt={table.name}
                        className="w-full h-full object-cover"
                      />
                      {reservationData.tableId === table.id && (
                        <div className="absolute top-2 right-2 bg-blue-600 text-white p-1 rounded-full">
                          <CheckCircle className="h-5 w-5" />
                        </div>
                      )}
                    </div>

                    <div className="p-4">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="text-lg font-semibold text-gray-900">
                          {table.name}
                        </h3>
                        <Badge className="bg-blue-100 text-blue-800">
                          ${table.price}
                        </Badge>
                      </div>

                      <div className="flex items-center text-gray-600 mb-2">
                        <Users className="h-4 w-4 mr-1" />
                        <span className="text-sm">
                          Up to {table.capacity} guests
                        </span>
                      </div>

                      <div className="flex items-center text-gray-600 mb-3">
                        <MapPin className="h-4 w-4 mr-1" />
                        <span className="text-sm">{table.location}</span>
                      </div>

                      <div className="flex flex-wrap gap-1">
                        {table.features.map((feature, index) => (
                          <Badge
                            key={index}
                            variant="outline"
                            className="text-xs"
                          >
                            {feature}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <div className="flex justify-between mt-8">
                <Button
                  onClick={handlePrevStep}
                  variant="outline"
                  className="border-gray-300 text-gray-700 hover:bg-gray-50 px-8 py-3 text-lg"
                >
                  Back
                </Button>
                <Button
                  onClick={handleNextStep}
                  disabled={!isStepValid(2)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg"
                >
                  Continue to Details
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {currentStep === 3 && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <Card className="border-gray-200 shadow-lg">
                <CardHeader className="bg-white border-b border-gray-100">
                  <CardTitle className="text-2xl text-gray-900 flex items-center">
                    <Mail className="h-6 w-6 mr-2 text-blue-600" />
                    Your Details
                  </CardTitle>
                  <CardDescription className="text-gray-600">
                    Please provide your contact information
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-8 bg-white">
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div className="space-y-2">
                        <Label
                          htmlFor="name"
                          className="text-gray-700 font-medium"
                        >
                          Full Name *
                        </Label>
                        <Input
                          id="name"
                          value={reservationData.customerName}
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
                          value={reservationData.customerPhone}
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
                        value={reservationData.customerEmail}
                        onChange={(e) =>
                          handleInputChange("customerEmail", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500"
                        placeholder="your.email@example.com"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label
                        htmlFor="requests"
                        className="text-gray-700 font-medium"
                      >
                        Special Requests (Optional)
                      </Label>
                      <Textarea
                        id="requests"
                        value={reservationData.specialRequests}
                        onChange={(e) =>
                          handleInputChange("specialRequests", e.target.value)
                        }
                        className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 min-h-[100px]"
                        placeholder="Any dietary restrictions, celebrations, or special accommodations..."
                      />
                    </div>
                  </div>

                  <div className="flex justify-between mt-8">
                    <Button
                      onClick={handlePrevStep}
                      variant="outline"
                      className="border-gray-300 text-gray-700 hover:bg-gray-50 px-8 py-3 text-lg"
                    >
                      Back
                    </Button>
                    <Button
                      onClick={handleSubmitReservation}
                      disabled={!isStepValid(3) || isLoading}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg"
                    >
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                          Processing...
                        </>
                      ) : (
                        "Confirm Reservation"
                      )}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Reservation Summary */}
            <div>
              <Card className="border-gray-200 shadow-lg sticky top-8">
                <CardHeader className="bg-blue-50 border-b border-blue-100">
                  <CardTitle className="text-xl text-gray-900">
                    Reservation Summary
                  </CardTitle>
                </CardHeader>
                <CardContent className="p-6 bg-white">
                  <div className="space-y-4">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Date:</span>
                      <span className="font-medium">
                        {reservationData.date}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Time:</span>
                      <span className="font-medium">
                        {reservationData.time}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Guests:</span>
                      <span className="font-medium">
                        {reservationData.guests}
                      </span>
                    </div>

                    {selectedTable && (
                      <>
                        <Separator className="bg-gray-200" />
                        <div>
                          <div className="flex justify-between mb-2">
                            <span className="text-gray-600">Table:</span>
                            <span className="font-medium">
                              {selectedTable.name}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Location:</span>
                            <span className="font-medium">
                              {selectedTable.location}
                            </span>
                          </div>
                        </div>

                        <Separator className="bg-gray-200" />
                        <div className="flex justify-between text-lg font-semibold">
                          <span>Total:</span>
                          <span className="text-blue-600">
                            ${getTotalPrice()}
                          </span>
                        </div>
                      </>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {currentStep === 4 && (
          <Card className="border-green-200 shadow-lg max-w-2xl mx-auto">
            <CardContent className="p-12 bg-white text-center">
              <div className="mb-6">
                <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
                <h2 className="text-3xl font-bold text-gray-900 mb-2">
                  Reservation Confirmed!
                </h2>
                <p className="text-xl text-gray-600">
                  Thank you for choosing our restaurant
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-6 mb-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Reservation Details
                </h3>
                <div className="space-y-2 text-left">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Confirmation #:</span>
                    <span className="font-medium">
                      RSV-{Date.now().toString().slice(-6)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Date & Time:</span>
                    <span className="font-medium">
                      {reservationData.date} at {reservationData.time}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Table:</span>
                    <span className="font-medium">{selectedTable?.name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Guests:</span>
                    <span className="font-medium">
                      {reservationData.guests}
                    </span>
                  </div>
                </div>
              </div>

              <p className="text-gray-600 mb-6">
                A confirmation email has been sent to{" "}
                {reservationData.customerEmail}
              </p>

              <Button
                onClick={() => window.location.reload()}
                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg"
              >
                Make Another Reservation
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
};

export default Reservation;
