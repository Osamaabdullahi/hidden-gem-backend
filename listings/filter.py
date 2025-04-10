import django_filters
from .models import Destinations, DestinationsImages, Review,CountyDetails

class DestinationsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Filter by name (case-insensitive)
    category = django_filters.CharFilter(field_name='category', lookup_expr='icontains')  # Filter by category
    county = django_filters.CharFilter(field_name='county', lookup_expr='icontains')  # Filter by county

    class Meta:
        model = Destinations
        fields = ['name', 'category', 'county']  # Fields to filter by


class DestinationsImagesFilter(django_filters.FilterSet):
    # Use the related field for filtering (e.g., place__name)
    place = django_filters.CharFilter(field_name='place__name', lookup_expr='icontains')  # Filter by related name field

    class Meta:
        model = DestinationsImages
        fields = ['place']  # Fields to filter by


class ReviewFilter(django_filters.FilterSet):
    destination = django_filters.CharFilter(field_name='destination__name', lookup_expr='icontains')  # Filter by destination name

    class Meta:
        model = Review
        fields = ['destination']  # Fields to filter by


class CountyDetailsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')  # Filter by county name (case-insensitive)

    class Meta:
        model = CountyDetails
        fields = ['name']  # Fields to filter by