from django.contrib import admin
from .models import Vehicle, Part


# Register your models here.
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    pass


@admin.register(Part)
class PartAdmin(admin.ModelAdmin):
    pass
