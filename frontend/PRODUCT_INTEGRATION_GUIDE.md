# Product Integration Guide

This document outlines the changes made to integrate real backend data into product pages.

## ✅ Completed

### 1. Zustand Store Created
- **File**: `frontend/src/Zustand/Product/ProductStates.ts`
- Created separate stores for each product type (Dessert, Doner, Drink, Kebab, Salad)
- Each store has `fetchProducts()` and `fetchProductById()` methods
- Includes loading and error states

### 2. Desserts List Page Updated
- **File**: `frontend/src/Pages/Couisine/Dessert/Desserts.tsx`
- ✅ Fetches real desserts from backend
- ✅ Shows loading spinner while fetching
- ✅ Displays error messages if fetch fails
- ✅ Uses real product data (price, final_price, discount_percentage, image_url, etc.)
- ✅ UI design unchanged

## 🔄 Remaining Updates Needed

### For Each Product List Page:
1. Import `useEffect` and the appropriate store
2. Replace mock data with `fetchProducts()` call
3. Add loading/error states
4. Map backend fields to UI components

### For Each Single Product Page:
1. Import `useEffect`, `useParams` and the appropriate store
2. Fetch product by ID on mount
3. Add loading/error states
4. Map backend fields to UI components

## Backend Field Mapping

### Common Fields (All Products)
```typescript
// Backend → Frontend
id → id
name → name
description → description
price → price (as string, e.g., "12.99")
discount_percentage → discount_percentage (as string)
final_price → final_price (calculated, as string)
image_url → image_url
is_active → is_active
is_front_page → is_front_page (use for "Popular" badge)
tags → tags (array of strings)
created_at → created_at
comments → comments (array of comment IDs)
favourited_product → favourited_product (array of user IDs)
```

### Dessert-Specific Fields
```typescript
is_vegan → is_vegan
is_alergic → is_alergic
dessert_type → dessert_type
calories → calories
```

### Doner-Specific Fields
```typescript
size → size
meat_type → meat_type
spice_level → spice_level
is_vegan → is_vegan
is_alergic → is_alergic
```

### Drink-Specific Fields
```typescript
size → size
is_acidic → is_acidic
```

### Kebab-Specific Fields
```typescript
size → size
meat_type → meat_type
spice_level → spice_level
is_vegan → is_vegan
is_alergic → is_alergic
```

### Salad-Specific Fields
```typescript
is_vegan → is_vegan
is_alergic → is_alergic
calories → calories
```

## API Endpoints

Based on your backend structure, the endpoints should be:
- GET `/products/desserts` - List all desserts
- GET `/products/desserts/{id}` - Get single dessert
- GET `/products/doners` - List all doners
- GET `/products/doners/{id}` - Get single doner
- GET `/products/drinks` - List all drinks
- GET `/products/drinks/{id}` - Get single drink
- GET `/products/kebabs` - List all kebabs
- GET `/products/kebabs/{id}` - Get single kebab
- GET `/products/salads` - List all salads
- GET `/products/salads/{id}` - Get single salad

## Example Pattern for List Pages

```typescript
import { useState, useEffect } from "react";
import { useProductStore } from "@/Zustand/Product/ProductStates";

const Products = () => {
  const { products, isLoading, error, fetchProducts } = useProductStore();
  
  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  // ... rest of component

  // In JSX:
  {isLoading && <LoadingSpinner />}
  {error && <ErrorMessage error={error} />}
  {!isLoading && !error && products.map(product => (
    // ... render product card
  ))}
}
```

## Example Pattern for Single Product Pages

```typescript
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useProductStore } from "@/Zustand/Product/ProductStates";

const Product = () => {
  const { id } = useParams();
  const { currentProduct, isLoading, error, fetchProductById } = useProductStore();
  
  useEffect(() => {
    if (id) {
      fetchProductById(parseInt(id));
    }
  }, [id, fetchProductById]);

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;
  if (!currentProduct) return <NotFound />;

  // ... rest of component with currentProduct data
}
```

## Notes

1. **Price Handling**: Backend returns Decimal as string, so use `parseFloat()` when needed for calculations
2. **Images**: Use fallback placeholder if `image_url` is null
3. **Ratings**: Backend doesn't store ratings, so either:
   - Calculate from comments
   - Use a default value (4.5)
   - Remove rating display
4. **Reviews Count**: Use `comments.length` for review count
5. **Popular Badge**: Use `is_front_page` field to show "Popular" badge
6. **Sale Badge**: Show when `discount_percentage > 0`

## Testing

1. Ensure backend is running
2. Check that `VITE_API_URL` is set correctly in `.env`
3. Test each product page for:
   - Loading state
   - Error handling
   - Data display
   - Navigation between list and detail pages
