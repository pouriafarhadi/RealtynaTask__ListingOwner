from django.db import models
from django.db.models import Q


class Property(models.Model):
    """
    properties that we want to list out in my webpage

    property options which is not mentions but can be considered:
    - Lot Size and Exterior
    - Interior Layout and Features
    - Age and Upgrades
    - Kitchen
    - Living Room
    - Bedrooms
    - Bathrooms
    - pictures
    """

    # owner = models.CharField(max_length=100, unique=True, )
    propertyTypeChoices = {
        "residential": "Residential",
        "commercial": "Commercial",
        "industrial": "Industrial",
        "rural": "Rural",
        "land": "Land",
        "rental": "Rental",
        "other": "Other",
    }
    property_name = models.CharField(max_length=250, unique=True, db_index=True)
    property_type = models.CharField(
        max_length=250,
        choices=propertyTypeChoices,
        null=True,
        blank=True,
        default="rental",
    )
    location = models.CharField(
        max_length=250, null=True, blank=True
    )  # we don't need this in future processes

    neighborhood = models.CharField(
        null=True, blank=True, max_length=250
    )  # mention any related data like amenities

    accessibility = models.CharField(
        null=True, blank=True, max_length=250
    )  # accessibility and convenience

    total_room_number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.property_name

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"


class Reservation(models.Model):
    """
    store reservation information
    """

    customer = models.CharField(max_length=250)
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="reservations"
    )
    room_number = models.PositiveIntegerField()
    reservation_date = models.DateTimeField(
        auto_now_add=True
    )  # time and date that reservation is created

    reservation_starts = models.DateTimeField()
    reservation_ends = models.DateTimeField()

    def __str__(self):
        return f"{self.property} for {self.customer}"
