from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from .models import Artifact
from .serializers import ArtifactSerializer


class ArtifactViewset(viewsets.ModelViewSet):
    serializer_class = ArtifactSerializer

    def get_queryset(self):
        return Artifact.objects.all()
