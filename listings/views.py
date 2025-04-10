from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .models import CountyDetails, Destinations, DestinationsImages, CustomUser, Review
from .serializers import CountyDetailsSerializer, DestinationsSerializer, DestinationsImagesSerializer, UserSerializer, ReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView
from .filter import DestinationsFilter, DestinationsImagesFilter, ReviewFilter,CountyDetailsFilter  # Import the filter classes




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Save the user instance
        user = serializer.save()
        # Generate a token for the newly created user
        token, _ = Token.objects.get_or_create(user=user)
        # Return the token and user details
        self.response_data = {
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'is_active': user.is_active,
                'is_staff': user.is_staff
            }
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(self.response_data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': {
                    'id':user.id,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff
                }
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CountyDetailsView(ListAPIView):
    queryset = CountyDetails.objects.all()
    serializer_class = CountyDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CountyDetailsFilter  


# class CountyDetailsView(APIView):
#     def get(self, request):
#         counties = CountyDetails.objects.all()
#         serializer = CountyDetailsSerializer(counties, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CountyDetailsSerializer(data=request.data, many=True)  # For bulk creation
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DestinationsView(APIView):
#     def get(self, request):
#         destinations = Destinations.objects.all()
#         serializer = DestinationsSerializer(destinations, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = DestinationsSerializer(data=request.data, many=True)  # For bulk creation
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class DestinationsImagesView(APIView):
#     def get(self, request):
#         images = DestinationsImages.objects.all()
#         serializer = DestinationsImagesSerializer(images, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = DestinationsImagesSerializer(data=request.data, many=True)  # For bulk creation
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DestinationsView(ListAPIView):
    queryset = Destinations.objects.all()
    serializer_class = DestinationsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DestinationsFilter  # Use the filter class defined in filter.py


class DestinationsImagesView(ListAPIView):
    queryset = DestinationsImages.objects.all()
    serializer_class = DestinationsImagesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DestinationsImagesFilter  # Use the filter class defined in filter.py

class ProfileView(APIView):
    permission_classes = [AllowAny]  # Temporarily allow any user
    def get(self, request, userid):
        # Retrieve the user's details by ID
        try:
            user = CustomUser.objects.get(id=userid)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'email': user.email,
            'full_name': user.full_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff
        })

    def put(self, request, userid):
        # Update the user's details by ID
        try:
            user = CustomUser.objects.get(id=userid)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, userid):
        # Delete the user's account by ID
        try:
            user = CustomUser.objects.get(id=userid)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class DestinationDetailView(APIView):
    def get(self, request, id):
        # Retrieve the destination by ID
        try:
            destination = Destinations.objects.get(id=id)
        except Destinations.DoesNotExist:
            return Response({"error": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DestinationsSerializer(destination)
        return Response(serializer.data)

class ReviewView(APIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get(self, request):
        # Filter and return reviews
        reviews = Review.objects.all()
        filterset = ReviewFilter(request.GET, queryset=reviews)
        if filterset.is_valid():
            reviews = filterset.qs
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Handle bulk creation of reviews
        serializer = ReviewSerializer(data=request.data, many=True)  # Allow bulk creation
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
