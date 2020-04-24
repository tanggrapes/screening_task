from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import LookUp

# Create your views here.


class LookUpView(viewsets.ViewSet):
    def list(self, request):
        queryset = LookUp.objects.all()
        serializer = LookUpSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = LookUp.objects.all()
        lookup = get_object_or_404(queryset, pk=pk)
        serializer = LookUpSerializer(lookup)
        return Response(serializer.data)

    def create(self, request):
        # serialize data from request
        serializer = LookUpSerializer(data=request.data)
        if serializer.is_valid():
            lookup = serializer.create(serializer.validated_data)
            # serialize data from db/query
            serializer = LookUpSerializer(lookup)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        # get lookup from db
        queryset = LookUp.objects.all()
        lookup_in_db = get_object_or_404(queryset, pk=pk)
        # serialize data from request
        serializer = LookUpSerializer(data=request.data)
        if serializer.is_valid():
            lookup = serializer.update(lookup_in_db, serializer.data)
            # serialize the updated data
            serializer = LookUpSerializer(lookup)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = LookUp.objects.all()
        lookup = get_object_or_404(queryset, pk=pk)
        lookup.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ValueView(viewsets.ViewSet):
    def list(self, request):
        queryset = Value.objects.all()
        serializer = ValueSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Value.objects.all()
        value = get_object_or_404(queryset, pk=pk)
        serializer = ValueSerializer(value)
        return Response(serializer.data)

    def create(self, request):
        serializer = ValueSerializer(data=request.data)
        if serializer.is_valid():
            lookup = LookUp.objects.get(pk=request.data["lookup"])
            value = Value.objects.create(lookup=lookup, **serializer.data)
            serializer = ValueSerializer(value)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        queryset = Value.objects.all()
        value = get_object_or_404(queryset, pk=pk)
        # serialize data from request
        serializer = ValueSerializer(data=request.data)
        if serializer.is_valid():
            lookup = LookUp.objects.get(pk=request.data["lookup"])
            value.title = serializer.data["title"]
            value.definition = serializer.data["definition"]
            value.lookup = lookup
            value.save()
            serializer = ValueSerializer(value)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        queryset = Value.objects.all()
        value = get_object_or_404(queryset, pk=pk)
        value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
