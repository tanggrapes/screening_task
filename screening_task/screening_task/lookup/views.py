from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import filters

# Create your views here.


class LookUpListView(generics.ListCreateAPIView):
    queryset = LookUp.objects.all()
    serializer_class = LookUpSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["$title"]


class LookUpView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LookUpSerializer
    queryset = LookUp.objects.all()


class ValueListView(generics.ListCreateAPIView):
    queryset = Value.objects.all()
    serializer_class = ValueSerializer


class ValueView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ValueSerializer
    queryset = Value.objects.all()
