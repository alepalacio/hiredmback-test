from django.contrib.auth.models import BaseUserManager

# Para crear un usuario usamos BaseUserManager porque es un modelo de usuario extendido/modificado (AbstractBaseUser)
class UserManager(BaseUserManager):
    #Crear un usuario nuevo. **other_fields hace referencia a los otros campos
    def create_user(self, email, password=None, **other_fields):
        #Si el usuario no provee un email, mandamos un error.
        if not email:
            raise ValueError('You must provide an email address')
        
        #Utilizamos normalize_email para igualar a minúsculas todos los dominios ingresados
        email = self.normalize_email(email)
        #De acuerdo con nuestro modelo, asignamos lo que ingrese el usuario a la variable. En este caso email.
        user = self.model(email=email, **other_fields)
        #Configuramos el password con lo que ingresó el usuario
        user.set_password(password)
        user.save()
        #Guardamos y retornamos al usuario
        return user

    #Para crear un super usuario
    def create_superuser(self, email, password, **other_fields):
        #Definimos como True los campos que en el modelo inicialmente estaban como False, ya que son los que brindaran facultades al superuser.  No se modifica is_active porque ya es True, como lo indica el modelo.
        user = self.create_user(email, password=password, **other_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
        