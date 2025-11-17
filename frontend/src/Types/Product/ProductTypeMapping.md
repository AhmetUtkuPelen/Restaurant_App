# Product Type Mapping Documentation

This document maps backend product models and schemas to frontend TypeScript interfaces.

## Product Inheritance Structure

Your backend uses **Single Table Inheritance (STI)** where all products share the `products` table with a `category` column to differentiate types.

```
Product (Base)
├── Dessert
├── Doner
├── Drink
├── Kebab
└── Salad
```

## Base Product

**Backend**: 
- Model: `backend/Models/PRODUCT/BaseProduct/BaseProductModel.py`
- Schema: `backend/Schemas/PRODUCT/BaseProduct/BaseProductSchemas.py`

**Frontend**: `frontend/src/Types/Product/BaseProduct/BaseProductTypes.ts`

| Backend Schema | Frontend Interface | Purpose |
|---|---|---|
| `ProductBase` | `ProductBase` | Base product data |
| `ProductBaseCreate` | `ProductBaseCreate` | Create product |
| `ProductBaseUpdate` | `ProductBaseUpdate` | Update product |
| `ProductBaseRead` | `ProductBaseRead` | Read product data |
| `ProductBaseInDb` | `ProductBaseInDb` | DB product data |

### Key Fields:
- `name`: Unique product name
- `description`: Product description
- `category`: Product type (dessert, doner, drink, kebab, salad)
- `tags`: JSON array of tags
- `price`: Decimal (stored as string in frontend)
- `discount_percentage`: 0-100 (Decimal as string)
- `final_price`: Calculated property (price after discount)
- `image_url`: Product image
- `is_active`: Soft delete flag
- `is_front_page`: Display on landing page

## Dessert

**Backend**:
- Model: `backend/Models/PRODUCT/Dessert/DessertModel.py`
- Schema: `backend/Schemas/PRODUCT/Dessert/DessertSchemas.py`

**Frontend**: `frontend/src/Types/Product/Dessert/DessertTypes.ts`

### Additional Fields:
- `is_vegan`: Boolean
- `is_alergic`: Boolean
- `dessert_type`: Enum (CAKE, PIE, PUDDING, ICE_CREAM, PASTRY, COOKIE, OTHER)
- `calories`: Integer

### Properties:
- `alergen_warning`: Warning message for allergens
- `vegan_warning`: Vegan status message

## Doner

**Backend**:
- Model: `backend/Models/PRODUCT/Doner/DonerModel.py`
- Schema: `backend/Schemas/PRODUCT/Doner/DonerSchemas.py`

**Frontend**: `frontend/src/Types/Product/Doner/DonerTypes.ts`

### Additional Fields:
- `size`: Enum (SMALL, MEDIUM, LARGE, EXTRA_LARGE)
- `meat_type`: Enum (CHICKEN, BEEF, LAMB, MIXED, VEGETARIAN)
- `spice_level`: Enum (MILD, MEDIUM, HOT, EXTRA_HOT)
- `is_vegan`: Boolean
- `is_alergic`: Boolean

### Properties:
- `summary`: Readable summary
- `description_summary`: Description text

## Drink

**Backend**:
- Model: `backend/Models/PRODUCT/Drink/DrinkModel.py`
- Schema: `backend/Schemas/PRODUCT/Drink/DrinkSchemas.py`

**Frontend**: `frontend/src/Types/Product/Drink/DrinkTypes.ts`

### Additional Fields:
- `size`: Enum (SMALL, MEDIUM, LARGE, EXTRA_LARGE)
- `is_acidic`: Boolean

## Kebab

**Backend**:
- Model: `backend/Models/PRODUCT/Kebab/KebabModel.py`
- Schema: `backend/Schemas/PRODUCT/Kebab/KebabSchemas.py`

**Frontend**: `frontend/src/Types/Product/Kebab/KebabTypes.ts`

### Additional Fields:
- `size`: Enum (SMALL, MEDIUM, LARGE, EXTRA_LARGE)
- `meat_type`: Enum (CHICKEN, BEEF, LAMB, MIXED, VEGETARIAN)
- `spice_level`: Enum (MILD, MEDIUM, HOT, EXTRA_HOT)
- `is_vegan`: Boolean
- `is_alergic`: Boolean

### Properties:
- `summary`: Readable summary
- `description_summary`: Description text

## Salad

**Backend**:
- Model: `backend/Models/PRODUCT/Salad/SaladModel.py`
- Schema: `backend/Schemas/PRODUCT/Salad/SaladSchemas.py`

**Frontend**: `frontend/src/Types/Product/Salad/SaladTypes.ts`

### Additional Fields:
- `is_vegan`: Boolean
- `is_alergic`: Boolean
- `calories`: Integer (default: 0)

## Favourite Product

**Backend**:
- Model: `backend/Models/PRODUCT/FavouriteProduct/FavouriteProductModel.py`
- Schema: `backend/Schemas/PRODUCT/FavouriteProduct/FavouriteProductSchemas.py`

**Frontend**: `frontend/src/Types/Product/FavProduct/FavProductTypes.ts`

### Fields:
- `user_id`: User who favorited
- `product_id`: Product that was favorited
- `created_at`: When favorited
- Unique constraint on (user_id, product_id)

## Key Differences

### Decimal Handling
- **Backend**: Uses `Decimal` type for precise monetary calculations
- **Frontend**: Uses `string` representation to avoid JavaScript floating-point issues

### Enum Values
- **Backend**: Uses Python Enum classes (e.g., `DessertType.CAKE`)
- **Frontend**: Uses TypeScript union types (e.g., `'CAKE' | 'PIE' | ...`)

### DateTime Handling
- **Backend**: Uses `datetime` objects
- **Frontend**: Uses ISO string format (`string`)

### Polymorphism
- **Backend**: Uses SQLAlchemy's polymorphic inheritance
- **Frontend**: Uses separate interfaces that extend the base product type

## Usage Examples

### Creating a Product

```typescript
// Dessert
const dessert: DessertCreate = {
  name: "Chocolate Cake",
  description: "Rich chocolate cake",
  category: "dessert",
  tags: ["chocolate", "sweet"],
  price: "15.99",
  discount_percentage: "10.00",
  image_url: "/images/chocolate-cake.jpg",
  is_active: true,
  is_front_page: true,
  is_vegan: false,
  is_alergic: true,
  dessert_type: "CAKE",
  calories: 350
};

// Doner
const doner: DonerCreate = {
  name: "Chicken Doner",
  description: "Grilled chicken doner",
  category: "doner",
  tags: ["chicken", "grilled"],
  price: "12.99",
  discount_percentage: "0.00",
  image_url: "/images/chicken-doner.jpg",
  is_active: true,
  is_front_page: false,
  size: "MEDIUM",
  meat_type: "CHICKEN",
  spice_level: "MEDIUM",
  is_vegan: false,
  is_alergic: false
};
```

### Adding to Favorites

```typescript
const favorite: FavouriteProductCreate = {
  product_id: 123
  // user_id comes from authenticated user
};
```

### Product Summary for Lists

```typescript
const summary: ProductSummary = {
  id: 1,
  name: "Chocolate Cake",
  category: "dessert",
  price: "15.99",
  final_price: "14.39", // After 10% discount
  discount_percentage: "10.00",
  image_url: "/images/chocolate-cake.jpg",
  is_active: true,
  tags: ["chocolate", "sweet"]
};
```

## Import Usage

```typescript
// Import specific types
import type { DessertCreate, DessertRead } from '@/Types/Product/Dessert/DessertTypes';

// Or import from index
import type { DessertCreate, DonerRead, ProductSummary } from '@/Types/Product';
```

## Relationships

Products have relationships with:
- **Users**: Through favorites (`favourite_products`)
- **Comments**: User reviews and ratings
- **Cart Items**: Products in user carts
- **Order Items**: Products in orders

These relationships are represented as:
- **IDs only** in base responses (e.g., `favourited_product: number[]`)
- **Full objects** in extended responses (e.g., `ProductWithRelations`)
