from django.urls import path

from rentals.views import RentalApi, ReservationApi

urlpatterns = [
    path("reservation", ReservationApi.as_view(), name="reservation"),
    path("listings", RentalApi.as_view(), name="listings"),
]
