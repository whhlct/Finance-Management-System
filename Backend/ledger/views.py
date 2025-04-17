from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import User, Account, Transaction
from .serializers import UserSerializer, AccountSerializer, TransactionSerializer
from decimal import Decimal
from django.http import JsonResponse
from django.utils.timezone import now


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

def change_balance(request, account_id, amount):
    """View to change the balance of an account."""
    try:
        account = get_object_or_404(Account, id=account_id)
        amount = Decimal(amount)
        account.change_balance(amount)  # Calls the model method to update balance
        return JsonResponse({"status": "success", "new_balance": str(account.balance)})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


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
def create_transaction(request, account_id, amount, description):
    """Create a transaction and update the account balance."""
    try:
        account = get_object_or_404(Account, id=account_id)
        amount = Decimal(amount)

        # Record the transaction
        transaction = Transaction(
            account=account,
            amount=amount,
            description=description,
            creator=request.user,  # Assuming the request user is the creator
            timestamp=datetime.now()
        )
        transaction.save()

        # Change the account balance
        account.change_balance(amount)

        return JsonResponse({
            "status": "success",
            "transaction_id": transaction.id,
            "new_balance": str(account.balance)
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def get_transaction_history(request, account_id):
    """Retrieve all transactions for an account."""
    account = get_object_or_404(Account, id=account_id)
    transactions = Transaction.objects.filter(account=account).order_by('-timestamp')

    transaction_list = [
        {
            "amount": str(tx.amount),
            "timestamp": tx.timestamp,
            "description": tx.description,
            "creator": tx.creator.name,
        }
        for tx in transactions
    ]

    return JsonResponse({"transactions": transaction_list})
def update_balance(request, account_id, new_balance):
    """Update the balance of an account."""
    try:
        account = get_object_or_404(Account, id=account_id)
        account.balance = Decimal(new_balance)
        account.save()
        return JsonResponse({"status": "success", "new_balance": str(account.balance)})

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})