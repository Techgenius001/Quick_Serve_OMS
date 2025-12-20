"""
Test script to verify Cloudinary URL generation
Run this in Django shell: python manage.py shell < test_cloudinary_urls.py
"""

import os
os.environ['RENDER'] = 'true'  # Simulate production

# Import after setting env var
from orders.models import MenuItem
from orders.templatetags.cloudinary_tags import smart_image_url

print("=" * 60)
print("CLOUDINARY URL GENERATION TEST")
print("=" * 60)

# Get a sample menu item with an image
menu_items = MenuItem.objects.filter(image__isnull=False)[:3]

if not menu_items:
    print("\n⚠️  No menu items with images found in database")
    print("Please add at least one menu item with an image first.")
else:
    print(f"\nFound {len(menu_items)} menu item(s) with images\n")
    
    for item in menu_items:
        print(f"Menu Item: {item.name}")
        print(f"  Image field name: {item.image.name}")
        
        # Test the smart_image_url filter
        url = smart_image_url(item.image)
        print(f"  Generated URL: {url}")
        
        # Verify URL structure
        if 'res.cloudinary.com' in url and '/image/upload/' in url:
            print("  ✅ CORRECT - URL includes /image/upload/")
        elif 'res.cloudinary.com' in url:
            print("  ❌ ERROR - Missing /image/upload/ in URL")
        else:
            print("  ⚠️  WARNING - Not a Cloudinary URL (might be local dev)")
        
        print()

print("=" * 60)
print("Test complete!")
print("=" * 60)
