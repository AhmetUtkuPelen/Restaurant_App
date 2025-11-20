export interface CreateOrderRequest {
  delivery_address?: string;
  special_instructions?: string;
}

export interface OrderResponse {
  message: string;
  order: {
    id: number;
    user_id: number;
    total_amount: number;
    status: "pending" | "completed" | "cancelled";
    delivery_address?: string;
    special_instructions?: string;
    created_at: string;
    updated_at?: string;
    completed_at?: string;
    order_items: Array<{
      id: number;
      order_id: number;
      product_id: number;
      quantity: number;
      unit_price: number;
      subtotal: number;
      created_at: string;
    }>;
  };
}