from django import forms
from django.forms import ModelForm

from .models import Transaction


class TransactionForm(ModelForm):

    debit = forms.CharField()  # cria um novo campo no formulario

    # modifica o metodo save.
    # def save(self):

    class Meta:
        model = Transaction
        fields = ['date', 'description', 'acc_to', 'value']
