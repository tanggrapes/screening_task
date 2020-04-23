from django.db import models


class LookUp(models.Model):
    title = models.CharField(max_length=255, unique=True)


class Value(models.Model):
    lookup = models.ForeignKey(LookUp, on_delete=models.CASCADE, related_name="values")
    title = models.CharField(max_length=255, unique=True)
    definition = models.TextField()
