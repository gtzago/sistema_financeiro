from django import forms
from django.forms import ModelForm

from .models import Transaction, Account


class TransactionForm(ModelForm):

    debit = forms.DecimalField(required=False)  # cria um novo campo no formulario
    credit = forms.DecimalField(required=False)

    def is_valid(self):
        return True

    class Meta:
        model = Transaction
        fields = ['date', 'description', 'acc_to']

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'