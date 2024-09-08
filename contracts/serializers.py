from django.db.models import Q
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from django.utils.dateparse import parse_datetime
from rest_framework.views import APIView

from .models import Property, Reservation
from rest_framework.response import Response
from django.utils import timezone


class PropertySerializer(serializers.ModelSerializer):
    """serializer for the Property model"""

    class Meta:
        model = Property
        fields = [
            "id",
            "property_name",
            "property_type",
            "total_room_number",
            "location",
            "neighborhood",
            "accessibility",
        ]


class ReservationSerializer(serializers.ModelSerializer):
    """serializer for the Reservation model"""

    class Meta:
        model = Reservation
        fields = [
            "id",
            "customer",
            "property",
            "room_number",
            "reservation_starts",
            "reservation_ends",
        ]
        read_only_fields = [
            "property",
        ]

    def validate_reservation_starts(self, value):
        """checking start date not to be in the past"""

        if value < timezone.now():
            raise ValidationError("Reservation start time cannot be in the past.")
        return value

    def validate_reservation_ends(self, value):
        """checking reservation_ends is after the start date"""

        reservation_starts_str = self.initial_data.get("reservation_starts")
        # reformat str to datetime
        reservation_starts = parse_datetime(reservation_starts_str)

        if reservation_starts is None:
            raise ValidationError("Invalid reservation start time format.")

        # make sure both datetimes are timezone-aware
        if timezone.is_naive(reservation_starts):
            reservation_starts = timezone.make_aware(
                reservation_starts, timezone.get_default_timezone()
            )
        if timezone.is_naive(value):
            value = timezone.make_aware(value, timezone.get_default_timezone())

        # main check
        if value <= reservation_starts:
            raise ValidationError("Reservation end time must be after the start time.")
        return value

    def create(self, validated_data):
        room_number = validated_data.get("room_number")

        property_id = self.context.get("property_id")
        property_obj = Property.objects.get(id=property_id)

        reservation_starts = validated_data.get("reservation_starts")
        reservation_ends = validated_data.get("reservation_ends")

        # calculate how many room is booked in a time range
        booked = Reservation.objects.filter(property=property_obj).filter(
            Q(reservation_starts__lt=reservation_ends)
            & Q(reservation_ends__gt=reservation_starts)
        )
        amount = 0
        if booked.exists():
            for obj in booked:
                amount += obj.room_number
        # check if requested room number is less than available room number
        if room_number < property_obj.total_room_number - amount:
            # create reservation
            a = Reservation.objects.create(property=property_obj, **validated_data)
            return a
        raise ValidationError(
            {
                "error": "Not Available",
                "detail": f"There is '{property_obj.total_room_number - amount}' room on chosen date and time",
            }
        )


class CheckAvailabilitySerializer(serializers.Serializer):
    """serializer for check availability"""

    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    room_number = serializers.IntegerField()

    def validate(self, attrs):
        """validate start and end time"""
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if start_time < timezone.now():
            raise ValidationError("Start time cannot be in the past.")
        if end_time < start_time:
            raise ValidationError("End time cannot be earlier than start time.")
        return attrs
