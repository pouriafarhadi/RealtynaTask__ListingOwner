from django.urls import path
from .views import (
    PropertyModelViewSet,
    CreateReservationView,
    CheckRoomAvailability,
    PropertyReservationsReportView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("property", PropertyModelViewSet, basename="property")

urlpatterns = router.urls

# reservation
urlpatterns += [
    # create reservation
    path(
        "property/<int:property_id>/reservation/",
        CreateReservationView.as_view(),
        name="create_reservation",
    ),
    # check room availability
    path(
        "property/<int:property_id>/check-availability/",
        CheckRoomAvailability.as_view(),
        name="check-availability",
    ),
    # overview of
    path(
        "property/<int:property_id>/report/",
        PropertyReservationsReportView.as_view(),
        name="property-reservations-report",
    ),
]
