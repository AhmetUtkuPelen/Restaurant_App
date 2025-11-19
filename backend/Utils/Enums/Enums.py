from enum import Enum



class MeatType(Enum):
    CHICKEN = "chicken"
    BEEF = "beef"
    LAMB = "lamb"



class SpiceLevel(Enum):
    MILD = "mild"
    MEDIUM = "medium"
    HOT = "hot"



class DonerSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"



class KebabSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"



class DrinkSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"



class DessertType(Enum):
    CAKE = "cake"
    PASTRY = "pastry"
    ICE_CREAM = "ice_cream"
    PUDDING = "pudding"
    BAKLAVA = "baklava"
    KUNEFE = "kunefe"
    BROWNIE = "brownie"
    TIRAMISU = "tiramisu"



class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    STAFF = "staff"



class OrderStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"



class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    REFUND_PENDING = "refund_pending"



class ReservationStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"



class TableLocation(Enum):
    WINDOW = "window"
    PATIO = "patio"
    MAIN_DINING_ROOM = "main_dining_room"