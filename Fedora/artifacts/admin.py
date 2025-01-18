from django.contrib import admin

# Register your models here.
from .models import Artifact

@admin.register(Artifact)
class ArtifactAdmin(admin.ModelAdmin):
    list_display = ("name","shiny")