import django_filters

from rentals.models import BaseModel, Rental, Reservation


class BaseFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="date"
    )
    updated_at = django_filters.DateTimeFilter(
        field_name="updated_at", lookup_expr="date"
    )

    class Meta:
        model = BaseModel
        fields = ("created_at", "updated_at")


class ReservationFilter(BaseFilter):
    # Filter behavior returns resy's with OVERLAPPING date ranges,
    #   hence swapped field names

    # end_time >= start_time arg && start_time <= end_time arg
    start_time = django_filters.DateTimeFilter(field_name="end_time", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="lte")

    class Meta:
        model = Reservation
        fields = ("rental", "start_time", "end_time")


class RentalFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Rental
        fields = ("rental_type", "name")


def reservation_list(*, filters=None):
    filters = filters or {}

    qs = Reservation.objects.all()

    return ReservationFilter(filters, qs).qs


def rental_list(*, filters=None):
    filters = filters or {}

    qs = Rental.objects.all()

    return RentalFilter(filters, qs).qs
