from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth

from transactions.models import Transaction



def home(request):

    if request.user.is_authenticated:

        transactions = Transaction.objects.filter(
            user=request.user
        )

        income = transactions.filter(
            transaction_type='Income'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        expense = transactions.filter(
            transaction_type='Expense'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        balance = income - expense

        # Monthly expense data
        monthly_data = (
            transactions
            .filter(transaction_type='Expense')
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('amount'))
            .order_by('month')
        )

        months = []
        amounts = []

        for item in monthly_data:
            months.append(item['month'].strftime('%b'))
            amounts.append(float(item['total']))

        recent_transactions = transactions.order_by('-date')[:5]

    else:

        income = 0
        expense = 0
        balance = 0

        months = []
        amounts = []

        recent_transactions = []

    context = {
        'income': income,
        'expense': expense,
        'balance': balance,
        'transactions': recent_transactions,

        'chart_income': float(income),
        'chart_expense': float(expense),

        'months': months,
        'amounts': amounts,
    }

    return render(
        request,
        'dashboard/home.html',
        context
    )


def custom_404(request, exception):
    return render(
        request,
        '404.html',
        status=404
    )