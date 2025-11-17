# Remaining Product Page Updates

## ✅ Completed
1. Desserts.tsx - List page ✓
2. Dessert.tsx - Single page ✓
3. Doners.tsx - List page ✓

## 🔄 Pattern for Remaining Pages

### For List Pages (Drinks.tsx, Kebabs.tsx, Salads.tsx)

1. Add imports:
```typescript
import { useState, useEffect } from "react";
import { use[Product]Store } from "@/Zustand/Product/ProductStates";
```

2. Replace mock data with store:
```typescript
const { products, isLoading, error, fetchProducts } = use[Product]Store();

useEffect(() => {
  fetchProducts();
}, [fetchProducts]);
```

3. Add loading/error states before grid:
```typescript
{isLoading && <LoadingSpinner />}
{error && <ErrorMessage />}
{!isLoading && !error && products.length > 0 && (
  <div className="grid...">
    {/* products */}
  </div>
)}
```

4. Update product mapping:
```typescript
const hasDiscount = parseFloat(product.discount_percentage) > 0;
const finalPrice = parseFloat(product.final_price);
// Use product.image_url, product.is_front_page, etc.
```

### For Single Pages (Doner.tsx, Drink.tsx, Kebab.tsx, Salad.tsx)

1. Add imports:
```typescript
import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { use[Product]Store } from "@/Zustand/Product/ProductStates";
```

2. Fetch product by ID:
```typescript
const { id } = useParams();
const { currentProduct, isLoading, error, fetchProductById } = use[Product]Store();

useEffect(() => {
  if (id) {
    fetchProductById(parseInt(id));
  }
}, [id, fetchProductById]);
```

3. Add loading/error/not found states:
```typescript
if (isLoading) return <LoadingSpinner />;
if (error || !currentProduct) return <NotFound />;
```

4. Use real product data:
```typescript
const hasDiscount = parseFloat(currentProduct.discount_percentage) > 0;
const finalPrice = parseFloat(currentProduct.final_price);
// Map all fields from backend
```

## Quick Reference: Product-Specific Fields

### Doner
- size, meat_type, spice_level, is_vegan, is_alergic

### Drink  
- size, is_acidic

### Kebab
- size, meat_type, spice_level, is_vegan, is_alergic

### Salad
- is_vegan, is_alergic, calories

## Notes
- All prices are strings from backend, use `parseFloat()` for calculations
- Use `product.image_url` with fallback placeholder
- Use `product.is_front_page` for "Popular" badge
- Use `product.comments.length` for review count
- Default rating to 4.5 (backend doesn't store ratings)
