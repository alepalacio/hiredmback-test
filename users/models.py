from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    #Modelo de User extendido y modificado, por eso usamos AbstractBaseUser.
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #Esto define que estamos usando el modelo de manager creado UserManager para definir que tipo de usuario estamos creando
    objects = UserManager()

    #Por default en el modelo User, el campo username es requerido, pero como nosotros no tenemos ese campo en nuestro modelo, configuramos que el username va a ser nuestro campo email, ya eso lo convierte en un campo requerido
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def tokens(self):
        return ""

#Tenemos que settear en settings.py AUTH_USER_MODEL = "<nombreapp>.<nombredemodelousuario>"  para que reconozca qué tipo de usuario va a usar.