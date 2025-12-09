#!/usr/bin/env python
"""
Script to fix category issues in production.
This script:
1. Deletes 'Popular' and 'New' categories (they should only be tags)
2. Creates standard categories if they don't exist
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartkibadaski.settings')
django.setup()

from orders.models import MenuCategory

def fix_categories():
    print("Fixing categories...")
    
    # Delete Popular and New categories
    deleted_count, _ = MenuCategory.objects.filter(name__in=['Popular', 'New']).delete()
    print(f"✓ Deleted {deleted_count} invalid categories (Popular/New)")
    
    # Ensure standard categories exist
    standard_categories = [
        'Breakfast',
        'Lunch',
        'Snack',
        'Beverage',
    ]
    
    created_count = 0
    for cat_name in standard_categories:
        category, created = MenuCategory.objects.get_or_create(name=cat_name)
        if created:
            created_count += 1
            print(f"✓ Created category: {cat_name}")
    
    if created_count == 0:
        print("✓ All standard categories already exist")
    
    # Show final categories
    all_categories = MenuCategory.objects.all()
    print(f"\nFinal categories ({all_categories.count()}):")
    for cat in all_categories:
        print(f"  - {cat.name}")
    
    print("\n✅ Categories fixed successfully!")

if __name__ == '__main__':
    fix_categories()
