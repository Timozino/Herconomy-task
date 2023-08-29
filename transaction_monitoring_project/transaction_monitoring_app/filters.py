
import django_filters
from .models import Transaction, UserProfile
from django.contrib.auth import get_user_model


User = get_user_model() 

class TransactionFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")
    user = django_filters.CharFilter(field_name="user__username", lookup_expr="exact")
    tier = django_filters.CharFilter(field_name="tier", lookup_expr="exact")

    class Meta:
        model = Transaction
        fields = []

class UserProfileFilter(django_filters.FilterSet):
    is_new_user = django_filters.BooleanFilter(field_name="is_new_user", lookup_expr="exact")
    is_flagged = django_filters.BooleanFilter(field_name="is_flagged", lookup_expr="exact")

    class Meta:
        model = UserProfile
        fields = []


