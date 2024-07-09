from django.contrib import admin

from rentals.models import Rental, RentalType, Reservation


@admin.register(RentalType)
class RentalTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "limit")
    search_fields = ("name",)


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rental_type")
    list_filter = ("rental_type",)
    search_fields = ("name", "rental_type__name")


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "rental", "start_time", "end_time", "created_at")
    list_filter = ("rental", "start_time", "end_time")
    search_fields = ("rental__name",)
