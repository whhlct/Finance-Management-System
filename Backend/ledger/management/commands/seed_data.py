from django.core.management.base import BaseCommand
from ledger.models import User, Account
from datetime import datetime

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        # Create a test user
        user, created = User.objects.get_or_create(
            name="Test User",
            email="test@example.com"
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created test user'))
        
        # Create some accounts
        accounts = [
            "Checking Account",
            "Savings Account",
            "Credit Card",
            "Investment Account"
        ]
        
        for account_name in accounts:
            account, created = Account.objects.get_or_create(
                name=account_name,
                owner=user
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created account: {account_name}'))
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database')) 