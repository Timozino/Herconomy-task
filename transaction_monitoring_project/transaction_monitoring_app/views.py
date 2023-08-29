from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Transaction, UserProfile
from .serializers import TransactionSerializer
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .filters import TransactionFilter
from rest_framework import generics


User = get_user_model() 

class TransactionList(APIView):
    """
    API endpoint for managing transactions.

    GET: Retrieve a list of all transactions.
    
    POST: Create a new transaction.
    """
    def get(self, request):
        """
        Retrieve a list of all transactions.

        Returns:
            - 200 OK: List of transactions.
        """
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new transaction.

        Parameters:
            - user (int): User ID for the transaction.
            - amount (float): Transaction amount.
            - email (str): Email for sending notifications.
            - tier (str): Tier for the transaction amount.

        Returns:
            - 201 Created: Successfully created transaction.
            - 400 Bad Request: Invalid data provided.
        """
        serializer = TransactionSerializer(data=request.data)
        
            
        if serializer.is_valid():
            email = request.data.get('email')  # Retrieve user_id from the request data
            user = User.objects.get(email=email) if email else None
            serializer.save(user=user) 

            # Check policies and trigger email
            transaction = serializer.instance
            recipient_list = [request.data.get('email')]

            violations = []

            # Policy checks go here
            tier_amounts = {
                'tier_1': 5000,
                'tier_2': 500000,
                'tier_3': 5000000
            }

            # Policy 1: The transaction amount is greater than 5,000,000.
            if transaction.amount > 5000000:
                violations.append("Policy 1: Transaction amount exceeded 5,000,000.")

            # Policy 2: Transaction from a particular user occurs within a timing window of less than 1 minute.
            one_minute_ago = datetime.now() - timedelta(minutes=1)
            if Transaction.objects.filter(user=transaction.user, timestamp__gte=one_minute_ago).count() > 1:
                violations.append("Policy 2: Multiple transactions occurred within 1 minute.")

            # Policy 3: Transaction is attributed to a new user.
            if transaction.user.is_new_user:
                violations.append("Policy 3: Transaction attributed to a new user.")

            # Policy 4: Transaction is happening between a regular user and previously flagged user.
            if transaction.user.is_flagged:
                violations.append("Policy 4: Transaction between regular and flagged users.")

            # Policy 5: Transaction amount exceeds the amount for a given tier.
            if transaction.amount > tier_amounts.get(transaction.tier):
                violations.append(f"Policy 5: Transaction amount exceeded Tier {transaction.tier}.")

            if violations:
                subject = "Transaction Alert"
                message = "The following policies were violated:\n\n"
                message += "\n".join(violations)
                from_email = "support@herconomy.com"
                recipient_list = [request.data.get('email')]
                send_mail(subject, message, from_email, recipient_list)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FilteredTransactionList(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
