from django.shortcuts import render

# Create your views here.
from .models import Person
from .serializers import PersonSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def list_people(request):
    people = Person.objects.all()
    serializer = PersonSerializer(people, many=True)
    content = {"people": serializer.data}
    return Response(content)
