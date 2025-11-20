import { useState } from "react";
import { Link } from "react-router-dom";
import { Card, CardContent } from "@/Components/ui/card";
import { Button } from "@/Components/ui/button";
import { Badge } from "@/Components/ui/badge";
import {
  Calendar,
  Clock,
  Users,
  MapPin,
  AlertCircle,
  CheckCircle,
  XCircle,
  Trash2,
  ArrowLeft,
  Edit,
} from "lucide-react";
import {
  useMyReservations,
  useCancelReservation,
  type Reservation,
} from "@/hooks/useReservation";
import { UpdateReservationDialog } from "@/Components/Reservation/UpdateReservationDialog";
import { toast } from "sonner";

const UserReservations = () => {
  const { data: reservations = [], isLoading, error } = useMyReservations();
  const cancelReservation = useCancelReservation();
  const [cancellingId, setCancellingId] = useState<number | null>(null);
  const [editingReservation, setEditingReservation] = useState<Reservation | null>(null);

  const handleCancelReservation = async (reservationId: number) => {
    toast.warning("Are you sure?", {
      description: "",
      action: {
        label: "Yes, Cancel Reservation",
        onClick: async () => {
          setCancellingId(reservationId);
          try {
            await cancelReservation.mutateAsync(reservationId);
            toast.success("Reservation cancelled successfully", {
              description: `Reservation #${reservationId} has been cancelled.`,
            });
          } catch (error) {
            toast.error("Failed to cancel reservation. Please try again.");
            console.error("Failed to cancel reservation:", error);
          } finally {
            setCancellingId(null);
          }
        },
      },
      cancel: {
        label: "Keep Reservation",
        onClick: () => {
          toast.info("Reservation cancellation cancelled");
        },
      },
    });
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case "confirmed":
        return "bg-green-100 text-green-800";
      case "pending":
        return "bg-yellow-100 text-yellow-800";
      case "cancelled":
        return "bg-red-100 text-red-800";
      case "completed":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case "confirmed":
        return <CheckCircle className="h-4 w-4" />;
      case "pending":
        return <AlertCircle className="h-4 w-4" />;
      case "cancelled":
        return <XCircle className="h-4 w-4" />;
      default:
        return <CheckCircle className="h-4 w-4" />;
    }
  };

  const formatDateTime = (dateTimeString: string) => {
    try {
      const date = new Date(dateTimeString);
      return {
        date: date.toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
        }),
        time: date.toLocaleTimeString("en-US", {
          hour: "numeric",
          minute: "2-digit",
          hour12: true,
        }),
      };
    } catch {
      return { date: "Invalid date", time: "" };
    }
  };

  const isUpcoming = (dateTimeString: string) => {
    try {
      return new Date(dateTimeString) > new Date();
    } catch {
      return false;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-400"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <Card className="bg-gray-800 border-gray-700 max-w-md">
          <CardContent className="p-8 text-center">
            <AlertCircle className="h-12 w-12 text-red-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">
              Error Loading Reservations
            </h3>
            <p className="text-gray-400 mb-4">
              {error instanceof Error
                ? error.message
                : "Failed to load reservations"}
            </p>
            <Button
              onClick={() => window.location.reload()}
              className="bg-blue-600 hover:bg-blue-700"
            >
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">

        <div className="mb-8">
          <Link
            to="/"
            className="inline-flex items-center gap-2 text-gray-400 hover:text-blue-400 mb-4 transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            Back to Home
          </Link>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white flex items-center">
                <Calendar className="h-8 w-8 mr-3 text-blue-400" />
                My Reservations
              </h1>
              <p className="text-gray-400 mt-2">
                View and manage your restaurant reservations
              </p>
            </div>
            <Link to="/reservation">
              <Button className="bg-blue-600 hover:bg-blue-700 text-white cursor-pointer">
                <Calendar className="h-4 w-4 mr-2" />
                New Reservation
              </Button>
            </Link>
          </div>
        </div>

        {reservations.length === 0 ? (
          <Card className="bg-gray-800 border-gray-700">
            <CardContent className="p-12 text-center">
              <Calendar className="h-16 w-16 text-gray-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">
                No Reservations Yet
              </h3>
              <p className="text-gray-400 mb-6">
                You haven't made any reservations. Book a table to get started!
              </p>
              <Link to="/reservations">
                <Button className="bg-blue-600 hover:bg-blue-700 text-white">
                  Make a Reservation
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {reservations.map((reservation) => {
              const { date, time } = formatDateTime(
                reservation.reservation_time
              );
              const upcoming = isUpcoming(reservation.reservation_time);
              const canCancel =
                upcoming &&
                reservation.status.toLowerCase() !== "cancelled" &&
                reservation.status.toLowerCase() !== "completed";

              return (
                <Card
                  key={reservation.id}
                  className="bg-gray-800 border-gray-700 hover:border-gray-600 transition-colors"
                >
                  <CardContent className="p-6">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-4">
                          <Badge
                            className={`${getStatusColor(
                              reservation.status
                            )} flex items-center gap-1`}
                          >
                            {getStatusIcon(reservation.status)}
                            {reservation.status}
                          </Badge>
                          {upcoming && (
                            <Badge className="bg-blue-600 text-white">
                              Upcoming
                            </Badge>
                          )}
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                          <div className="flex items-center gap-2 text-gray-300">
                            <Calendar className="h-5 w-5 text-blue-400" />
                            <div>
                              <p className="text-xs text-gray-500">Date</p>
                              <p className="font-medium">{date}</p>
                            </div>
                          </div>

                          <div className="flex items-center gap-2 text-gray-300">
                            <Clock className="h-5 w-5 text-green-400" />
                            <div>
                              <p className="text-xs text-gray-500">Time</p>
                              <p className="font-medium">{time}</p>
                            </div>
                          </div>

                          <div className="flex items-center gap-2 text-gray-300">
                            <Users className="h-5 w-5 text-purple-400" />
                            <div>
                              <p className="text-xs text-gray-500">Guests</p>
                              <p className="font-medium">
                                {reservation.number_of_guests}{" "}
                                {reservation.number_of_guests === 1
                                  ? "Guest"
                                  : "Guests"}
                              </p>
                            </div>
                          </div>

                          <div className="flex items-center gap-2 text-gray-300">
                            <MapPin className="h-5 w-5 text-orange-400" />
                            <div>
                              <p className="text-xs text-gray-500">Table</p>
                              <p className="font-medium">
                                Table #{reservation.table_id}
                              </p>
                            </div>
                          </div>
                        </div>

                        {reservation.special_requests && (
                          <div className="bg-gray-700/50 rounded-lg p-3 mb-4">
                            <p className="text-xs text-gray-400 mb-1">
                              Special Requests:
                            </p>
                            <p className="text-sm text-gray-300">
                              {reservation.special_requests}
                            </p>
                          </div>
                        )}

                        <div className="flex items-center gap-4 text-xs text-gray-500">
                          <span>Reservation ID: #{reservation.id}</span>
                          <span>
                            Created:{" "}
                            {new Date(
                              reservation.created_at
                            ).toLocaleDateString("en-US", {
                              year: "numeric",
                              month: "short",
                              day: "numeric",
                            })}
                          </span>
                        </div>
                      </div>

                      {canCancel && (
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setEditingReservation(reservation)}
                            className="border-blue-600 text-blue-400 hover:bg-blue-900/20 hover:text-blue-300 cursor-pointer"
                          >
                            <Edit className="h-4 w-4 mr-2" />
                            Update
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() =>
                              handleCancelReservation(reservation.id)
                            }
                            disabled={cancellingId === reservation.id}
                            className="border-red-600 text-red-400 hover:bg-red-900/20 hover:text-red-300 cursor-pointer"
                          >
                            {cancellingId === reservation.id ? (
                              <>
                                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-400 mr-2"></div>
                                Cancelling...
                              </>
                            ) : (
                              <>
                                <Trash2 className="h-4 w-4 mr-2" />
                                Cancel
                              </>
                            )}
                          </Button>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}

        {/* Update Reservation */}
        {editingReservation && (
          <UpdateReservationDialog
            reservation={editingReservation}
            open={!!editingReservation}
            onOpenChange={(open) => !open && setEditingReservation(null)}
          />
        )}
      </div>
    </div>
  );
};

export default UserReservations;