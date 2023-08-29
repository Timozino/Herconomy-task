

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Transaction

User = get_user_model() 

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        exclude=['id']

