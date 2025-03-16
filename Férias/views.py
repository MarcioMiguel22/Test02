from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import render
from .models import Vacation
from .serializers import VacationSerializer

class VacationViewSet(viewsets.ModelViewSet):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        pending = Vacation.objects.filter(status='pending')
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def approved(self, request):
        approved = Vacation.objects.filter(status='approved')
        serializer = self.get_serializer(approved, many=True)
        return Response(serializer.data)
