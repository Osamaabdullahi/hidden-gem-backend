from django.urls import path
from .views import RegisterView, LoginView, CountyDetailsView, DestinationsView, DestinationsImagesView, ProfileView, DestinationDetailView, ReviewView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('counties/', CountyDetailsView.as_view(), name='county-details'),
    path('destinations/', DestinationsView.as_view(), name='destinations'),
    path('images/', DestinationsImagesView.as_view(), name='destination-images'),
    path('profile/<int:userid>/', ProfileView.as_view(), name='profile'),
    path('destinations/<int:id>/', DestinationDetailView.as_view(), name='destination-detail'),
    path('reviews/', ReviewView.as_view(), name='reviews'),
]


