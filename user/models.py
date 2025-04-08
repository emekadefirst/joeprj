from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AppUserManager(BaseUserManager):
    def create_user(self, id, email, username, role, password=None):
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            id=id,
            email=self.normalize_email(email),
            role=role,
            username=username,
        )
        user.set_password(password)  
        user.save()
        return user


    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            id=None,
            email=email,
            username=username,
            role="ADMIN",
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class ROLE(models.TextChoices):
        USER = "USER", "User"
        ADMIN = "ADMIN", "Admin"

    role = models.CharField(max_length=20, choices=ROLE.choices, null=True, default=ROLE.USER)
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AppUserManager()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.email