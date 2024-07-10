from django.urls import path

from rentals.views import RentalApi, ReservationApi

urlpatterns = [
    path("reservation", ReservationApi.as_view(), name="reservation"),
    path("reservation/<int:id>", ReservationApi.as_view(), name="reservation_by_id"),
    
    path("listing", RentalApi.as_view(), name="listing"),
    path("listing/<int:id>", RentalApi.as_view(), name="listing_by_id"),

]
