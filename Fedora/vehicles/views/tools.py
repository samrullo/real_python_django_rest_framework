from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Tool
from ..serializers import ToolSerializer


@api_view(["GET"])
def list_tools(request):
    tools = [Tool("hammer", "Mastercraft"), Tool("wrench", "Husky")]
    serializer = ToolSerializer(tools, many=True)
    content = {"tools": serializer.data}
    return Response(content)
