# Backend to Frontend Type Mapping

This document shows the mapping between backend Pydantic schemas and frontend TypeScript interfaces.

## User Types
**Backend**: `backend/Models/USER/UserModel.py` + `backend/Schemas/USER/UserSchemas.py`
**Frontend**: `frontend/src/Types/User/UserTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `UserLogin` | `UserLogin` | Login credentials |
| `UserRegister` | `UserRegister` | Registration data |
| `UserUpdate` | `UserUpdate` | User profile updates |
| `UserProfileUpdate` | `UserProfileUpdate` | Profile-specific updates |
| `AdminCreateUser` | `AdminCreateUser` | Admin user creation |
| `AdminUpdateUser` | `AdminUpdateUser` | Admin user updates |
| `UserInDbBase` | `UserInDbBase` | Base user data from DB |
| `User` | `User` | Public user data |
| `UserInDb` | `UserInDb` | Internal user data with password |
| `UserProfileRead` | `UserProfileRead` | Profile view data |

## Reservation Types
**Backend**: `backend/Models/RESERVATION/ReservationModel.py` + `backend/Schemas/RESERVATION/ReservationSchemas.py`
**Frontend**: `frontend/src/Types/Reservation/ReservationTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `ReservationBase` | `ReservationBase` | Base reservation data |
| `ReservationCreate` | `ReservationCreate` | Create reservation |
| `ReservationUpdate` | `ReservationUpdate` | Update reservation |
| `ReservationRead` | `ReservationRead` | Read reservation data |
| `ReservationInDB` | `ReservationInDB` | DB reservation data |

## Table Types
**Backend**: `backend/Models/RESERVATION/TableModel.py` + `backend/Schemas/RESERVATION/TableSchemas.py`
**Frontend**: `frontend/src/Types/Reservation/TableTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `TableBase` | `TableBase` | Base table data |
| `TableCreate` | `TableCreate` | Create table |
| `TableUpdate` | `TableUpdate` | Update table |
| `TableRead` | `TableRead` | Read table data |
| `TableInDB` | `TableInDB` | DB table data |

## Cart Types
**Backend**: `backend/Models/CART/CartModel.py` + `backend/Schemas/CART/CartSchemas.py`
**Frontend**: `frontend/src/Types/Cart/CartTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `CartItemBase` | `CartItemBase` | Base cart item data |
| `CartItemCreate` | `CartItemCreate` | Add item to cart |
| `CartItemUpdate` | `CartItemUpdate` | Update cart item |
| `CartItemRead` | `CartItemRead` | Read cart item data |
| `CartBase` | `CartBase` | Base cart data |
| `CartCreate` | `CartCreate` | Create cart |
| `CartRead` | `CartRead` | Read cart data |
| `CartInDB` | `CartInDB` | DB cart data |

## Comment Types
**Backend**: `backend/Models/COMMENT/CommentModel.py` + `backend/Schemas/COMMENT/CommentSchemas.py`
**Frontend**: `frontend/src/Types/Comment/CommentTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `CommentBase` | `CommentBase` | Base comment data |
| `CommentCreate` | `CommentCreate` | Create comment |
| `CommentUpdate` | `CommentUpdate` | Update comment |
| `CommentRead` | `CommentRead` | Read comment data |
| `CommentInDB` | `CommentInDB` | DB comment data |

## Order Types
**Backend**: `backend/Models/ORDER/OrderModel.py` + `backend/Models/ORDER/OrderItemModel.py` + `backend/Schemas/ORDER/OrderSchemas.py`
**Frontend**: `frontend/src/Types/Order/OrderTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `OrderItemBase` | `OrderItemBase` | Base order item data |
| `OrderItemCreate` | `OrderItemCreate` | Create order item |
| `OrderItemRead` | `OrderItemRead` | Read order item data |
| `OrderBase` | `OrderBase` | Base order data |
| `OrderCreate` | `OrderCreate` | Create order |
| `OrderUpdate` | `OrderUpdate` | Update order |
| `OrderRead` | `OrderRead` | Read order data |
| `OrderInDB` | `OrderInDB` | DB order data |

## Payment Types
**Backend**: `backend/Models/PAYMENT/PaymentModel.py` + `backend/Schemas/PAYMENT/PaymentSchemas.py`
**Frontend**: `frontend/src/Types/Payment/PaymentTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `CardInfo` | `CardInfo` | Card information |
| `PaymentCreate` | `PaymentCreate` | Create payment |
| `PaymentUpdate` | `PaymentUpdate` | Update payment |
| `PaymentRead` | `PaymentRead` | Read payment data |
| `PaymentInDB` | `PaymentInDB` | DB payment data |

## Key Differences

### Decimal Handling
- **Backend**: Uses `Decimal` type for precise monetary calculations
- **Frontend**: Uses `string` representation to avoid JavaScript floating-point issues

### Enum Values
- **Backend**: Uses Python Enum classes (e.g., `UserRole.ADMIN`)
- **Frontend**: Uses TypeScript union types (e.g., `'ADMIN' | 'USER' | 'STAFF'`)

### DateTime Handling
- **Backend**: Uses `datetime` objects
- **Frontend**: Uses ISO string format (`string`)

### Optional Fields
- **Backend**: Uses `Optional[Type]` or `Type | None`
- **Frontend**: Uses `Type | null` or `Type | undefined`

### Relationships
- **Backend**: Uses SQLAlchemy relationships
- **Frontend**: Uses separate interfaces for extended data with relations

## Extended Frontend Types

The frontend includes additional interfaces not present in the backend:

### With Relations Interfaces
- `ReservationWithRelations` - Reservation with user and table data
- `CartWithProducts` - Cart with full product details
- `CommentWithUser` - Comment with user information
- `OrderWithProducts` - Order with product details
- `PaymentWithUser` - Payment with user information

### Operation Interfaces
- `AddToCartRequest` - Specific cart operations
- `OrderFilters` - Admin filtering options
- `PaymentRequest` - Payment processing
- `RefundRequest` - Refund operations

### Statistics Interfaces
- `CommentStats` - Comment analytics
- `OrderSummary` - Order statistics
- `PaymentStats` - Payment analytics

These extended types provide better developer experience and type safety for complex frontend operations.