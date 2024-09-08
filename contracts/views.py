from django.db.models import Q
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Property, Reservation
from .serializers import (
    PropertySerializer,
    ReservationSerializer,
    CheckAvailabilitySerializer,
)


class PropertyModelViewSet(viewsets.ModelViewSet):
    """
    Property CRUD functionality using ModelViewSet
    """

    queryset = Property.objects.all()
    serializer_class = PropertySerializer


class CreateReservationView(GenericAPIView):
    """
    Creating reservation
    """

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, property_id):
        # sending data and property_id to serializer to check their validation
        serializer = self.serializer_class(
            data=request.data, context={"property_id": property_id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CheckRoomAvailability(GenericAPIView):
    queryset = Reservation.objects.all()
    serializer_class = CheckAvailabilitySerializer

    def post(self, request, property_id):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_time = serializer.validated_data["start_time"]
        end_time = serializer.validated_data["end_time"]
        room_number_requested = serializer.validated_data["room_number"]

        property_obj = Property.objects.get(id=property_id)

        # get all the reservation on given time range
        all_reservations = Reservation.objects.filter(property=property_obj).filter(
            Q(reservation_starts__lt=end_time) & Q(reservation_ends__gt=start_time)
        )

        if not all_reservations.exists():  # there is no reservation on given time range
            return Response(
                data={
                    "detail": f"property {property_obj} is available for reservations with {property_obj.total_room_number} rooms"
                }
            )
        else:  # counting all booked rooms number
            reserved_rooms = 0
            for reservation in all_reservations:
                reserved_rooms += reservation.room_number
            # check if requested room number is less than available ones.
            if room_number_requested < property_obj.total_room_number - reserved_rooms:
                return Response(
                    data={
                        "detail": f"property {property_obj} is available for reservations with {property_obj.total_room_number - reserved_rooms} rooms"
                    }
                )
            return Response(data={"detail": "Not Available"})


class PropertyReservationsReportView(GenericAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get(self, request, property_id):
        try:
            property_obj = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            return Response(
                data={"detail": "property not found"}, status=status.HTTP_404_NOT_FOUND
            )

        reservations = Reservation.objects.filter(property=property_obj)
        serializer = ReservationSerializer(reservations, many=True)
        data = serializer.data
        return render(
            request,
            "contracts/reservation_report.html",
            context={"property_name": property_obj.property_name, "data": data},
        )
