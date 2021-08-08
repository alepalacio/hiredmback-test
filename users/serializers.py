from django.conf import settings
from django.contrib.auth import authenticate, get_user, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from users.models import User
#from rest_auth import serializers

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email',)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id","email", "password",)
        extra_kwargs = {"password": {"write_only": True}}
        
    # Reescribimos la función create y update que vienen por defecto en ModelSerializer
    # Utilizando el ORM para crear el usuario
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        print(instance)
        instance.email = validated_data.get("email", instance.email)
        instance.is_verified = validated_data.get("is_verified", instance.is_verified)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.is_staff = validated_data.get("is_staff", instance.is_staff)
        password = instance.password
        instance.set_password(password)
        instance.save()
        return instance
    
    UserModel = get_user_model()
    
# Personalizando el serializador de login, ya que por default trabaja con username
class LoginSerializer(serializers.Serializer):
    
    # Quitamos el campo 'username' para trabajar solo con email y password.
    email = serializers.EmailField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def _validate_username_email(self, username, email, password):
        user = None

        if email and password:
            user = self.authenticate(email=email, password=password)
        elif username and password:
            user = self.authenticate(username=username, password=password)
        else:
            msg = _('Must include either "username" or "email" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        
        email = attrs.get('email')
        password = attrs.get('password')

        user = None

        # Authentication without using allauth
        if email:
            try:
                username = User.objects.get(email__iexact=email).get_username()
            except User.DoesNotExist:
                pass

        if username:
            user = self._validate_username_email(username, '', password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)
        
        attrs['user'] = user
        return attrs
        
        
        




















# class UserRegistrationSerializer(RegistrationSerializer):
#     class Meta:
#         model = User

#         # You must include the 'email' field for the serializer to work.
#         fields = (
#             #User.USERNAME_FIELD,
#             "email",
#             "password",
#         )
#         extra_kwargs = {"password": {"write_only": True}}


# # Get the UserModel
# UserModel = get_user_model()


# class LoginSerializer(serializers.Serializer):
#     # username = serializers.CharField(required=False, allow_blank=True)
#     email = serializers.EmailField(required=True, allow_blank=False)
#     password = serializers.CharField(style={"input_type": "password"})

#     def authenticate(self, **kwargs):
#         return authenticate(self.context["request"], **kwargs)

#     def _validate_email(self, email, password):
#         user = None

#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         else:
#             msg = _('Must include "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def _validate_username_email(self, username, email, password):
#         user = None

#         if email and password:
#             user = self.authenticate(email=email, password=password)
#         elif username and password:
#             user = self.authenticate(username=username, password=password)
#         else:
#             msg = _('Must include either "username" or "email" and "password".')
#             raise exceptions.ValidationError(msg)

#         return user

#     def validate(self, attrs):
#         email = attrs.get("email")
#         password = attrs.get("password")

#         user = None

#         if email:
#             try:
#                 username = UserModel.objects.get(email__iexact=email).get_username()
#             except UserModel.DoesNotExist:
#                 pass

#         # if username:
#         #     user = self._validate_username_email(username, "", password)

#         # Did we get back an active user?
#         if user:
#             if not user.is_active:
#                 msg = _("User account is disabled.")
#                 raise exceptions.ValidationError(msg)
#         else:
#             msg = _("Unable to log in with provided credentials.")
#             raise exceptions.ValidationError(msg)

#         attrs["user"] = user
#         return attrs


# class PasswordChangeSerializer(serializers.Serializer):
#     old_password = serializers.CharField(max_length=32)
#     new_password1 = serializers.CharField(max_length=32)
#     # new_password2 = serializers.CharField(max_length=128)

#     set_password_form_class = SetPasswordForm

#     def __init__(self, *args, **kwargs):
#         self.old_password_field_enabled = getattr(
#             settings, "OLD_PASSWORD_FIELD_ENABLED", True
#         )
#         self.logout_on_password_change = getattr(
#             settings, "LOGOUT_ON_PASSWORD_CHANGE", False
#         )
#         super(PasswordChangeSerializer, self).__init__(*args, **kwargs)

#         if not self.old_password_field_enabled:
#             self.fields.pop("old_password")

#         self.request = self.context.get("request")
#         self.user = getattr(self.request, "user", None)

#     def validate_old_password(self, value):
#         invalid_password_conditions = (
#             self.old_password_field_enabled,
#             self.user,
#             not self.user.check_password(value),
#         )

#         if all(invalid_password_conditions):
#             raise serializers.ValidationError("Invalid password")
#         return value

#     def validate(self, attrs):
#         self.set_password_form = self.set_password_form_class(
#             user=self.user, data=attrs
#         )

#         if not self.set_password_form.is_valid():
#             raise serializers.ValidationError(self.set_password_form.errors)
#         return attrs

#     def save(self):
#         self.set_password_form.save()
#         if not self.logout_on_password_change:
#             from django.contrib.auth import update_session_auth_hash

#             update_session_auth_hash(self.request, self.user)
