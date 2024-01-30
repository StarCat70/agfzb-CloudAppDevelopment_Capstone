from django.contrib import admin
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf

# Register your models here.
admin.site.register(CarMake)
admin.site.register(CarModel)

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
# CarModelAdmin class
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [CarModelInline]
# CarMakeAdmin class with CarModelInline
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'car_make', 'type', 'year']
    search_fields = ['name', 'car_make__name']
    list_filter = ['type', 'year']
    inlines = [CarModelInline]

