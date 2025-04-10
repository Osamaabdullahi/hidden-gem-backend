from rest_framework import serializers
from .models import CustomUser, CountyDetails, Destinations, DestinationsImages, Review
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'full_name', 'password')

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user

class CountyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountyDetails
        fields = '__all__'

class DestinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destinations
        fields = '__all__'

class DestinationsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = DestinationsImages
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'destination', 'full_name', 'comment', 'rating', 'date']  # Include all fields

