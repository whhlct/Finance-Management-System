from django.http import HttpResponse
from django.shortcuts import render

from .models import Transaction

# Create your views here.
def index(request):
    transactions = Transaction.objects.all()
    context = {
        "transactions": transactions,
        "transaction_count": transactions.count()
    }

    return render(request, "ledger/index.html", context)