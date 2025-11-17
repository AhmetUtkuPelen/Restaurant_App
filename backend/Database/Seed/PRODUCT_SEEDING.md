# Product Seeding Guide

## Overview

This guide explains how to seed your restaurant database with sample products across all categories: Desserts, Doners, Drinks, Kebabs, and Salads.

## Quick Start

### Method 1: Automatic Seeding on Server Startup

Add this to your `.env` file:

```env
SEED_PRODUCTS=true
```

Then start your server:

```bash
uvicorn main:app --reload
```

All products will be automatically seeded when the server starts.

**Note:** After the first run, set `SEED_PRODUCTS=false` or remove it from `.env` to prevent checking on every startup.

### Method 2: Run Individual Seeding Scripts

```bash
# From the backend directory

# Seed all products at once
python -m Database.Seed.SeedAllProducts

# Or seed individual categories
python -m Database.Seed.SeedDessert
python -m Database.Seed.SeedDoner
python -m Database.Seed.SeedDrink
python -m Database.Seed.SeedKebab
python -m Database.Seed.SeedSalad
```

## What Gets Seeded

### 🍰 Desserts (8 items)
- Chocolate Lava Cake - ₺45.00
- Turkish Baklava - ₺35.00 (10% discount)
- Künefe - ₺40.00
- Vanilla Ice Cream - ₺25.00
- Chocolate Brownie - ₺30.00 (15% discount)
- Tiramisu - ₺42.00
- Rice Pudding - ₺22.00
- Vegan Chocolate Cake - ₺38.00 (5% discount)

### 🥙 Doners (8 items)
- Classic Chicken Doner - ₺35.00
- Spicy Beef Doner - ₺42.00 (10% discount)
- Lamb Doner Special - ₺48.00
- Mini Chicken Doner - ₺25.00
- Mixed Meat Doner - ₺40.00 (5% discount)
- Chicken Doner Plate - ₺45.00
- Beef Doner Wrap - ₺38.00
- Family Size Lamb Doner - ₺85.00 (15% discount)

### 🥤 Drinks (12 items)
- Fresh Orange Juice - ₺18.00
- Turkish Tea - ₺8.00
- Turkish Coffee - ₺15.00
- Coca Cola - ₺12.00
- Ayran - ₺10.00
- Fresh Lemonade - ₺16.00 (10% discount)
- Mineral Water - ₺6.00
- Apple Juice - ₺14.00
- Iced Tea - ₺13.00
- Hot Chocolate - ₺20.00
- Energy Drink - ₺22.00 (5% discount)
- Pomegranate Juice - ₺25.00

### 🍖 Kebabs (10 items)
- Adana Kebab - ₺55.00
- Chicken Shish Kebab - ₺45.00 (10% discount)
- Beef Kofte Kebab - ₺48.00
- Mixed Grill Kebab - ₺75.00 (15% discount)
- Lamb Chops - ₺65.00
- Chicken Wings Kebab - ₺38.00 (5% discount)
- Beef Steak Kebab - ₺85.00
- Urfa Kebab - ₺52.00
- Chicken Beyti Kebab - ₺50.00 (8% discount)
- Family Kebab Platter - ₺120.00 (20% discount)

### 🥗 Salads (12 items)
- Mediterranean Salad - ₺32.00
- Caesar Salad - ₺28.00 (10% discount)
- Turkish Shepherd Salad - ₺22.00
- Grilled Chicken Salad - ₺42.00
- Quinoa Power Salad - ₺38.00 (5% discount)
- Arugula Salad - ₺26.00
- Tuna Salad - ₺45.00
- Caprese Salad - ₺35.00
- Spinach and Strawberry Salad - ₺33.00 (8% discount)
- Vegan Buddha Bowl - ₺40.00
- Kale and Apple Salad - ₺30.00
- Protein Power Salad - ₺48.00 (12% discount)

## Product Features

Each product includes:

✅ **Realistic Pricing** - Turkish Lira (TRY) pricing
✅ **Discounts** - Some products have promotional discounts
✅ **Categories** - Proper categorization (dessert, doner, drink, kebab, salad)
✅ **Tags** - Searchable tags for filtering
✅ **Images** - High-quality Unsplash images
✅ **Descriptions** - Detailed product descriptions
✅ **Dietary Info** - Vegan and allergen information
✅ **Nutritional Data** - Calorie information where applicable
✅ **Sizes** - Different sizes for applicable products
✅ **Spice Levels** - For kebabs and doners
✅ **Front Page** - Featured products for homepage

## Testing the Seeded Products

### 1. Browse Products

```bash
# Get all desserts
GET /api/desserts/

# Get all doners
GET /api/doners/

# Get all drinks
GET /api/drinks/

# Get all kebabs
GET /api/kebabs/

# Get all salads
GET /api/salads/
```

### 2. Add to Cart and Order

```bash
# Add a dessert to cart
POST /api/cart/items
{
  "product_id": 1,
  "quantity": 2
}

# Create order from cart
POST /api/orders/
{
  "delivery_address": "Test Address"
}
```

### 3. Leave Comments

```bash
# Comment on a product
POST /api/comments/
{
  "product_id": 1,
  "content": "Delicious dessert!",
  "rating": 5
}
```

## Customizing Products

To customize the seeded products, edit the respective files:

- `SeedDessert.py` - Modify dessert data
- `SeedDoner.py` - Modify doner data
- `SeedDrink.py` - Modify drink data
- `SeedKebab.py` - Modify kebab data
- `SeedSalad.py` - Modify salad data

### Example Customization

```python
# In SeedDessert.py, modify the desserts_data list:
{
    "name": "Your Custom Dessert",
    "description": "Your description",
    "price": Decimal('50.00'),
    "discount_percentage": Decimal('10.00'),
    "image_url": "https://your-image-url.com",
    "is_vegan": True,
    "dessert_type": DessertType.CAKE,
    "calories": 300
}
```

## Environment Variables

Add these to your `.env` file for automatic seeding:

```env
# Seed products on server startup
SEED_PRODUCTS=true

# Also seed admin users (optional)
SEED_ADMIN=true
```

## Seeding Output

When seeding completes, you'll see output like:

```
================================================================================
🎉 PRODUCT SEEDING COMPLETED!
================================================================================
📊 SUMMARY:
   ✅ Total Products Created: 50
   ⏭️  Total Products Skipped: 0
   📦 Total Products Processed: 50

📋 BREAKDOWN BY CATEGORY:
   🍰 Desserts: 8 created, 0 skipped
   🥙 Doners: 8 created, 0 skipped
   🥤 Drinks: 12 created, 0 skipped
   🍖 Kebabs: 10 created, 0 skipped
   🥗 Salads: 12 created, 0 skipped
================================================================================

🚀 Your restaurant is now ready with a full menu!
```

## Troubleshooting

### Issue: "Product already exists" messages
**Solution:** This is normal. The script skips existing products to prevent duplicates.

### Issue: Import errors
**Solution:** Make sure you're running from the backend directory and all dependencies are installed.

### Issue: Database connection errors
**Solution:** Check your `.env` file has the correct `DATABASE_URL` configured.

### Issue: Enum errors
**Solution:** Ensure all enum values in the seeding data match those defined in `Utils/Enums/Enums.py`.

## Database Schema

The seeded products use these database tables:

- `products` - Base product information (polymorphic table)
- `desserts` - Dessert-specific fields
- `doners` - Doner-specific fields
- `drinks` - Drink-specific fields
- `kebabs` - Kebab-specific fields
- `salads` - Salad-specific fields

## Next Steps

After seeding products:

1. ✅ Browse products via API endpoints
2. ✅ Test cart functionality
3. ✅ Create test orders
4. ✅ Test payment system
5. ✅ Leave product reviews
6. ✅ Test admin product management
7. ✅ Customize products for your restaurant
8. ✅ Add your own product images
9. ✅ Adjust pricing for your market
10. ✅ Configure product availability

## Support

If you encounter issues with product seeding:

1. Check the console output for specific error messages
2. Verify your database connection
3. Ensure all required dependencies are installed
4. Check that enum values match your `Enums.py` file
5. Review the seeding script logs for detailed information

Your restaurant API is now fully stocked and ready for business! 🍽️