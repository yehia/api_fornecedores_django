from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin,)

class UserManager(BaseUserManager):

    def create_user(self, username, email, nome, password=None):

        if username is None:
            raise TypeError('Usuário deve possuir um nome de usuário.')
        if nome is None:
            raise TypeError('Usuário deve possuir um nome.')
        if email is None:
            raise TypeError('Usuário deve possuir um e-mail.')

        user = self.model(username=username, email=self.normalize_email(email), nome=nome)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, nome, email, password=None):

        if password is None:
            raise TypeError('A senha não pode ser nula.')
    
        user = self.create_user(username, nome, email, password)
        user.is_superuser = True
        user.is_staff=True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True, db_index=True, error_messages={'unique':"Usuário já cadastrado."})
    email = models.EmailField(max_length=255, unique=True, db_index=True, error_messages={'unique':"Email já cadastrado."})
    nome = models.CharField(max_length=255, null=False, blank=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'nome']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh_token' : str(refresh),
            'access_token' : str(refresh.access_token)
        }