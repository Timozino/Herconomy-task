from django.urls import path
from .views import TransactionList, FilteredTransactionList

app_name='transaction_monitoring_app'


urlpatterns = [
    path('', TransactionList.as_view(), name='transaction-list'),
    path('filtered-transactions/', FilteredTransactionList.as_view(), name='filtered-transaction-list'),
]



