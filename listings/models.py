from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email




REGION_CHOICES = [
    ("Central", "Central"),
    ("Coast", "Coast"),
    ("Eastern", "Eastern"),
    ("Nairobi", "Nairobi"),
    ("North Eastern", "North Eastern"),
    ("Nyanza", "Nyanza"),
    ("Rift Valley", "Rift Valley"),
    ("Western", "Western"),
]



class CountyDetails(models.Model):
    # Basic Information
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    region = models.CharField(
        max_length=100,
        choices=REGION_CHOICES,
        default='Nairobi',  
    )
    rating = models.DecimalField(max_digits=3, decimal_places=1, help_text="e.g., 4.9", blank=True, null=True)
    review_count = models.PositiveIntegerField(blank=True, null=True)
    overview = models.TextField(help_text="A brief introduction to the county.", blank=True)

    # Quick Facts
    population = models.CharField(max_length=50, help_text="e.g., 1.2 million", blank=True)
    languages = models.CharField(max_length=255, help_text="e.g., English, Swahili", blank=True)
    timezone = models.CharField(max_length=50, help_text="e.g., GMT+3", blank=True)
    best_time_to_visit = models.CharField(max_length=50, help_text="e.g., October to April", blank=True)
    average_temp = models.CharField(max_length=50, help_text="e.g., 24°C (75°F)", blank=True)

    # Weather
    season = models.CharField(max_length=50, help_text="e.g., Summer", blank=True)
    temperature_range = models.CharField(max_length=50, help_text="e.g., 25-32°C", blank=True)
    months = models.CharField(max_length=50, help_text="e.g., Dec-Feb", blank=True)
    weather_description = models.CharField(max_length=255, help_text="e.g., Warm and dry", blank=True)

    # Demographics & Economy
    average_income = models.CharField(max_length=50, help_text="e.g., $15,000 per year", blank=True)
    major_industries = models.TextField(help_text="List of major industries, e.g., Tourism, Agriculture", blank=True)
    cost_of_living_rent = models.CharField(max_length=100, help_text="e.g., $400-600", blank=True)
    cost_of_living_utilities = models.CharField(max_length=100, help_text="e.g., $50-100", blank=True)
    meal_cost = models.CharField(max_length=100, help_text="e.g., $10-20 for mid-range meal", blank=True)
    transport_cost = models.CharField(max_length=100, help_text="e.g., $50 per month", blank=True)

    # Healthcare
    hospital_name = models.CharField(max_length=255, blank=True)
    hospital_type = models.CharField(max_length=50, help_text="e.g., Public or Private", blank=True)
    specialties = models.CharField(max_length=255, help_text="e.g., Cardiology, Neurology", blank=True)
    health_insurance_recommendation = models.BooleanField(default=True)

    # Education
    universities = models.TextField(help_text="List notable universities", blank=True)
    literacy_rate = models.DecimalField(max_digits=4, decimal_places=1, help_text="e.g., 94.3", blank=True, null=True)

    # Infrastructure
    transportation_options = models.TextField(help_text="e.g., Bus, Rail", blank=True)
    utilities = models.TextField(help_text="e.g., electricity: KPLC, internet: Fiber", blank=True)

    # Safety & Emergency
    safety_index = models.CharField(max_length=50, help_text="e.g., Moderate", blank=True)
    safe_areas = models.TextField(help_text="e.g., CBD, Riverside", blank=True)
    police_contact = models.CharField(max_length=20, help_text="Police contact e.g., 999", blank=True)
    ambulance_contact = models.CharField(max_length=20, help_text="Ambulance contact e.g., 911", blank=True)
    county_emergency_contact = models.CharField(max_length=20, help_text="County emergency contact e.g., 112", blank=True)

    def __str__(self):
        return f"{self.name}, {self.region}"





class Destinations(models.Model):
    # Basic Information
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    images = models.CharField(max_length=255)
    region = models.CharField(
        max_length=100,
        choices=REGION_CHOICES,
        default='Nairobi',  # Optional: set a default value if needed
        blank=True
    )

    # Key Details
    description = models.TextField()
    hours_of_operation = models.CharField(max_length=255, help_text="e.g., Mon-Fri 9am-5pm")
    contact_phone = models.CharField(max_length=20, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_website = models.URLField(blank=True, null=True)
    admission_fees = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Free, $10 per person")

    # Visitor Experience
    top_features =models.CharField(max_length=255,blank=True)
    best_times_to_visit = models.CharField(max_length=255, blank=True, help_text="e.g., Evening, Off-peak hours")

    # User Feedback
    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True
    )
    review_count = models.PositiveIntegerField(default=0)

    # Visual Map Location
    map_location = models.CharField(max_length=255, blank=True, help_text="Map coordinates or embedded map link")
    image_url = models.CharField(max_length=255, blank=True, help_text="url src for the image")

    

    def __str__(self):
        return  f"{self.name}"

class DestinationsImages(models.Model):
    place = models.ForeignKey(Destinations, related_name='DestinationsImages', on_delete=models.CASCADE)
    image = models.CharField(max_length=100,blank=True)
    caption = models.CharField(max_length=255, blank=True, help_text="Optional caption for the image")

    def __str__(self):
        return f"Image for {self.place.name}"

class Review(models.Model):
    destination = models.ForeignKey(Destinations, on_delete=models.CASCADE, related_name='reviews')  # Link to Destinations
    full_name = models.CharField(max_length=255)  # Full name of the user
    comment = models.TextField()  # Review comment
    rating = models.PositiveIntegerField()  # Rating (e.g., 1-5)
    date = models.DateTimeField(default=now)  # Date of the review

    def __str__(self):
        return f"Review for {self.destination.name} by {self.full_name}"
