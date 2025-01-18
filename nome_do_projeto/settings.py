# ...existing code...

INSTALLED_APPS = [
    # ...existing apps...
    'rest_framework',
    'corsheaders',
    'nome_do_app',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ...existing middleware...
]

# CORS settings
CORS_ALLOW_ALL_ORIGINS = True  # For development only
# For production, use:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://your-frontend-domain.com",
# ]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100
}
