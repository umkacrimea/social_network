# users/views.py

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        login(request, user)
        
        return Response({
            'user': UserSerializer(user).data,
            'message': 'Пользователь успешно зарегистрирован!'
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Успешный вход!'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'Неверное имя пользователя или пароль'
            }, status=status.HTTP_400_BAD_REQUEST)

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get_object(self):
        return self.request.user

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        logout(request)
        return Response({
            'message': 'Вы успешно вышли из системы'
        }, status=status.HTTP_200_OK)