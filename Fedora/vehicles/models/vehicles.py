from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=50)


class Part(models.Model):
    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
