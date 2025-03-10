from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from .models import Avaria, Material
from .serializers import AvariaSerializer, MaterialSerializer

class AvariaListCreate(generics.ListCreateAPIView):
    serializer_class = AvariaSerializer

    def get_queryset(self):
        queryset = Avaria.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(current_user=user)
        return queryset

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)
        serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class AvariaRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Avaria.objects.all()
    serializer_class = AvariaSerializer

    def get_object(self):
        obj = super().get_object()
        user = self.request.query_params.get('user', None)
        
        # If user parameter is provided, check if the user has permission
        if user is not None and obj.current_user != user:
            raise PermissionDenied("You don't have permission to access this avaria")
        return obj
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # If current_user is not already set, use the one from request
        if not instance.current_user and 'current_user' in request.data:
            instance.current_user = request.data['current_user']
            instance.save()
        return super().update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class MaterialListCreate(generics.ListCreateAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

class MaterialRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
