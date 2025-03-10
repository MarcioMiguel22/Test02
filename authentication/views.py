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

    if not username or not password:
        return Response({
            'status': 'error',
            'message': 'Usuário e senha são obrigatórios.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            'status': 'error',
            'message': 'Usuário não encontrado.'
        }, status=status.HTTP_404_NOT_FOUND)

    if not user.check_password(password):
        return Response({
            'status': 'error',
            'message': 'Senha incorreta.'
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Generate tokens for authenticated user
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'status': 'success',
        'message': 'Login realizado com sucesso.',
        'tokens': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not username or not email or not password:
        return Response({
            'status': 'error',
            'message': 'Todos os campos são obrigatórios.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({
            'status': 'error',
            'message': 'Este nome de usuário já está em uso.'
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({
            'status': 'error',
            'message': 'Este e-mail já está registrado.'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create new user
    user = User.objects.create_user(username=username, email=email, password=password)
    
    return Response({
        'status': 'success',
        'message': 'Usuário registrado com sucesso.'
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    
    if not email:
        return Response({
            'status': 'error',
            'message': 'Email é obrigatório.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        # We don't want to reveal if a user exists or not
        return Response({
            'status': 'success',
            'message': 'Se o email for válido, você receberá instruções para redefinir sua senha.'
        })
    
    # Generate uid and token
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    
    # Create reset URL - adjust the domain based on your frontend URL
    reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"
    
    # Send email
    try:
        send_mail(
            subject='Redefinição de senha',
            message=f'Para redefinir sua senha, acesse o link: {reset_url}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({
            'status': 'error',
            'message': 'Erro ao enviar o email de redefinição.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({
        'status': 'success',
        'message': 'Instruções para redefinição de senha foram enviadas para o seu email.'
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    uid = request.data.get('uid')
    token = request.data.get('token')
    password = request.data.get('password')
    
    if not uid or not token or not password:
        return Response({
            'status': 'error',
            'message': 'Todos os campos são obrigatórios.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Decode user ID
        user_id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=user_id)
        
        # Verify token
        if not default_token_generator.check_token(user, token):
            return Response({
                'status': 'error',
                'message': 'Token inválido ou expirado.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(password)
        user.save()
        
        return Response({
            'status': 'success',
            'message': 'Senha alterada com sucesso.'
        })
        
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({
            'status': 'error',
            'message': 'Link inválido.'
        }, status=status.HTTP_400_BAD_REQUEST)