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
