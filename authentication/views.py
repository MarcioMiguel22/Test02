from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
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

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    
    if not email:
        return Response({
            "status": "error", 
            "message": "Email é obrigatório."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
        
        # Generate password reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        # Create password reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
        
        # Send email with reset link
        send_mail(
            subject="Recuperação de senha",
            message=f"Olá {user.username},\n\nVocê solicitou a recuperação de senha. Clique no link abaixo para redefinir sua senha:\n\n{reset_link}\n\nSe você não solicitou esta alteração, ignore este email.\n\nAtenciosamente,\nEquipe de suporte",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        
        return Response({
            "status": "success",
            "message": "Enviamos um email com instruções para recuperar sua senha."
        }, status=status.HTTP_200_OK)
    
    except User.DoesNotExist:
        # For security reasons, don't reveal that the email doesn't exist
        return Response({
            "status": "success",
            "message": "Se o email estiver cadastrado em nosso sistema, enviaremos instruções para recuperar a senha."
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({
            "status": "error",
            "message": "Não foi possível processar sua solicitação."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    new_password = request.data.get('password')
    
    if not all([uid, token, new_password]):
        return Response({
            "status": "error",
            "message": "Todos os campos são obrigatórios."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Decode user id
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        # Verify token is valid
        if not default_token_generator.check_token(user, token):
            return Response({
                "status": "error",
                "message": "Link de recuperação inválido ou expirado."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        return Response({
            "status": "success",
            "message": "Senha atualizada com sucesso. Agora você pode fazer login com sua nova senha."
        }, status=status.HTTP_200_OK)
    
    except (User.DoesNotExist, ValueError, TypeError):
        return Response({
            "status": "error",
            "message": "Link de recuperação inválido ou expirado."
        }, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        return Response({
            "status": "error",
            "message": "Não foi possível resetar sua senha."
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)