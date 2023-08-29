
from django.contrib import admin
from .models import Transaction, UserProfile, User

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'email', 'tier', 'timestamp']
    list_filter = ['user', 'tier', 'timestamp']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_new_user', 'is_flagged']
    list_filter = ['is_new_user', 'is_flagged']


