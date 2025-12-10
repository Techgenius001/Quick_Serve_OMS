from django.core.management.base import BaseCommand
from orders.models import MenuCategory


class Command(BaseCommand):
    help = 'Fix category issues by removing Popular/New categories and ensuring standard ones exist'

    def handle(self, *args, **options):
        self.stdout.write("Fixing categories...")
        
        # Delete Popular and New categories
        deleted_count, _ = MenuCategory.objects.filter(name__in=['Popular', 'New']).delete()
        self.stdout.write(f"✓ Deleted {deleted_count} invalid categories (Popular/New)")
        
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
                self.stdout.write(f"✓ Created category: {cat_name}")
        
        if created_count == 0:
            self.stdout.write("✓ All standard categories already exist")
        
        # Show final categories
        all_categories = MenuCategory.objects.all()
        self.stdout.write(f"\nFinal categories ({all_categories.count()}):")
        for cat in all_categories:
            self.stdout.write(f"  - {cat.name}")
        
        self.stdout.write(self.style.SUCCESS("\n✅ Categories fixed successfully!"))