from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .models import Item
from .serializers import ItemSerializer
from .models import Transaction, Account

# Create your views here.
def index(request):
    transactions = Transaction.objects.all()
    context = {
        "transactions": transactions,
        "transaction_count": transactions.count()
    }

    return render(request, "ledger/index.html", context)

def accounts(request):
    accounts = Account.objects.all()
    context = {
        "accounts": accounts,
        "account_count": accounts.count()
    }

    return render(request, "ledger/accounts.html", context)