
from django.db import models
#from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_new_user = models.BooleanField(default=False)
    is_flagged= models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name', 'last_name']

    def __str__(self):
        return self.username


class Transaction(models.Model):
    user = models.ForeignKey('transaction_monitoring_app.User', on_delete=models.CASCADE)
    amount = models.FloatField(default=0)
    email = models.EmailField(default="")
    tier = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction ID: {self.pk}, Amount: {self.amount}"

class UserProfile(models.Model):
    user = models.OneToOneField('transaction_monitoring_app.User', on_delete=models.CASCADE)
    is_new_user = models.BooleanField(default=True)
    is_flagged = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.username}"

