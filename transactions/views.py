from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Sum
from django.http import HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
import csv

from .models import Transaction
from .forms import TransactionForm


def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            messages.success(
                request,
                "Transaction added successfully!"
            )

            return redirect('home')

    else:
        form = TransactionForm()

    return render(
        request,
        'transactions/add_transaction.html',
        {'form': form}
    )


def transaction_list(request):

    search = request.GET.get('search')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')

    # Search
    if search:
        transactions = transactions.filter(
            Q(title__icontains=search) |
            Q(category__icontains=search) |
            Q(transaction_type__icontains=search)
        )

    # Date filter
    if start_date:
        transactions = transactions.filter(
            date__gte=start_date
        )

    if end_date:
        transactions = transactions.filter(
            date__lte=end_date
        )

    # Summary
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

    # Pagination
    paginator = Paginator(transactions, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search': search,
        'start_date': start_date,
        'end_date': end_date,
        'income': income,
        'expense': expense,
        'balance': balance,
    }

    return render(
        request,
        'transactions/list.html',
        context
    )


def edit_transaction(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            instance=transaction
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Transaction updated successfully!"
            )

            return redirect('transaction_list')

    else:
        form = TransactionForm(
            instance=transaction
        )

    return render(
        request,
        'transactions/edit.html',
        {'form': form}
    )


def delete_transaction(request, pk):

    transaction = get_object_or_404(
        Transaction,
        pk=pk,
        user=request.user
    )

    transaction.delete()

    messages.success(
        request,
        "Transaction deleted successfully!"
    )

    return redirect('transaction_list')


def export_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response['Content-Disposition'] = (
        'attachment; filename="transactions.csv"'
    )

    writer = csv.writer(response)

    writer.writerow([
        'Title',
        'Category',
        'Type',
        'Amount',
        'Date',
        'Description'
    ])

    transactions = Transaction.objects.filter(
        user=request.user
    )

    for transaction in transactions:

        writer.writerow([
            transaction.title,
            transaction.category,
            transaction.transaction_type,
            transaction.amount,
            transaction.date,
            transaction.description
        ])

    return response