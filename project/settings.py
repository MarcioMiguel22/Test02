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
