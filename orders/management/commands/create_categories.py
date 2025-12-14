from django.core.management.base import BaseCommand
from orders.models import MenuCategory


class Command(BaseCommand):
    help = 'Create default menu categories'

    def handle(self, *args, **options):
        categories = [
            'Breakfast',
            'Lunch', 
            'Snack',
            'Beverage',
        ]

        created_count = 0
        for category_name in categories:
            category, created = MenuCategory.objects.get_or_create(
                name=category_name
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category_name}')
                )
                created_count += 1
            else:
                self.stdout.write(f'Category already exists: {category_name}')

        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {created_count} categories')
            )
        else:
            self.stdout.write('All categories already exist')