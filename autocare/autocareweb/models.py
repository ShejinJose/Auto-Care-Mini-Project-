from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    ADMIN = 'admin', _('Admin')
    SERVICE_MANAGER = 'service_manager', _('Service Manager')
    MECHANIC = 'mechanic', _('Mechanic')
    CUSTOMER = 'customer', _('Customer')

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class UserDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='details')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.name
