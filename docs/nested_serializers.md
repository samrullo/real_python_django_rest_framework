# Nested Serializers

- DRF provides methods for serializing related ORM objects
- Reference foreign keys by id
- Nest serialized relationships. Objects within objects

# We will continue building on vehicls app

- Building on top of the vehicles app
- Follow along with models, serializers, views, and urls files as shown
- Create and admin.py for the models if desired
- Run makemigrations and migrate as needed
- Use admin to load some data

# Let's build Vehicles models

We will define ```Vehicle``` model that has just one field ```name``` and ```Part``` model which is related to
a ```Vehicle```

```python
from django.db import models


class Vehicle(models.Model):
    name = models.CharField(max_length=50)


class Part(models.Model):
    name = models.CharField(max_length=50)
    make = models.CharField(max_length=50)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
```

One ```Vehicle``` can have multiple ```Part```s.

# Serializers
Below is how we define ```Serializers``` associated with Vehicles and Parts models.

```python
from rest_framework import serializers
from ..models import Vehicle, Part


class SerialNumberField(serializers.Field):
    def to_representation(self, value):
        code = value.make[:3].upper()
        return f"{code}-{value.id}"


class PartSerializer(serializers.ModelSerializer):
    serial_no = SerialNumberField(source="*")

    class Meta:
        model = Part
        fields = ["url", "name", "vehicle", "serial_no"]


class VehicleSerializer(serializers.ModelSerializer):
    part_set = PartSerializer(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = ["id", "name", "part_set"]

```

Let's focus on ```VehicleSerializer```. Pay attention how the field ```part_sets``` is not a field within ```Vehicle``` ORM model,
but rather a serializer fields that is yet another serializer with ```many``` argument as ```True```. We are also marking ```part_set``` as ```read_only```.

The reason we mark ```part_set``` as ```read_only``` is so that we can create ```Vehicles``` without being bound to Parts.
But of course it is up to you whether you want such behavior. It is possible to create Vehicles together with their Parts in one POST request.

```PartSerializer``` is also our regular ```ModelSerializer```, where we associate with django model and specify fields.
But pay attention that we defined a custom field ```serial_no```.
You might ask, what does ```source='*''``` mean when initializing this custom field.
By default DRF uses serializer field name to look up the value of that field within django db model.
By settings ```source='*'``` we are passing the whole db model object as the value.

In case you are wondering where ```url``` field comes from, it is a special DRF field that constructs the ```url``` of the record.

# Viewsets
Finally let's define ModelViewsets associated with our serializers

```python
from rest_framework import viewsets
from ..models import Vehicle, Part
from ..serializers import VehicleSerializer, PartSerializer


class PartViewSet(viewsets.ModelViewSet):
    serializer_class = PartSerializer
    queryset = Part.objects.all()


class VehicleViewSet(viewsets.ModelViewSet):
    serializer_class = VehicleSerializer

    def get_queryset(self):
        return Vehicle.objects.all()
```

Above code shows you two different ways of specifying ```queryset``` for our ```ModelViewSets```

# URLs for viewsets

Let's define ```DefaultRouter``` and register urls for our viewsets

```python
from django.urls import path, include
from .views import tools, vehicles
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"vehicles", vehicles.VehicleViewSet, "vehicles")
router.register(r"parts", vehicles.PartViewSet, "parts")

urlpatterns = [path("", include(router.urls)),
               path("list_tools/", tools.list_tools),
               ]
```

One gotcha. When registering ViewSets to routers, the basename should be in singular form, otherwise DRF will throw an error saying can't find relationship

So need to fix above as below

```python
router.register(r"vehicles", vehicles.VehicleViewSet, "vehicle")
router.register(r"parts", vehicles.PartViewSet, "part")
```