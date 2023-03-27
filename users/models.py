from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, AbstractUser
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None, is_mod=False):
        if not email:
            raise ValueError('email gotta be provided to create account here')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.is_active = True
        user.is_mod = is_mod

        user.save(using=self.db)

        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email=email, username=username, password=password)

        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True, verbose_name='Email Address')
    username = models.CharField(max_length=30, unique=True)
    date_join = models.DateTimeField(auto_now_add=True, verbose_name='Date joined')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Last login')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_mod = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    def __str__(self):
        return self.username
