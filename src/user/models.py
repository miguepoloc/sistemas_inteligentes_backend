"""
Models for core app.
"""

from random import randint

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords

from core.models import BaseModel


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create, save and return a superuser."""
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    document = models.CharField(max_length=50, blank=True)
    code_phone = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=50, blank=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.CharField(max_length=250, blank=True)
    historical = HistoricalRecords()
    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        """Return string representation of user."""
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        """Override the save method to generate username from email."""
        if not self.username:
            # Generate username from email
            username = slugify(self.email.split('@')[0])
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                # Append a random number to the username
                username = f"{username}-{randint(1000, 9999)}"
            self.username = username
        super().save(*args, **kwargs)
