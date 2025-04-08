from django.shortcuts import render
from rest_framework import viewsets
from .models import User, Account, Transaction
from .serializers import UserSerializer, AccountSerializer, TransactionSerializer

# API viewsets using DRF
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

# Existing HTML views
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
