from .models import *
from rest_framework import serializers, fields


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = ("id", "title", "definition")


class LookUpSerializer(serializers.ModelSerializer):
    values = ValueSerializer(many=True)

    class Meta:
        model = LookUp
        fields = ("id", "title", "values")

    def create(self, validated_data):
        lookup_values = validated_data.pop("values")
        lookup = LookUp.objects.create(**validated_data)
        for lookup_value in lookup_values:
            Value.objects.create(lookup=lookup, **lookup_value)
        return lookup

    def update(self, instance, validated_data):
        lookup_values = validated_data.pop("values")
        lookups = (instance.values).all()
        lookups = list(lookups)
        instance.title = validated_data.get("title", instance.title)
        instance.save()
        for lookup_value in lookup_values:
            lookup = lookups.pop(0)
            lookup.title = lookup_value.get("title", lookup.title)
            lookup.definition = lookup_value.get("definition", lookup.definition)
            lookup.save()
        return instance


from django.contrib import admin
