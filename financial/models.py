# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.db import transaction as dj_transaction
from django.db.models import Q
from django.utils import timezone


# Create your models here.
# Create your models here.
class Account(models.Model):
    name = models.CharField("nome da conta", max_length=50)
    description = models.CharField(max_length=200)
    bank = 'BK'
    expense = 'EX'
    income = 'IN'
    acc_type_choices = (
        (bank, 'Banco'),
        (expense, 'Despesa'),
        (income, 'Recurso'),
    )
    acc_type = models.CharField(
        "tipo", max_length=2, choices=acc_type_choices, default=expense)
    balance = models.DecimalField("saldo", max_digits=15, decimal_places=2)

    # cria uma propriedade para as instâncias de account, é o saldo total.
    @property
    def balancee(self):
        # lista todas as transacoes envolvendo a referida conta.
        transactions = Transaction.objects.filter(
            Q(acc_from=self) | Q(acc_to=self)).order_by("date")
        balancee = 0  # variavel que armazenara o saldo
        for transaction in transactions:
            # se transação for de crédito, aumenta o saldo.
            if transaction.is_credit(self):
                balancee += transaction.value
            else:
                # diminui o saldo caso contrário.
                balancee -= transaction.value
        return balancee

    # cria uma propriedade para acompanhar a evolução do saldo para cada
    # transação.
    @property
    def transactions(self):
        # lista todas as transações envolvendo a referida conta.
        transactions = Transaction.objects.filter(
            Q(acc_from=self) | Q(acc_to=self)).order_by("date")
        for transaction in transactions:
            transaction.balance = 0
            for transaction_parent in transactions:
                if transaction_parent.is_credit(self):
                    transaction.balance += transaction_parent.value
                else:
                    transaction.balance -= transaction_parent.value
                if transaction_parent.pk == transaction.pk:
                    break

        # retorna as transações com uma nova propriedade chamada balance que
        # contém o saldo na conta no momento da transação.
        return transactions

    def __str__(self):
        return self.name


class Transaction(models.Model):
    date = models.DateField("data")
    description = models.CharField("descrição", max_length=200)
    acc_from = models.ForeignKey(
        Account, on_delete=models.PROTECT, verbose_name="conta debitada", related_name='taken')
    acc_to = models.ForeignKey(
        Account, on_delete=models.PROTECT, verbose_name="conta creditada", related_name='added')
    value = models.DecimalField("valor", max_digits=15, decimal_places=2,  validators=[
                                validators.MinValueValidator(0.0)])

    def is_credit(self, account):
        return self.acc_to == account

    @dj_transaction.atomic
    def save(self, *args, **kwargs):
        super(Transaction, self).save(*args, **kwargs)
        self.acc_from.balance -= self.value
        self.acc_from.save()

        self.acc_to.balance += self.value
        self.acc_to.save()

    def __str__(self):
        return self.description

    def clean(self):
        '''
        Testa antes de salvar o modelo no banco.
        Somente neste metodo se pode utilizar validação entre campos diferentes.
        '''
        try:
            if self.acc_to == self.acc_from:
                raise ValidationError(
                    u'Não se pode transferir de uma conta para ela mesma.')
        except:
            pass
