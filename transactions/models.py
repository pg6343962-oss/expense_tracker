
from django.db import models
from django.contrib.auth.models import User


class Transaction(models.Model):

    TYPE = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )

    CATEGORY = (
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Bills', 'Bills'),
        ('Health', 'Health'),
        ('Salary', 'Salary'),
        ('Other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TYPE)
    category = models.CharField(max_length=20, choices=CATEGORY)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title