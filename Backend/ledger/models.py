from django.db import models
from decimal import Decimal

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return self.name
class Account(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    authorized_users = models.ManyToManyField(User, related_name='authorized_accounts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add this line

    def __str__(self):
        return self.name

    def change_balance(self, amount: Decimal):
        """Update the balance of the account."""
        self.balance += amount
        self.save()

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    description = models.TextField()

    def __str__(self):
        return f"{self.timestamp} - {self.amount} - {self.account.name} - {self.description}"