from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def myview(request):
    return HttpResponse('Olá, mundo!')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', myview),
]
