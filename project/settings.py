# Add these settings to your project settings.py file

# ... existing settings ...

INSTALLED_APPS = [
    # ... existing apps ...
    'rest_framework',
    'corsheaders',
    'authentication',
]

MIDDLEWARE = [
    # ... existing middleware ...
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ... other middleware ...
]

# CORS settings - Allow frontend to connect to backend
CORS_ALLOW_ALL_ORIGINS = True  # In production, specify exact origins instead

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Frontend URL for links in emails
FRONTEND_URL = 'http://localhost:3000'  # Change in production

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Change to your SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'  # Change to your email
EMAIL_HOST_USER_PASSWORD = 'your-app-password'  # Change to your email password/app password

# For development/testing, you can use console backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
