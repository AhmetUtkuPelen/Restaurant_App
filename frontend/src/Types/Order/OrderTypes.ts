// --- Enums ---
type OrderStatus =
  | "PENDING"
  | "CONFIRMED"
  | "PREPARING"
  | "READY"
  | "DELIVERED"
  | "CANCELLED"
  | "COMPLETED";

// --- Order Item Types ---
interface OrderItemBase {
  /** Product ID */
  product_id: number;
  /** Quantity ordered */
  quantity: number;
  /** Price per unit at time of order */
  unit_price: string; // Decimal as string
  /** Total price for this item (quantity * unit_price) */
  subtotal: string; // Decimal as string
}

interface OrderItemCreate {
  /** Product ID */
  product_id: number;
  /** Quantity to order */
  quantity: number;
  // unit_price and subtotal will be calculated from product
}

interface OrderItemRead extends OrderItemBase {
  /** Unique order item identifier */
  id: number;
  /** Order ID this item belongs to */
  order_id: number;
  /** Creation timestamp */
  created_at: string;
}

// --- Order Types ---
interface OrderBase {
  /** Delivery address (optional) */
  delivery_address?: string | null;
  /** Special instructions for the order */
  special_instructions?: string | null;
}

interface OrderCreate extends OrderBase {
  /** Order items (if None, will use cart items) */
  items?: OrderItemCreate[] | null;
}

interface OrderUpdate {
  /** Order status */
  status?: OrderStatus;
  /** Delivery address */
  delivery_address?: string | null;
  /** Special instructions */
  special_instructions?: string | null;
}

interface OrderRead extends OrderBase {
  /** Unique order identifier */
  id: number;
  /** User ID who placed the order */
  user_id: number;
  /** Current order status */
  status: OrderStatus;
  /** Total amount for the order */
  total_amount: string; // Decimal as string
  /** Creation timestamp */
  created_at: string;
  /** Last update timestamp */
  updated_at?: string | null;
  /** Completion timestamp */
  completed_at?: string | null;
  /** List of order items */
  order_items: OrderItemRead[];
}

type OrderInDB = OrderRead;

// --- Extended Response with Relations ---
interface OrderItemWithProduct extends OrderItemRead {
  /** Product information at time of order */
  product?: {
    id: number;
    name: string;
    image_url?: string | null;
    category: string;
  };
}

interface OrderWithProducts extends Omit<OrderRead, "order_items"> {
  /** Order items with product details */
  order_items: OrderItemWithProduct[];
}

interface OrderWithUser extends OrderRead {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
}

interface OrderWithRelations extends Omit<OrderRead, "order_items"> {
  /** User information */
  user?: {
    id: number;
    username: string;
    email: string;
    phone?: string | null;
  };
  /** Order items with product details */
  order_items: OrderItemWithProduct[];
  /** Payment information */
  payments?: Array<{
    id: number;
    amount: string;
    status: string;
    created_at: string;
  }>;
}

// --- Order Operations ---
interface CreateOrderFromCart {
  /** Delivery address (optional) */
  delivery_address?: string | null;
  /** Special instructions */
  special_instructions?: string | null;
}

interface OrderSummary {
  /** Total number of orders */
  total_orders: number;
  /** Total amount of all orders */
  total_amount: string; // Decimal as string
  /** Orders by status */
  orders_by_status: Record<OrderStatus, number>;
  /** Recent orders */
  recent_orders: OrderRead[];
}

// --- Admin Operations ---
interface OrderStatusUpdate {
  /** New status for the order */
  status: OrderStatus;
  /** Optional note about the status change */
  note?: string;
}

interface OrderFilters {
  /** Filter by status */
  status?: OrderStatus;
  /** Filter by user ID */
  user_id?: number;
  /** Filter by date range (start) */
  date_from?: string;
  /** Filter by date range (end) */
  date_to?: string;
  /** Filter by minimum amount */
  min_amount?: number;
  /** Filter by maximum amount */
  max_amount?: number;
}

// Export all interfaces
export type {
  OrderStatus,
  OrderItemBase,
  OrderItemCreate,
  OrderItemRead,
  OrderBase,
  OrderCreate,
  OrderUpdate,
  OrderRead,
  OrderInDB,
  OrderItemWithProduct,
  OrderWithProducts,
  OrderWithUser,
  OrderWithRelations,
  CreateOrderFromCart,
  OrderSummary,
  OrderStatusUpdate,
  OrderFilters,
};
