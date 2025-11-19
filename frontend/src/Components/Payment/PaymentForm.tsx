/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/Components/ui/card";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Label } from "@/Components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/Components/ui/select";
import { Separator } from "@/Components/ui/separator";
import { CreditCard, Lock } from "lucide-react";
import { useCreatePayment } from "@/hooks/usePayment";
import { usePaymentStore } from "@/Zustand/Payment/PaymentState";
import { toast } from "sonner";

interface PaymentFormProps {
  amount: number;
  orderId?: number;
  reservationId?: number;
  paymentType: "cart" | "reservation";
  onSuccess?: (paymentId: number) => void;
  onError?: (error: string) => void;
}

const PaymentForm = ({
  amount,
  orderId,
  reservationId,
  paymentType,
  onSuccess,
  onError,
}: PaymentFormProps) => {
  const createPayment = useCreatePayment();
  const { isProcessing } = usePaymentStore();

  const [formData, setFormData] = useState({
    cardNumber: "",
    expiryMonth: "",
    expiryYear: "",
    cvc: "",
    cardHolderName: "",
    contactName: "",
    city: "",
    country: "",
    address: "",
    zipCode: "",
  });

  const handleInputChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const formatCardNumber = (value: string) => {
    const v = value.replace(/\s+/g, "").replace(/[^0-9]/gi, "");
    const matches = v.match(/\d{4,16}/g);
    const match = (matches && matches[0]) || "";
    const parts = [];
    for (let i = 0, len = match.length; i < len; i += 4) {
      parts.push(match.substring(i, i + 4));
    }
    if (parts.length) {
      return parts.join(" ");
    } else {
      return v;
    }
  };

  const handleCardNumberChange = (value: string) => {
    const formatted = formatCardNumber(value);
    handleInputChange("cardNumber", formatted);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (
      !formData.cardNumber ||
      !formData.expiryMonth ||
      !formData.expiryYear ||
      !formData.cvc ||
      !formData.cardHolderName
    ) {
      toast.error("Please fill in all card information");
      return;
    }

    try {
      // Get user's IP address
      const ipAddress = "127.0.0.1"; // For development only , If in Production this is gonna change

      const paymentData = {
        amount,
        currency: "TRY",
        installment: 1,
        ip_address: ipAddress,
        order_ids: orderId ? [orderId] : undefined,
        reservation_id: reservationId,
        metadata: {
          card_info: {
            cardNumber: formData.cardNumber.replace(/\s/g, ""),
            expiryMonth: formData.expiryMonth,
            expiryYear: formData.expiryYear,
            cvc: formData.cvc,
            cardHolderName: formData.cardHolderName,
          },
          billing_address: {
            contactName: formData.contactName,
            city: formData.city,
            country: formData.country,
            address: formData.address,
            zipCode: formData.zipCode,
          },
        },
      };

      const result = await createPayment.mutateAsync(paymentData);

      if (result.status === "completed") {
        onSuccess?.(result.id);
      } else {
        // For demo - development purposes, simulate payment \\
        onSuccess?.(result.id);
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || "Something went wrong";
      toast.error(errorMessage);
      onError?.(errorMessage);
    }
  };

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 10 }, (_, i) => currentYear + i);
  const months = Array.from({ length: 12 }, (_, i) =>
    String(i + 1).padStart(2, "0")
  );

  return (
    <div className="space-y-6">
      {/* Demo Payment Notice */}
      <Card className="border-blue-200 bg-blue-50">
        <CardContent className="p-4">
          <div className="flex items-start gap-3">
            <CreditCard className="h-5 w-5 text-blue-600 mt-0.5" />
            <div>
              <h4 className="font-medium text-blue-900 mb-1">Demo Payment System</h4>
              <p className="text-sm text-blue-700">
                This is a demonstration payment system. You can enter any card details to test the checkout process. 
                No real charges will be made.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Payment Form */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Lock className="h-5 w-5 mr-2 text-green-600" />
            Secure Payment
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Card Information */}
            <div className="space-y-4">
              <h3 className="font-medium text-gray-900">Card Information</h3>

              <div className="space-y-2">
                <Label htmlFor="cardNumber">Card Number *</Label>
                <Input
                  id="cardNumber"
                  value={formData.cardNumber}
                  onChange={(e) => handleCardNumberChange(e.target.value)}
                  placeholder="1234 5678 9012 3456"
                  maxLength={19}
                  className="font-mono"
                />
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="expiryMonth">Month *</Label>
                  <Select
                    value={formData.expiryMonth}
                    onValueChange={(value) =>
                      handleInputChange("expiryMonth", value)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="MM" />
                    </SelectTrigger>
                    <SelectContent>
                      {months.map((month) => (
                        <SelectItem key={month} value={month}>
                          {month}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="expiryYear">Year *</Label>
                  <Select
                    value={formData.expiryYear}
                    onValueChange={(value) =>
                      handleInputChange("expiryYear", value)
                    }
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="YYYY" />
                    </SelectTrigger>
                    <SelectContent>
                      {years.map((year) => (
                        <SelectItem key={year} value={year.toString()}>
                          {year}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="cvc">CVC *</Label>
                  <Input
                    id="cvc"
                    value={formData.cvc}
                    onChange={(e) => handleInputChange("cvc", e.target.value)}
                    placeholder="123"
                    maxLength={4}
                    className="font-mono"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="cardHolderName">Cardholder Name *</Label>
                <Input
                  id="cardHolderName"
                  value={formData.cardHolderName}
                  onChange={(e) =>
                    handleInputChange("cardHolderName", e.target.value)
                  }
                  placeholder="John Doe"
                />
              </div>
            </div>

            <Separator />

            {/* Billing Address */}
            <div className="space-y-4">
              <h3 className="font-medium text-gray-900">Billing Address</h3>

              <div className="space-y-2">
                <Label htmlFor="contactName">Contact Name *</Label>
                <Input
                  id="contactName"
                  value={formData.contactName}
                  onChange={(e) =>
                    handleInputChange("contactName", e.target.value)
                  }
                  placeholder="John Doe"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="city">City *</Label>
                  <Input
                    id="city"
                    value={formData.city}
                    onChange={(e) => handleInputChange("city", e.target.value)}
                    placeholder="Istanbul"
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="country">Country *</Label>
                  <Input
                    id="country"
                    value={formData.country}
                    onChange={(e) =>
                      handleInputChange("country", e.target.value)
                    }
                    placeholder="Turkey"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label htmlFor="address">Address *</Label>
                <Input
                  id="address"
                  value={formData.address}
                  onChange={(e) => handleInputChange("address", e.target.value)}
                  placeholder="123 Main Street, Apartment 4B"
                />
              </div>

              <div className="space-y-2">
                <Label htmlFor="zipCode">Zip Code</Label>
                <Input
                  id="zipCode"
                  value={formData.zipCode}
                  onChange={(e) => handleInputChange("zipCode", e.target.value)}
                  placeholder="34000"
                />
              </div>
            </div>

            <Separator />

            {/* Payment Summary */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="flex justify-between items-center">
                <span className="font-medium text-gray-900">Total Amount:</span>
                <span className="text-2xl font-bold text-green-600">
                  ₺{amount.toFixed(2)}
                </span>
              </div>
              <div className="text-sm text-gray-600 mt-1">
                Payment for {paymentType === "cart" ? "Order" : "Reservation"}
              </div>
            </div>

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={isProcessing}
              className="w-full bg-green-600 hover:bg-green-700 text-white py-3 text-lg cursor-pointer"
            >
              {isProcessing ? (
                <>
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Processing Payment...
                </>
              ) : (
                <>
                  <Lock className="h-5 w-5 mr-2" />
                  Pay ₺{amount.toFixed(2)}
                </>
              )}
            </Button>

            <div className="text-center text-sm text-gray-500">
              <Lock className="h-4 w-4 inline mr-1" />
              Your payment information is secure and encrypted
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};

export default PaymentForm;
