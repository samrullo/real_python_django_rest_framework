from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from .serializers import BookSerializer
from .models import Book
from django.contrib.auth.decorators import login_required


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsSuperUser | IsAdminUser]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Book.objects.all()
        return Book.objects.filter(restricted=False).all()


@login_required
def library(request):
    return render(request, "library.html")
