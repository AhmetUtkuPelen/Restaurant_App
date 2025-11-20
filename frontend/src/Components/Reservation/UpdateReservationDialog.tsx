import { useState, useEffect } from "react";
import { Button } from "@/Components/ui/button";
import { Input } from "@/Components/ui/input";
import { Label } from "@/Components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/Components/ui/dialog";
import { Calendar, Clock, Users, Loader2 } from "lucide-react";
import { useUpdateReservation, useTables } from "@/hooks/useReservation";
import { toast } from "sonner";
import type {Reservation} from "@/hooks/useReservation";

interface UpdateReservationDialogProps {
  reservation: Reservation;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export const UpdateReservationDialog = ({
  reservation,
  open,
  onOpenChange,
}: UpdateReservationDialogProps) => {
  const updateReservation = useUpdateReservation();
  const { data: tables = [] } = useTables();

  const [formData, setFormData] = useState({
    date: "",
    time: "",
    guests: reservation.number_of_guests,
    tableId: reservation.table_id,
    specialRequests: reservation.special_requests || "",
  });

  // Helper for converting 24-hour time to 12-hour time format \\
  const convertTo12Hour = (time24h: string) => {
    const [hoursStr, minutes] = time24h.split(":");
    let hours = parseInt(hoursStr, 10);
    const ampm = hours >= 12 ? "PM" : "AM";
    
    hours = hours % 12;
    hours = hours ? hours : 12;
    
    return `${hours}:${minutes} ${ampm}`;
  };

  // Initialize form data if reservation changes \\
  useEffect(() => {
    if (reservation) {
      const reservationDate = new Date(reservation.reservation_time);
      const dateStr = reservationDate.toISOString().split("T")[0];
      const timeStr = reservationDate.toTimeString().slice(0, 5);
      const time12h = convertTo12Hour(timeStr);

      setFormData({
        date: dateStr,
        time: time12h,
        guests: reservation.number_of_guests,
        tableId: reservation.table_id,
        specialRequests: reservation.special_requests || "",
      });
    }
  }, [reservation]);

  // Helper function for converting 12-hour time to 24-hour time format
  const convertTo24Hour = (time12h: string) => {
    const [time, modifier] = time12h.split(" ");
    const [hoursStr, minutes] = time.split(":");
    let hours = parseInt(hoursStr, 10);

    if (modifier === "AM") {
      if (hours === 12) {
        hours = 0;
      }
    } else if (modifier === "PM") {
      if (hours !== 12) {
        hours += 12;
      }
    }

    return `${hours.toString().padStart(2, "0")}:${minutes}`;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.date || !formData.time) {
      toast.error("Please select date and time");
      return;
    }

    try {
      // Convert 12-hour time to 24-hour time format \\
      const time24h = convertTo24Hour(formData.time);
      const reservationDateTime = `${formData.date}T${time24h}:00`;
      
      const updateData: Record<string, string | number | null> = {};
      
      // include changed fields only \\
      if (reservationDateTime !== reservation.reservation_time) {
        updateData.reservation_time = reservationDateTime;
      }
      
      if (formData.guests !== reservation.number_of_guests) {
        updateData.number_of_guests = formData.guests;
      }
      
      if (formData.tableId !== reservation.table_id) {
        updateData.table_id = formData.tableId;
      }
      
      if (formData.specialRequests !== (reservation.special_requests || "")) {
        updateData.special_requests = formData.specialRequests || null;
      }

      // If nothing changed \\
      if (Object.keys(updateData).length === 0) {
        toast.info("No changes detected !");
        onOpenChange(false);
        return;
      }

      await updateReservation.mutateAsync({
        reservationId: reservation.id,
        data: updateData,
      });

      toast.success("Reservation updated successfully !");
      onOpenChange(false);
    } catch (err) {
      const error = err as { response?: { data?: { detail?: string } } };
      toast.error(error?.response?.data?.detail || "Failed to update reservation");
    }
  };

  const availableTables = tables.filter(
    (table) => table.is_available && table.capacity >= formData.guests
  );

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[500px] bg-gray-800 text-white border-gray-700">
        <DialogHeader>
          <DialogTitle className="text-2xl text-blue-400">
            Update Reservation
          </DialogTitle>
          <DialogDescription className="text-gray-400">
            Modify your reservation details. All fields are optional - only update what you need to change.
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-6 mt-4">
          {/* Date */}
          <div className="space-y-2">
            <Label htmlFor="date" className="text-gray-300 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-blue-400" />
              Date
            </Label>
            <Input
              type="date"
              id="date"
              value={formData.date}
              onChange={(e) => setFormData({ ...formData, date: e.target.value })}
              min={new Date().toISOString().split("T")[0]}
              className="bg-gray-900 border-gray-600 text-white"
              required
            />
          </div>

          {/* Time */}
          <div className="space-y-2">
            <Label htmlFor="time" className="text-gray-300 flex items-center gap-2">
              <Clock className="w-4 h-4 text-green-400" />
              Time
            </Label>
            <select
              id="time"
              value={formData.time}
              onChange={(e) => setFormData({ ...formData, time: e.target.value })}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
              required
            >
              <option value="">Select time</option>
              <option value="11:00 AM">11:00 AM</option>
              <option value="11:30 AM">11:30 AM</option>
              <option value="12:00 PM">12:00 PM</option>
              <option value="12:30 PM">12:30 PM</option>
              <option value="1:00 PM">1:00 PM</option>
              <option value="1:30 PM">1:30 PM</option>
              <option value="2:00 PM">2:00 PM</option>
              <option value="2:30 PM">2:30 PM</option>
              <option value="6:00 PM">6:00 PM</option>
              <option value="6:30 PM">6:30 PM</option>
              <option value="7:00 PM">7:00 PM</option>
              <option value="7:30 PM">7:30 PM</option>
              <option value="8:00 PM">8:00 PM</option>
              <option value="8:30 PM">8:30 PM</option>
              <option value="9:00 PM">9:00 PM</option>
              <option value="9:30 PM">9:30 PM</option>
            </select>
          </div>

          {/* Guests number */}
          <div className="space-y-2">
            <Label htmlFor="guests" className="text-gray-300 flex items-center gap-2">
              <Users className="w-4 h-4 text-purple-400" />
              Number of Guests
            </Label>
            <Input
              type="number"
              id="guests"
              min="1"
              max="20"
              value={formData.guests}
              onChange={(e) =>
                setFormData({ ...formData, guests: parseInt(e.target.value) })
              }
              className="bg-gray-900 border-gray-600 text-white"
              required
            />
          </div>

          {/* Table Select */}
          <div className="space-y-2">
            <Label htmlFor="table" className="text-gray-300">
              Table
            </Label>
            <select
              id="table"
              value={formData.tableId}
              onChange={(e) =>
                setFormData({ ...formData, tableId: parseInt(e.target.value) })
              }
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-blue-400"
              required
            >
              <option value="">Select a table</option>
              {availableTables.map((table) => (
                <option key={table.id} value={table.id}>
                  Table {table.table_number} - {table.location} (Capacity:{" "}
                  {table.capacity})
                </option>
              ))}
            </select>
            {availableTables.length === 0 && (
              <p className="text-sm text-yellow-400">
                No tables available for {formData.guests} guests
              </p>
            )}
          </div>

          {/* Special Requests */}
          <div className="space-y-2">
            <Label htmlFor="specialRequests" className="text-gray-300">
              Special Requests (Optional)
            </Label>
            <textarea
              id="specialRequests"
              value={formData.specialRequests}
              onChange={(e) =>
                setFormData({ ...formData, specialRequests: e.target.value })
              }
              rows={3}
              maxLength={500}
              className="w-full px-4 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 resize-none"
              placeholder="Any special requests or dietary requirements..."
            />
          </div>

          {/* Buttons */}
          <div className="flex gap-3 pt-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              className="flex-1 border-gray-600 text-red-500 hover:bg-red-500 hover:text-white cursor-pointer"
              disabled={updateReservation.isPending}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white cursor-pointer"
              disabled={updateReservation.isPending || availableTables.length === 0}
            >
              {updateReservation.isPending ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Updating...
                </>
              ) : (
                "Update Reservation"
              )}
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  );
};