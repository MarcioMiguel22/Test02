from xml.etree.ElementInclude import XINCLUDE
from django.http import HttpResponse
from django.urls import include, path
from . import views
from nome_do_app import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nome_do_app.urls')),  
]
