from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user:
        # Generate JWT tokens for the authenticated user
        refresh = RefreshToken.for_user(user)
        
        # Authentication successful
        return Response({
            "status": "success",
            "message": "Login realizado com sucesso!",
            "tokens": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }, status=status.HTTP_200_OK)
    else:
        # Authentication failed
        return Response({
            "status": "error",
            "message": "Usuário ou senha inválidos."
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Validate input data
    if not all([username, email, password]):
        return Response({
            "status": "error", 
            "message": "Todos os campos são obrigatórios."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response({
            "status": "error", 
            "message": "Este nome de usuário já está em uso."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Check if email already exists
    if User.objects.filter(email=email).exists():
        return Response({
            "status": "error", 
            "message": "Este email já está em uso."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Create new user
    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        
        return Response({
            "status": "success",
            "message": "Registro realizado com sucesso!"
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Erro ao criar usuário: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)