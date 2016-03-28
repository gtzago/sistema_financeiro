from django.conf.urls import url

from . import views

app_name = 'financial'

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create$', views.TransactionCreateView.as_view(), name='create_transaction'),
    url(r'^update/(?P<pk>[0-9]+)/$', views.TransactionUpdateView.as_view(), name='update_transaction'),
    url(r'^delete_transaction/(?P<account_pk>[0-9]+)/(?P<pk>[0-9]+)/$', views.TransactionDeleteView.as_view(), name='delete_transaction'),
    url(r'^delete_account/(?P<pk>[0-9]+)/$', views.AccountDeleteView.as_view(), name='delete_account'),
    #url(r'^account_transactions$', views.AccountTransactionsView.as_view(), name = 'account_transactions'),
    url(r'^(?P<pk>[0-9]+)/$', views.AccountDetailView.as_view(), name='account_transactions'),
]