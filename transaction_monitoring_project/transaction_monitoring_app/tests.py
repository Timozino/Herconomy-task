from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from .models import Transaction
from .serializers import TransactionSerializer
from django.urls import reverse
from django.core import mail
from django.test import override_settings


User = get_user_model() 

class TransactionListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_create_transaction_valid(self):
        user = User.objects.create(email="test@example.com")
        data = {
            "user": user.id,
            "amount": 1000.0,
            "email": user.email,
            "tier": "tier_1"
        }
        response = self.client.post(reverse('transaction_monitoring_app:transaction-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)

    def test_create_transaction_policy_violation(self):
        user = User.objects.create(email="test@example.com")
        Transaction.objects.create(user=user, amount=6000000, email=user.email, tier="tier_3")

        data = {
            "user": user.id,
            "amount": 6000001.0,  # Violates Policy 1
            "email": user.email,
            "tier": "tier_3"
        }
        response = self.client.post(reverse('transaction_monitoring_app:transaction-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # It's still created despite the violation
        self.assertEqual(Transaction.objects.count(), 2)

        # Check if the email alert was sent
        self.assertEqual(len(response.wsgi_request.outbox), 1)
        self.assertIn("Policy 1: Transaction amount exceeded 5,000,000.", response.wsgi_request.outbox[0].body)

    def test_create_transaction_multiple_transactions(self):
        user = User.objects.create(email="test@example.com")
        Transaction.objects.create(user=user, amount=1000, email=user.email, tier="tier_1")

        # Create a second transaction within 1 minute (violates Policy 2)
        data = {
            "user": user.id,
            "amount": 2000.0,
            "email": user.email,
            "tier": "tier_1"
        }
        response = self.client.post(reverse('transaction_monitoring_app:transaction-list'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 2)

        # Check if the email alert was sent
        self.assertEqual(len(response.wsgi_request.outbox), 1)
        self.assertIn("Policy 2: Multiple transactions occurred within 1 minute.", response.wsgi_request.outbox[0].body)

    

    def test_get_transaction_list(self):
        user = User.objects.create(email="test@example.com")
        Transaction.objects.create(user=user, amount=1000, email=user.email, tier="tier_1")
        Transaction.objects.create(user=user, amount=2000, email=user.email, tier="tier_2")

        response = self.client.get(reverse('transaction_monitoring_app:transaction-list'))  
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)



