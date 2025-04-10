from django.contrib import admin
from .models import CustomUser, CountyDetails, Destinations, DestinationsImages, Review

# Register the CustomUser model
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'is_active', 'is_staff')  # Fields to display in the admin list view
    search_fields = ('email', 'full_name')  # Fields to search by
    list_filter = ('is_active', 'is_staff')  # Filters in the admin sidebar

# Register the CountyDetails model
@admin.register(CountyDetails)
class CountyDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Customize fields to display
    search_fields = ('name',)

# Register the Destinations model
@admin.register(Destinations)
class DestinationsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'county')  # Customize fields to display
    search_fields = ('name', 'category', 'county')
    list_filter = ('category', 'county')

# Register the DestinationsImages model
@admin.register(DestinationsImages)
class DestinationsImagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'place', 'image')  # Customize fields to display
    search_fields = ('place__name',)  # Search by related place name

# Register the Review model
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'destination', 'full_name', 'rating', 'date')  # Customize fields to display
    search_fields = ('destination__name', 'full_name')  # Search by destination name and user full name
    list_filter = ('rating', 'date')  # Filters in the admin sidebar
