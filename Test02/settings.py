# Add to INSTALLED_APPS:
INSTALLED_APPS = [
    # ...existing apps...
    'rest_framework',
    'django_filters',
    'Registros_de_Entregas',  # Correct app name (was 'Registros_de_Entrada')
]

# Add to settings:
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
