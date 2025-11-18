import { useState } from "react";
import { useNavigate } from "react-router-dom";
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
import {
  Calendar,
  Clock,
  Users,
  MapPin,
  CheckCircle,
  AlertCircle,
} from "lucide-react";
import { useTables, useCreateReservation } from "@/hooks/useReservation";
import PaymentForm from "@/Components/Payment/PaymentForm";

interface ReservationData {
  date: string;
  time: string;
  guests: number;
  tableId: number | null;
  specialRequests: string;
}

const Reservation = () => {
  const navigate = useNavigate();
  const {
    data: tables = [],
    isLoading: tablesLoading,
    error: tablesError,
  } = useTables();
  const createReservation = useCreateReservation();

  const [reservationData, setReservationData] = useState<ReservationData>({
    date: "",
    time: "",
    guests: 2,
    tableId: null,
    specialRequests: "",
  });

  const [currentStep, setCurrentStep] = useState(1);
  const [reservationSuccess, setReservationSuccess] = useState(false);
  const [confirmationNumber, setConfirmationNumber] = useState("");
  const [reservationId, setReservationId] = useState<number | null>(null);

  // Fixed reservation fee
  const RESERVATION_FEE = 50; // ₺50 reservation fee

  // Helper function to format location
  const formatLocation = (location: string) => {
    const locationMap: Record<string, string> = {
      window: "Window Side",
      patio: "Patio",
      main_dining_room: "Main Dining Room",
    };
    return locationMap[location] || location;
  };

  // Helper function to get table image based on location
  const getTableImage = (location: string) => {
    const imageMap: Record<string, string> = {
      window:
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400&h=300&fit=crop",
      patio:
        "https://images.unsplash.com/photo-1578474846511-04ba529f0b88?w=400&h=300&fit=crop",
      main_dining_room:
        "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=400&h=300&fit=crop",
    };
    return imageMap[location] || imageMap.main_dining_room;
  };

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
    value: string | number | null
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

  // Helper function to convert 12-hour time to 24-hour format
  const convertTo24Hour = (time12h: string) => {
    const [time, modifier] = time12h.split(" ");
    const [hoursStr, minutes] = time.split(":");
    let hours = hoursStr;

    if (hours === "12") {
      hours = "00";
    }

    if (modifier === "PM" && hours !== "12") {
      hours = String(parseInt(hours, 10) + 12);
    }

    if (modifier === "AM" && hours === "12") {
      hours = "00";
    }

    return `${hours.padStart(2, "0")}:${minutes}`;
  };

  const handleSubmitReservation = async () => {
    if (!reservationData.tableId) return;

    try {
      // Convert 12-hour time to 24-hour format
      const time24h = convertTo24Hour(reservationData.time);

      // Combine date and time into ISO datetime string
      const reservationDateTime = new Date(
        `${reservationData.date}T${time24h}:00`
      ).toISOString();

      const result = await createReservation.mutateAsync({
        table_id: reservationData.tableId,
        reservation_time: reservationDateTime,
        number_of_guests: reservationData.guests,
        special_requests: reservationData.specialRequests || undefined,
      });

      setReservationId(result.reservation.id);
      setCurrentStep(3); // Move to payment step
    } catch (error) {
      console.error("Failed to create reservation:", error);
      alert("Failed to create reservation. Please try again.");
    }
  };

  const handlePaymentSuccess = () => {
    setConfirmationNumber(`RSV-${Date.now().toString().slice(-6)}`);
    setReservationSuccess(true);
  };

  const handlePaymentError = (error: string) => {
    alert(`Payment failed: ${error}`);
  };

  const getAvailableTables = () => {
    return tables.filter(
      (table) => table.is_available && table.capacity >= reservationData.guests
    );
  };

  const selectedTable = tables.find(
    (table) => table.id === reservationData.tableId
  );

  const isStepValid = (step: number) => {
    switch (step) {
      case 1:
        return (
          reservationData.date &&
          reservationData.time &&
          reservationData.guests > 0
        );
      case 2:
        return reservationData.tableId !== null;
      default:
        return false;
    }
  };

  // Loading state
  if (tablesLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Error state
  if (tablesError) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="p-8 text-center">
            <AlertCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">
              Error Loading Tables
            </h3>
            <p className="text-gray-600 mb-4">
              {tablesError instanceof Error
                ? tablesError.message
                : "Failed to load tables"}
            </p>
            <Button onClick={() => window.location.reload()}>Try Again</Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // Success state
  if (reservationSuccess) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
          <Card className="border-green-200 shadow-lg">
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
                    <span className="font-medium">{confirmationNumber}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Date & Time:</span>
                    <span className="font-medium">
                      {reservationData.date} at {reservationData.time}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Table:</span>
                    <span className="font-medium">
                      {selectedTable?.table_number}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Guests:</span>
                    <span className="font-medium">
                      {reservationData.guests}
                    </span>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <Button
                  onClick={() => navigate("/userReservations")}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg w-full"
                >
                  View My Reservations
                </Button>
                <Button
                  onClick={() => window.location.reload()}
                  variant="outline"
                  className="px-8 py-3 text-lg w-full"
                >
                  Make Another Reservation
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
                  {step === 3 && "Payment"}
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

              <div className="mt-6">
                <Label
                  htmlFor="requests"
                  className="text-lg font-medium text-gray-700"
                >
                  Special Requests (Optional)
                </Label>
                <Textarea
                  id="requests"
                  value={reservationData.specialRequests}
                  onChange={(e) =>
                    handleInputChange("specialRequests", e.target.value)
                  }
                  className="border-gray-300 focus:border-blue-500 focus:ring-blue-500 min-h-[100px] mt-2"
                  placeholder="Any dietary restrictions, celebrations, or special accommodations..."
                />
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
              {getAvailableTables().length === 0 ? (
                <div className="text-center py-12">
                  <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    No Available Tables
                  </h3>
                  <p className="text-gray-600 mb-4">
                    No tables available for {reservationData.guests} guests. Try
                    selecting fewer guests or a different date/time.
                  </p>
                  <Button onClick={handlePrevStep} variant="outline">
                    Go Back
                  </Button>
                </div>
              ) : (
                <>
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
                            src={getTableImage(table.location)}
                            alt={table.table_number}
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
                              Table {table.table_number}
                            </h3>
                            <Badge className="bg-green-100 text-green-800">
                              Available
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
                            <span className="text-sm">
                              {formatLocation(table.location)}
                            </span>
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
                      onClick={handleSubmitReservation}
                      disabled={!isStepValid(2) || createReservation.isPending}
                      className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg"
                    >
                      {createReservation.isPending ? (
                        <>
                          <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                          Creating Reservation...
                        </>
                      ) : (
                        "Continue to Payment"
                      )}
                    </Button>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        )}

        {currentStep === 3 && reservationId && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <PaymentForm
                amount={RESERVATION_FEE}
                reservationId={reservationId}
                paymentType="reservation"
                onSuccess={handlePaymentSuccess}
                onError={handlePaymentError}
              />
            </div>

            {/* Reservation Summary */}
            <div>
              <Card className="sticky top-8">
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
                        <div className="border-t pt-4">
                          <div className="flex justify-between mb-2">
                            <span className="text-gray-600">Table:</span>
                            <span className="font-medium">
                              {selectedTable.table_number}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Location:</span>
                            <span className="font-medium">
                              {formatLocation(selectedTable.location)}
                            </span>
                          </div>
                        </div>
                      </>
                    )}

                    <div className="border-t pt-4">
                      <div className="flex justify-between text-lg font-semibold">
                        <span>Reservation Fee:</span>
                        <span className="text-blue-600">
                          ₺{RESERVATION_FEE}
                        </span>
                      </div>
                      <p className="text-sm text-gray-500 mt-1">
                        Refundable if cancelled 24h in advance
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Reservation;
