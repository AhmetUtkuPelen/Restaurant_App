# Iyzico Payment Integration Setup

## Environment Variables

Add these variables to your `.env` file:

```env
# Iyzico Payment Gateway Configuration
IYZICO_API_KEY=your_api_key_here
IYZICO_SECRET_KEY=your_secret_key_here
IYZICO_BASE_URL=https://sandbox-api.iyzipay.com

# For production, use:
# IYZICO_BASE_URL=https://api.iyzipay.com
```

## Getting Iyzico Test Credentials

### 1. Sign Up for Iyzico Sandbox Account

1. Go to [Iyzico Sandbox](https://sandbox-merchant.iyzipay.com/)
2. Create a free sandbox account
3. Verify your email
4. Login to the merchant panel

### 2. Get Your API Credentials

1. Navigate to **Settings** → **API Credentials**
2. Copy your:
   - **API Key** (starts with `sandbox-`)
   - **Secret Key** (long alphanumeric string)
3. Add them to your `.env` file

## Test Cards for Iyzico

Use these test cards in the sandbox environment:

### Successful Payment Cards

#### Visa
- **Card Number:** `5528790000000008`
- **Expiry:** Any future date (e.g., `12/2030`)
- **CVV:** `123`
- **Cardholder Name:** Any name

#### Mastercard
- **Card Number:** `5400010000000004`
- **Expiry:** Any future date
- **CVV:** `123`
- **Cardholder Name:** Any name

### Failed Payment Cards (for testing error scenarios)

#### Insufficient Funds
- **Card Number:** `5406670000000009`
- **Expiry:** Any future date
- **CVV:** `123`

#### Do Not Honor
- **Card Number:** `4543590000000006`
- **Expiry:** Any future date
- **CVV:** `123`

## Payment Flow

### Current Implementation (Test Mode)

1. **User creates payment:**
   ```bash
   POST /api/payments/
   {
     "order_ids": [1, 2],
     "amount": 100.00,
     "currency": "TRY",
     "installment": 1,
     "ip_address": "127.0.0.1"
   }
   ```

2. **Payment record is created** with status `PENDING`

3. **User simulates completion (TEST MODE):**
   ```bash
   POST /api/payments/{payment_id}/complete-test
   ```

4. **System updates:**
   - Payment status → `COMPLETED`
   - Related orders → `COMPLETED`
   - Related reservations → `CONFIRMED`

### Production Implementation (TODO)

For production, you need to integrate the actual Iyzico API:

1. **Install Iyzico Python SDK:**
   ```bash
   pip install iyzipay
   ```

2. **Update PaymentControllers.create_payment():**
   ```python
   import iyzipay
   
   # Initialize Iyzico client
   options = {
       'api_key': os.getenv('IYZICO_API_KEY'),
       'secret_key': os.getenv('IYZICO_SECRET_KEY'),
       'base_url': os.getenv('IYZICO_BASE_URL')
   }
   
   # Create payment request
   payment_request = {
       'locale': 'tr',
       'conversationId': payment.conversation_id,
       'price': str(payment.amount),
       'paidPrice': str(payment.amount),
       'currency': payment.currency,
       'installment': payment.installment,
       'basketId': payment.basket_id,
       'paymentChannel': 'WEB',
       'paymentGroup': 'PRODUCT',
       # ... more fields
   }
   
   # Call Iyzico API
   payment_result = iyzipay.Payment().create(payment_request, options)
   ```

3. **Implement callback endpoint:**
   ```python
   @PaymentRouter.post("/callback/iyzico")
   async def iyzico_callback(request: Request, db: AsyncSession = Depends(get_db)):
       # Handle Iyzico callback
       # Verify payment status
       # Update payment record
       # Update orders/reservations
       pass
   ```

## Testing the Payment System

### 1. Create an Order

```bash
# Add items to cart
POST /api/cart/items
{
  "product_id": 1,
  "quantity": 2
}

# Create order from cart
POST /api/orders/
{
  "delivery_address": "Test Address",
  "special_instructions": "Test order"
}
```

### 2. Create Payment for Order

```bash
POST /api/payments/
{
  "order_ids": [1],
  "amount": 50.00,
  "currency": "TRY",
  "installment": 1,
  "ip_address": "127.0.0.1",
  "metadata": {
    "note": "Test payment"
  }
}
```

### 3. Complete Payment (Test Mode)

```bash
POST /api/payments/1/complete-test
```

### 4. Verify Payment

```bash
# Check payment status
GET /api/payments/my-payments/1

# Check order status (should be completed)
GET /api/orders/my-orders/1
```

## Payment for Reservations

```bash
# Create reservation
POST /api/reservations/
{
  "table_id": 1,
  "reservation_time": "2024-12-25T19:00:00",
  "number_of_guests": 4
}

# Pay for reservation
POST /api/payments/
{
  "reservation_id": 1,
  "amount": 50.00,
  "currency": "TRY",
  "installment": 1,
  "ip_address": "127.0.0.1"
}

# Complete payment
POST /api/payments/1/complete-test
```

## Security Notes

⚠️ **IMPORTANT:**

1. **Never commit API keys** to version control
2. **Use environment variables** for all sensitive data
3. **Validate payment amounts** server-side (already implemented)
4. **Verify Iyzico callbacks** using signature verification
5. **Use HTTPS** in production
6. **Log all payment transactions** for audit trail
7. **Implement idempotency** to prevent duplicate payments
8. **Set up monitoring** for failed payments

## Admin Endpoints

Admins can:
- View all payments: `GET /api/payments/admin/all`
- View payment details: `GET /api/payments/admin/{payment_id}`
- Update payment status: `PUT /api/payments/admin/{payment_id}`
- View statistics: `GET /api/payments/admin/statistics`
- View user payments: `GET /api/payments/admin/user/{user_id}`

## Troubleshooting

### Issue: "Amount mismatch" error
**Solution:** Ensure the payment amount matches the total of orders/reservation fee

### Issue: "Order is not pending" error
**Solution:** Can only pay for orders with PENDING status

### Issue: "Reservation is not pending" error
**Solution:** Can only pay for reservations with PENDING status

### Issue: Payment created but not completing
**Solution:** Use the `/complete-test` endpoint in test mode

## Next Steps for Production

1. ✅ Install Iyzico SDK: `pip install iyzipay`
2. ✅ Get production API credentials from Iyzico
3. ✅ Implement actual Iyzico API integration
4. ✅ Set up callback endpoint for payment notifications
5. ✅ Implement 3D Secure authentication
6. ✅ Add payment retry logic
7. ✅ Set up payment monitoring and alerts
8. ✅ Implement refund functionality
9. ✅ Add payment receipt generation
10. ✅ Test with real cards in production environment

## Support

- Iyzico Documentation: https://dev.iyzipay.com/
- Iyzico Support: destek@iyzico.com
- Sandbox Merchant Panel: https://sandbox-merchant.iyzipay.com/
