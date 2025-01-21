"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from nome_do_app.views import home, CodigoListCreateAPIView, CodigoEntradaViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('nome_do_app.urls')),
    path('', home, name='home'),  # Add this line to include the home view
    path('api/codigos/', CodigoListCreateAPIView.as_view(), name='codigo-list-create'),  # Add this line to include the CodigoListCreateAPIView
    path('api/codigos/<int:pk>/', CodigoEntradaViewSet.as_view({'put': 'update'}), name='codigo-update'),  # Add this line for updating a single entry
]
