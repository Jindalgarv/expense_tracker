"""
Management command to seed default categories.
Run with: python manage.py seed_categories
"""
from django.core.management.base import BaseCommand
from tracker.models import Category


class Command(BaseCommand):
    help = 'Seed default expense categories'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Food & Drinks', 'icon': '🍕', 'color': '#ff6b6b'},
            {'name': 'Transportation', 'icon': '🚗', 'color': '#feca57'},
            {'name': 'Groceries', 'icon': '🛒', 'color': '#00d2d3'},
            {'name': 'Entertainment', 'icon': '🎬', 'color': '#5f27cd'},
            {'name': 'Rent', 'icon': '🏠', 'color': '#54a0ff'},
            {'name': 'Utilities', 'icon': '💡', 'color': '#ff9f43'},
            {'name': 'Shopping', 'icon': '🛍️', 'color': '#ee5a24'},
            {'name': 'Travel', 'icon': '✈️', 'color': '#0abde3'},
            {'name': 'Health', 'icon': '🏥', 'color': '#1dd1a1'},
            {'name': 'Education', 'icon': '📚', 'color': '#6c5ce7'},
            {'name': 'Other', 'icon': '📦', 'color': '#6c757d'},
        ]
        created_count = 0
        for cat_data in categories:
            _, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon'], 'color': cat_data['color']}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Seeded {created_count} categories (total: {Category.objects.count()})'))
