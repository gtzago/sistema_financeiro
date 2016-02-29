# Create your views here.
from django.core.urlresolvers import reverse
from django.db import transaction as dj_transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import FormView

from financial.forms import TransactionForm
from financial.models import Transaction

from .models import Account


class IndexView(generic.ListView):
    template_name = 'financial/index.html'
    context_object_name = 'accounts_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Account.objects.all()


class TransactionCreateView(generic.CreateView):

    '''
        Esta classe eh utilizada para criar entradas na base de dados.
    '''
    model = Transaction
    template_name = 'financial/create_transaction.html'
    fields = ['date', 'description', 'acc_from', 'acc_to', 'value']
    success_url = 'create'


class TransactionUpdateView(generic.UpdateView):

    '''
        Esta classe eh utilizada para criar entradas na base de dados.
    '''
    model = Transaction
    template_name = 'financial/update_transaction.html'
    fields = ['date', 'description', 'acc_from', 'acc_to', 'value']
    #success_url = '/financial'

    def get_success_url(self):
        return reverse('account_transactions')

    def get_object(self, queryset=None):
        obj = Transaction.objects.get(id=self.kwargs['pk'])
        return obj


class TransactionDeleteView(generic.DeleteView):

    '''
        Esta classe eh utilizada para criar entradas na base de dados.
    '''
    model = Transaction
    #template_name = 'financial/update_transaction.html'
    #fields = ['date', 'description','acc_from', 'acc_to', 'value']
    #success_url = '/financial'

    def get_success_url(self):
        # retorna para a url com o parametro pk (id da conta)
        return reverse('financial:account_transactions', args=(self.kwargs.get('account_pk')))
        # return reverse('financial:account_transactions',
        # args=self.kwargs.get('pk'))

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    # def get_object(self, queryset=None):
    #    obj = Transaction.objects.get(id=self.kwargs['pk'])
    #    return obj


class AccountDetailView(generic.CreateView):

    '''
        Esta classe eh utilizada para criar entradas na base de dados.
    '''
    model = Transaction
    form_class = TransactionForm  # formulario que esta sendo usado, descrito em outro arquivo (forms.py).
    template_name = 'financial/account_transactions.html'
    # fields = ['date', 'description', 'acc_to', 'value'] # sao os campos
    # utilizados no formulario. Caso eu nao apontasse qual form utilziar.
    success_url = 'create'

    def get_context_data(self, **kwargs):
        '''
            Adiciona parametros extras no template.
        '''
        context = super(AccountDetailView, self).get_context_data(**kwargs)
        # adiciona uma variavel chamada pk dentro de kwargs de acordo com o
        # parametro passado na url ('pk').
        context['object'] = Account.objects.get(pk=self.kwargs.get('pk'))

        return context

    def get_success_url(self):
        # retorna para a url com o parametro pk (id da conta)
        return reverse('financial:account_transactions', args=self.kwargs.get('pk'))
