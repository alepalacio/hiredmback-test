from datetime import datetime

from django.contrib.sessions.models import Session
from django.contrib.auth import logout

from rest_framework import renderers, parsers
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.schemas import ManualSchema
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.decorators import api_view, permission_classes

from users.models import User
from users.serializers import UserSerializer, LoginSerializer, UserTokenSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """
    Registers user to the server. Input should be in the format:
    {
        "email": "email@emails.com",
        "password": "1973zpqm",
    }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message':'User registered successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserAPIView(APIView):
    
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    
    def put(self, request, pk):
        user = User.objects.filter(id=pk).first()
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    #serializer_class = UserTokenSerializer
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


obtain_auth_token = ObtainAuthToken.as_view()
    
# Login de usuario con el modelo herencia de ObtainAuthToken modificado.
class Login(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        # Traemos el serializador personalizado para el login.
        login_serializer = LoginSerializer(data = request.data, context = {'request': request})
        
        if login_serializer.is_valid():
            #print(login_serializer.validated_data['user'])
            user = login_serializer.validated_data['user']
            
            # Si es un usuario activo se obtiene o se va a crear el token
            if user.is_active:
                token, created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                
                # Si es creado, devolvemos como respuesta el token, el email que viene del serializador UserTokenSerializer y un mensaje.
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Logged in successfully'
                    }, status=status.HTTP_201_CREATED)
                
                # Si el usuario desea iniciar sesión desde otro dispositivo, se elimina la sesión y también su token.
                else:
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                    if all_sessions.exists():
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Logged in successfully'
                    }, status=status.HTTP_201_CREATED)
                    
            else: 
                return Response({'error': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED)
            
        else: 
            return Response({'error': 'Wrong email or password. Try again'}, status=status.HTTP_400_BAD_REQUEST)
        
# Logout de usuario
class Logout(APIView):
    
    def get(self, request, *args, **kwargs):
        
            token = Token.objects.filter(key = request.GET.get('token')).first()
            print(token)
            if token:
                user = token.user
                all_sessions = Session.objects.filter(expire_date__gte = datetime.now())
                if all_sessions.exists():
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            # Si coincide el id del usuario con información de sesión del usario, eliminamos la sesión.
                            session.delete()
                # También eliminamos el token.            
                token.delete()
                
                session_message = 'User sessions deleted'
                token_message = 'User token deleted'
                
                return Response({'session_message':session_message, 'token_message':token_message}, status=status.HTTP_200_OK)
            return Response({'error':'User not found'}, status=status.HTTP_400_BAD_REQUEST)