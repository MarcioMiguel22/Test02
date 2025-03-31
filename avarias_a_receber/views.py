from django.shortcuts import render
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from .models import Avaria, Material, RatesConfiguration
from .serializers import AvariaSerializer, MaterialSerializer, RatesConfigurationSerializer

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

class RatesConfigurationViewSet(viewsets.ModelViewSet):
    queryset = RatesConfiguration.objects.all()
    serializer_class = RatesConfigurationSerializer
    
    def get_queryset(self):
        queryset = RatesConfiguration.objects.all()
        user = self.request.query_params.get('user', None)
        if user is not None:
            queryset = queryset.filter(current_user=user)
        return queryset
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current user's rates or create default if doesn't exist"""
        user = request.query_params.get('user', None)
        
        try:
            config = RatesConfiguration.objects.get(current_user=user)
        except RatesConfiguration.DoesNotExist:
            # Create default configuration
            config = RatesConfiguration.objects.create(current_user=user)
        
        serializer = self.get_serializer(config)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_rates(self, request):
        """Update rates for current user"""
        user = request.data.get('current_user', None)
        
        try:
            config = RatesConfiguration.objects.get(current_user=user)
        except RatesConfiguration.DoesNotExist:
            config = RatesConfiguration.objects.create(current_user=user)
        
        serializer = self.get_serializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
