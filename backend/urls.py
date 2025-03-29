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
from Guia_de_transporte.views import GuiaDeTransporteViewSet, GuiaDeTransporteListCreateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('nome_do_app.urls')),
    path('api/', include('authentication.urls')),
    path('api/avarias/', include('avarias_a_receber.urls')),
    path('', home, name='home'),
    path('api/codigos/', CodigoListCreateAPIView.as_view(), name='codigo-list-create'),
    path('api/codigos/<int:pk>/', CodigoEntradaViewSet.as_view({'put': 'update'}), name='codigo-update'),
    path('formulario/', include('formulario.urls')),
    path('api/guia/', include('Guia_de_transporte.urls')),
    path('api/', include('Registros_de_Entregas.urls')),
    path('api/guias/', GuiaDeTransporteListCreateView.as_view(), name='guia-list-create'),
    path('api/vacation/', include('Férias.urls')),
    path('api/despesas/', include('despesas_carro.urls'))
]
