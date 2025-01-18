from django.urls import path
from .views import tools

urlpatterns = [path("list_tools/", tools.list_tools)]
